# Jalur Afirmasi (Kuota 30%) - Versi NiceGUI

import math
from nicegui import ui
import Ui
from Data import SEKOLAH_DATA, JALUR_INFO

PANDUAN = """• Kuota   : 30%, dari total kursi sekolah.
• Sasaran :
  1. Siswa dari keluarga tidak mampu (dibuktikan surat resmi)
  2. Anak buruh (orang tua terdaftar sebagai buruh)
  3. Penyandang disabilitas
• Dokumen utama :
  - Surat Keterangan Tidak Mampu (SKTM) dari kelurahan
  - Bukti terdaftar di DTKS
  - Kartu Indonesia Pintar (KIP) / bantuan sosial lain
  - Surat keterangan anak buruh (jika berlaku)
  - Surat keterangan disabilitas dari dokter/RS (jika berlaku)
• Semakin banyak kriteria terpenuhi → peluang lebih tinggi."""

KRITERIA = {
    "sktm"       : {"label": "Memiliki Surat Keterangan Tidak Mampu (SKTM)", "bobot": 35},
    "dtks"       : {"label": "Terdaftar di DTKS (Data Terpadu Kesejahteraan Sosial)", "bobot": 30},
    "kip"        : {"label": "Pernah/sedang menerima KIP atau bantuan sosial lain", "bobot": 20},
    "anak_buruh" : {"label": "Orang tua terdaftar sebagai buruh (ada kartu/surat)", "bobot": 20},
    "disabilitas": {"label": "Penyandang disabilitas (ada surat keterangan dokter/RS)", "bobot": 25},
}

# ==========================================
# FUNGSI LOGIKA
# ==========================================
def hitung_afirmasi(kriteria_terpenuhi: dict, sekolah: str) -> dict:
    total_poin      = sum(KRITERIA[k]["bobot"] for k, v in kriteria_terpenuhi.items() if v)
    jumlah_kriteria = sum(1 for v in kriteria_terpenuhi.values() if v)
    nilai_akhir     = min(total_poin / 80 * 100, 100)

    if jumlah_kriteria == 0:
        peluang = 0.0
    else:
        selisih = nilai_akhir - 50
        peluang = 1 / (1 + math.exp(-selisih * 0.07)) * 100
        peluang = min(peluang + 8, 100)

    return {
        "nilai_akhir"    : round(nilai_akhir, 2),
        "total_poin"     : total_poin,
        "jumlah_kriteria": jumlah_kriteria,
        "peluang"        : round(peluang, 1),
    }

def buat_saran_afirmasi(peluang, jumlah_kriteria, kriteria_terpenuhi, jenis_disabilitas):
    if jumlah_kriteria == 0:
        return ("Tidak ada kriteria afirmasi yang terpenuhi. "
                "Jalur ini tidak dapat digunakan. "
                "Gunakan jalur Prestasi Akademik atau Domisili.")
    saran = []
    if peluang >= 75:
        saran.append("Kriteria afirmasi kuat — peluang diterima sangat baik.")
    elif peluang >= 50:
        saran.append("Peluang cukup baik. Lengkapi semua dokumen pendukung.")
    else:
        saran.append("Peluang perlu ditingkatkan. Cek kelengkapan dokumen.")

    kurang = [KRITERIA[k]["label"] for k, v in kriteria_terpenuhi.items() if not v]
    if kurang:
        saran.append("Dokumen belum terpenuhi:\n  • " + "\n  • ".join(kurang))
    if kriteria_terpenuhi.get("disabilitas") and jenis_disabilitas:
        saran.append(f"Disabilitas: {jenis_disabilitas}. Pastikan surat dari dokter/RS resmi.")
    saran.append("Semua dokumen harus diunggah saat pendaftaran online PPDB.")
    return "\n\n".join(saran)

# ==========================================
# ANTARMUKA WEB NICEGUI
# ==========================================
def buat_panel():
    with ui.row().classes('w-full items-start gap-6 flex-col md:flex-row'):
        
        # --- KOLOM KIRI (INPUT) ---
        kiri = ui.column().classes('w-full md:w-5/12 bg-[#112240] p-6 rounded-2xl border border-gray-700 shadow-xl')
        
        # --- KOLOM KANAN (HASIL) ---
        kanan = ui.column().classes('w-full md:flex-1 bg-[#152238] p-6 rounded-2xl border border-gray-700 min-h-[400px] justify-center items-center')
        
        with kanan:
            ui.label('Isi data di kiri lalu tekan Hitung').classes('text-gray-400 text-lg text-center')

        with kiri:
            Ui.judul_section('Panduan Afirmasi')
            ui.label(PANDUAN).classes('text-sm text-gray-300 whitespace-pre-line mb-4')

            Ui.judul_section('Pilih Sekolah Tujuan')
            sekolah_opts = list(SEKOLAH_DATA.keys())
            sekolah_select = ui.select(sekolah_opts, value=sekolah_opts[0], label='SMA/SMK Negeri').classes('w-full mb-4').props('dark outlined color="primary"')

            Ui.judul_section('Kriteria Afirmasi (Centang yang berlaku)')
            
            cek_vars = {}
            for key, info in KRITERIA.items():
                with ui.row().classes('w-full items-center justify-between bg-[#1A2840] p-3 rounded-lg mb-2 border border-gray-700 hover:border-teal-500 transition-colors'):
                    cb = ui.checkbox(info['label']).classes('text-sm text-gray-300 flex-grow')
                    ui.label(f"+{info['bobot']}").classes('text-xs font-bold bg-[#00BFA5] text-[#0A192F] px-2 py-1 rounded')
                    cek_vars[key] = cb

            # Input Teks Disabilitas (Menggunakan bind_visibility_from untuk sinkronisasi tampilan reaktif yang aman)
            disabilitas_input = ui.input('Tuliskan jenis disabilitas (Contoh: Tunanetra)').classes('w-full mt-4').props('dark outlined color="primary"')
            disabilitas_input.bind_visibility_from(cek_vars['disabilitas'], 'value')

            # --- FUNGSI TOMBOL ---
            def aksi_hitung():
                sekolah = sekolah_select.value
                terpenuhi = {k: v.value for k, v in cek_vars.items()}

                if not any(terpenuhi.values()):
                    ui.notify('Centang minimal satu kriteria afirmasi yang kamu miliki!', type='warning', position='top')
                    return

                jenis_dis = ""
                if terpenuhi.get("disabilitas"):
                    jenis_dis = disabilitas_input.value
                    if not jenis_dis or not jenis_dis.strip():
                        ui.notify('Kamu mencentang Disabilitas tetapi belum mengisi jenis disabilitas.', type='negative', position='top')
                        return

                hasil = hitung_afirmasi(terpenuhi, sekolah)
                pg = SEKOLAH_DATA[sekolah]["passing_grade_est"]
                saran = buat_saran_afirmasi(hasil["peluang"], hasil["jumlah_kriteria"], terpenuhi, jenis_dis)
                krit_list = [KRITERIA[k]["label"] for k, v in terpenuhi.items() if v]

                detail = [
                    ("Sekolah Tujuan", sekolah),
                    ("Kriteria Terpenuhi", f"{hasil['jumlah_kriteria']} dari {len(KRITERIA)}"),
                    ("Total Poin Kriteria", f"{hasil['total_poin']}"),
                    ("Nilai Akhir Kalkulasi", f"{hasil['nilai_akhir']:.2f}"),
                    ("Est. Passing Grade", f"{pg:.1f}"),
                ]
                if jenis_dis:
                    detail.append(("Jenis Disabilitas", jenis_dis))

                # Render Hasil ke Kolom Kanan
                kanan.classes('justify-start items-stretch')
                Ui.render_hasil(
                    container=kanan,
                    peluang=hasil["peluang"],
                    nilai_akhir=hasil["nilai_akhir"],
                    passing_grade=pg,
                    sekolah=sekolah,
                    jalur="Afirmasi",
                    detail_rows=detail,
                    saran=saran
                )

                # Tambahkan list kriteria yang terpenuhi di bawah hasil standar
                if krit_list:
                    with kanan:
                        with ui.card().classes('w-full bg-[#1A2840] p-4 rounded-xl mt-4 border border-green-800/50'):
                            ui.label('Kriteria Terpenuhi :').classes('font-bold text-[#64FFDA] mb-2 text-sm')
                            for k in krit_list:
                                ui.label(f"✔ {k}").classes('text-sm text-green-400')

            def aksi_reset():
                sekolah_select.value = sekolah_opts[0]
                for cb in cek_vars.values():
                    cb.value = False
                disabilitas_input.value = ''
                kanan.clear()
                kanan.classes('justify-center items-center')
                with kanan:
                    ui.label('Isi data di kiri lalu tekan Hitung').classes('text-gray-400 text-lg text-center')

            # --- TOMBOL ---
            with ui.row().classes('w-full gap-4 mt-6'):
                ui.button('Hitung', on_click=aksi_hitung).classes('flex-grow bg-[#64FFDA] text-[#0A192F] font-bold py-3 rounded-lg shadow-lg')
                ui.button('Reset', on_click=aksi_reset, color='red-500').classes('text-white font-bold py-3 rounded-lg')
                