# Jalur Mutasi (Kuota 5%) - Versi NiceGUI

import math
from nicegui import ui
import Ui
from Data import SEKOLAH_DATA, JALUR_INFO

PANDUAN = """• Kuota  : 5%, dari total kursi sekolah.
• Sasaran: Calon murid yang orang tua/wali-nya mendapat
  surat tugas pindah kerja ke Kota Surabaya.
• Dokumen wajib :
  1. Surat Pindah Tugas dari instansi/perusahaan
  2. Surat Keterangan Domisili baru di Surabaya
  3. Kartu Keluarga (KK) yang sudah diperbarui
  4. Akta Kelahiran siswa
  5. Raport/Ijazah sekolah asal (lengkap)
  6. Surat Keterangan Pindah dari sekolah asal
• Nilai rapor tetap dipertimbangkan sebagai tie-breaker."""

INSTANSI_JENIS = [
    "ASN / PNS (pemerintah pusat / daerah)",
    "TNI / Polri",
    "BUMN / BUMD",
    "Perusahaan Swasta",
    "Instansi Asing / Multinasional",
    "Wiraswasta / Mandiri",
    "Lainnya",
]
ASAL_WILAYAH = [
    "Dalam Kota Surabaya (mutasi antar instansi)",
    "Luar Kota Surabaya (dalam Jawa Timur)",
    "Luar Provinsi Jawa Timur (dalam Indonesia)",
    "Luar Negeri",
]
LAMA_TUGAS_OPT = [
    "< 3 bulan (baru ditetapkan)",
    "3 – 6 bulan",
    "6 – 12 bulan",
    "> 1 tahun",
]
DOKUMEN_LIST = [
    ("surat_tugas",    "Surat Pindah Tugas resmi dari instansi", True),
    ("domisili",       "Surat Keterangan Domisili baru", True),
    ("kk_baru",        "Kartu Keluarga (KK) yang diperbarui", False),
    ("akta",           "Akta Kelahiran siswa", False),
    ("rapor",          "Raport/Ijazah sekolah asal", False),
    ("pindah_sekolah", "Surat Ket. Pindah dari sekolah asal", True),
]

# ==========================================
# FUNGSI LOGIKA (Tetap sama)
# ==========================================
def hitung_mutasi(dokumen_ada, instansi, asal, lama_tugas, rapor, sekolah):
    bobot_dok = {
        "surat_tugas": 30, "domisili": 20, "kk_baru": 15,
        "akta": 10, "rapor": 15, "pindah_sekolah": 10,
    }
    skor_dok = sum(bobot_dok[k] for k, v in dokumen_ada.items() if v)

    bonus_instansi = {
        "ASN / PNS (pemerintah pusat / daerah)": 10,
        "TNI / Polri": 10, "BUMN / BUMD": 8,
        "Perusahaan Swasta": 5, "Instansi Asing / Multinasional": 6,
        "Wiraswasta / Mandiri": 2, "Lainnya": 3,
    }.get(instansi, 3)

    bonus_asal = {
        "Dalam Kota Surabaya (mutasi antar instansi)": 3,
        "Luar Kota Surabaya (dalam Jawa Timur)": 6,
        "Luar Provinsi Jawa Timur (dalam Indonesia)": 10,
        "Luar Negeri": 12,
    }.get(asal, 5)

    bonus_lama = {
        "< 3 bulan (baru ditetapkan)": 8,
        "3 – 6 bulan": 6, "6 – 12 bulan": 4, "> 1 tahun": 2,
    }.get(lama_tugas, 4)

    kontrib_rapor = rapor * 0.15 if rapor > 0 else 0
    total         = skor_dok + bonus_instansi + bonus_asal + bonus_lama + kontrib_rapor
    nilai_akhir   = min(total / 1.2, 100)

    pg      = SEKOLAH_DATA[sekolah]["passing_grade_est"]
    selisih = nilai_akhir - pg
    peluang = 1 / (1 + math.exp(-selisih * 0.07)) * 100
    peluang = min(peluang + 8, 100)

    return {
        "skor_dok"     : skor_dok,
        "bonus_instansi": bonus_instansi,
        "bonus_asal"   : bonus_asal,
        "bonus_lama"   : bonus_lama,
        "kontrib_rapor": round(kontrib_rapor, 2),
        "nilai_akhir"  : round(nilai_akhir, 2),
        "peluang"      : round(peluang, 1),
        "pg"           : pg,
        "selisih"      : round(nilai_akhir - pg, 2),
    }

def buat_saran_mutasi(hasil, dokumen_ada):
    p = hasil["peluang"]
    saran = []
    if p >= 75:
        saran.append("Dokumen lengkap — peluang tinggi! Daftar segera saat PPDB dibuka.")
    elif p >= 50:
        saran.append("Peluang cukup baik. Segera lengkapi dokumen yang belum ada.")
    else:
        saran.append("Peluang perlu ditingkatkan. Perhatikan kelengkapan dokumen berikut:")

    kurang = [label for key, label, _ in DOKUMEN_LIST if not dokumen_ada.get(key)]
    if kurang:
        saran.append("Dokumen belum tersedia :\n  • " + "\n  • ".join(kurang))
    if not dokumen_ada.get("surat_tugas"):
        saran.append("INFO: Surat Pindah Tugas adalah dokumen PALING PENTING "
                     "dan wajib ada. Tanpa ini jalur Mutasi tidak dapat diproses.")
    saran.append("Semua dokumen harus diunggah PDF/JPG saat pendaftaran "
                 "dan dibawa aslinya saat verifikasi.")
    return "\n\n".join(saran)


# ==========================================
# ANTARMUKA WEB NICEGUI
# ==========================================
def buat_panel():
    with ui.row().classes('w-full items-start gap-6 flex-col md:flex-row'):
        
        # --- KOLOM KIRI (INPUT) ---
        kiri = ui.column().classes('w-full md:w-5/12 bg-[#112240] p-6 rounded-2xl border border-gray-700 shadow-xl')
        
        # --- KOLOM KANAN (HASIL & CHECKBOX DOKUMEN) ---
        kanan = ui.column().classes('w-full md:flex-1 bg-[#152238] p-6 rounded-2xl border border-gray-700 min-h-[400px]')

        # -----------------------------
        # DESAIN KOLOM KIRI
        # -----------------------------
        with kiri:
            Ui.judul_section('Panduan Mutasi')
            ui.label(PANDUAN).classes('text-sm text-gray-300 whitespace-pre-line mb-4')

            Ui.judul_section('Informasi Mutasi')
            sekolah_opts = list(SEKOLAH_DATA.keys())
            sekolah_select = ui.select(sekolah_opts, value=sekolah_opts[0], label='SMA/SMK Negeri').classes('w-full mb-3').props('dark outlined color="primary"')
            
            instansi_select = ui.select(INSTANSI_JENIS, value=INSTANSI_JENIS[0], label='Jenis Instansi / Perusahaan').classes('w-full mb-3').props('dark outlined color="primary"')
            asal_select = ui.select(ASAL_WILAYAH, value=ASAL_WILAYAH[0], label='Asal Wilayah Sebelum Pindah').classes('w-full mb-3').props('dark outlined color="primary"')
            lama_select = ui.select(LAMA_TUGAS_OPT, value=LAMA_TUGAS_OPT[0], label='Lama Surat Tugas Diterbitkan').classes('w-full mb-3').props('dark outlined color="primary"')

            Ui.judul_section('Nilai Rapor (Opsional / Tie-breaker)')
            rapor_input = ui.number(label='Rata-rata Rapor Smt 1-5 (Opsional)', format='%.2f').classes('w-full mb-6').props('dark outlined color="primary"')
            
            ui.button('Reset Simulasi', on_click=lambda: aksi_reset(), color='red-500').classes('w-full text-white font-bold py-3 mt-4 rounded-lg')

        # -----------------------------
        # DESAIN KOLOM KANAN
        # -----------------------------
        dok_vars = {}
        with kanan:
            # Area form dokumen (bisa disembunyikan nanti saat hasil muncul)
            container_form_dokumen = ui.column().classes('w-full')
            
            with container_form_dokumen:
                Ui.judul_section('Kelengkapan Dokumen (Centang yang disiapkan)')
                for key, label, wajib in DOKUMEN_LIST:
                    with ui.row().classes('w-full items-center justify-between bg-[#1A2840] p-3 rounded-lg mb-2 border border-gray-700 hover:border-[#64FFDA] transition-colors'):
                        cb = ui.checkbox(label).classes('text-sm text-gray-300 flex-grow')
                        dok_vars[key] = cb
                        
                        if wajib:
                            ui.label('WAJIB').classes('text-[10px] font-bold bg-red-500 text-white px-2 py-1 rounded tracking-wider')
                        else:
                            ui.label('Penting').classes('text-[10px] font-bold bg-yellow-500 text-[#0A192F] px-2 py-1 rounded tracking-wider')

                ui.button('Hitung Peluang Mutasi', on_click=lambda: aksi_hitung()).classes('w-full bg-[#64FFDA] text-[#0A192F] font-bold py-3 mt-6 rounded-lg shadow-lg')

            # Area khusus hasil
            container_hasil = ui.column().classes('w-full')

        # --- FUNGSI TOMBOL HITUNG & RESET ---
        def aksi_hitung():
            # Validasi dokumen wajib (Surat Pindah Tugas)
            if not dok_vars["surat_tugas"].value:
                ui.notify('Surat Pindah Tugas WAJIB dicentang. Tanpa dokumen ini jalur Mutasi tidak bisa diproses!', type='negative', position='top')
                return

            sekolah = sekolah_select.value
            raw_rapor = rapor_input.value or 0.0
            
            if not (0 <= raw_rapor <= 100):
                ui.notify('Nilai rapor harus berada di antara 0 sampai 100.', type='negative', position='top')
                return

            dok_ada = {k: v.value for k, v in dok_vars.items()}
            
            hasil = hitung_mutasi(dok_ada, instansi_select.value, asal_select.value, lama_select.value, raw_rapor, sekolah)
            saran = buat_saran_mutasi(hasil, dok_ada)
            jml_dok = sum(1 for v in dok_ada.values() if v)

            detail = [
                ("Sekolah Tujuan", sekolah),
                ("Jenis Instansi", instansi_select.value.split("(")[0].strip()),
                ("Asal Wilayah", asal_select.value.split("(")[0].strip()),
                ("Lama Surat Tugas", lama_select.value),
                ("Dokumen Tersedia", f"{jml_dok} dari {len(DOKUMEN_LIST)}"),
                ("Skor Dokumen", f"{hasil['skor_dok']}"),
                ("Bonus Instansi", f"+{hasil['bonus_instansi']}"),
                ("Bonus Asal Wilayah", f"+{hasil['bonus_asal']}"),
                ("Bonus Urgensi Waktu", f"+{hasil['bonus_lama']}"),
                ("Kontribusi Rapor", f"+{hasil['kontrib_rapor']:.2f}"),
                ("Nilai Akhir Kalkulasi", f"{hasil['nilai_akhir']:.2f}"),
                ("Est. Passing Grade", f"{hasil['pg']:.1f}"),
                ("Selisih", f"{hasil['selisih']:+.2f}"),
            ]
            if raw_rapor > 0:
                detail.insert(5, ("Rata-rata Rapor", f"{raw_rapor:.2f}"))

            # Sembunyikan checklist dokumen dan tampilkan hasil
            container_form_dokumen.classes(add='hidden')
            
            Ui.render_hasil(
                container=container_hasil,
                peluang=hasil["peluang"],
                nilai_akhir=hasil["nilai_akhir"],
                passing_grade=hasil["pg"],
                sekolah=sekolah,
                jalur="Mutasi",
                detail_rows=detail,
                saran=saran
            )

            # Tambahkan status list dokumen di bawah hasil
            with container_hasil:
                with ui.card().classes('w-full bg-[#1A2840] p-4 rounded-xl mt-4 border border-blue-800/50'):
                    ui.label('Status Kelengkapan Dokumen').classes('font-bold text-[#FFD700] mb-2 text-sm border-b border-gray-700 pb-2')
                    for key, label, _ in DOKUMEN_LIST:
                        ada = dok_ada.get(key, False)
                        if ada:
                            ui.label(f"✔ {label}").classes('text-sm text-green-400 font-semibold mb-1')
                        else:
                            ui.label(f"✘ {label}").classes('text-sm text-red-400 mb-1')
                            
                ui.button('Kembali ke Form Checklist', on_click=kembali_form).classes('w-full bg-[#3b82f6] text-white py-2 mt-4 rounded-lg')

        def kembali_form():
            container_hasil.clear()
            container_form_dokumen.classes(remove='hidden')

        def aksi_reset():
            sekolah_select.value = sekolah_opts[0]
            instansi_select.value = INSTANSI_JENIS[0]
            asal_select.value = ASAL_WILAYAH[0]
            lama_select.value = LAMA_TUGAS_OPT[0]
            rapor_input.value = None
            for cb in dok_vars.values():
                cb.value = False
            kembali_form()