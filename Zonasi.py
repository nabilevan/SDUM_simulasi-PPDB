# Jalur Domisili / Zonasi (Kuota 35%) - Versi NiceGUI

import math
from nicegui import ui
import Ui
from Data import SEKOLAH_DATA, JALUR_INFO

PANDUAN = """• Kuota   : 35%, dari total kursi sekolah.
• Dasar   : Jarak dari rumah/tempat tinggal ke sekolah.
  Semakin dekat jarak, semakin besar peluang diterima.
• Syarat  : Alamat KK harus sudah terdaftar minimal 1 tahun
  sebelum PPDB di wilayah zona sekolah yang dituju.
• Data jarak terjauh yang masih diterima per sekolah
  bersumber dari estimasi historis PPDB Kota Surabaya.
• Jika jarak melebihi batas zona, peluang diterima sangat kecil.

Tips : Ukur jarak lewat Google Maps, pilih mode Jalan Kaki."""

# ==========================================
# FUNGSI LOGIKA (Tetap sama seperti aslinya)
# ==========================================
def hitung_zonasi(jarak_m: float, sekolah: str) -> dict:
    jarak_max = SEKOLAH_DATA[sekolah]["jarak_max_m"]
    rasio     = jarak_m / jarak_max

    if rasio <= 0:
        nilai_akhir = 100.0
    elif rasio <= 1.0:
        nilai_akhir = 100 - (rasio ** 1.5) * 60
    else:
        nilai_akhir = max(0, 40 - (rasio - 1) * 80)

    selisih = nilai_akhir - 70
    peluang = 1 / (1 + math.exp(-selisih * 0.08)) * 100
    peluang = min(peluang + 5, 100)

    if jarak_m <= jarak_max * 0.5:
        status = "🟢  Dalam zona inti (jarak sangat dekat)"
    elif jarak_m <= jarak_max:
        status = "🟡  Dalam zona (jarak dapat diterima)"
    elif jarak_m <= jarak_max * 1.3:
        status = "🟠  Di luar zona, masih borderline"
    else:
        status = "🔴  Di luar zona, peluang sangat kecil"

    return {
        "nilai_akhir": round(nilai_akhir, 2),
        "peluang"    : round(peluang, 1),
        "jarak_max"  : jarak_max,
        "rasio"      : round(rasio, 3),
        "status_zona": status,
    }

def buat_saran_zonasi(peluang, jarak_m, jarak_max, sekolah):
    selisih_m = jarak_m - jarak_max
    if peluang >= 80:
        return ("Posisi sangat baik! Jarak rumahmu sangat dekat ke sekolah. "
                "Pastikan dokumen KK valid dan alamat sesuai data Disdukcapil.")
    elif peluang >= 60:
        return ("Jarak masih dalam zona yang baik. "
                "Segera lengkapi dokumen: KK, akta kelahiran, dan surat keterangan domisili.")
    elif peluang >= 40:
        return (f"Jarak mendekati batas zona ({jarak_max:,} m). "
                "Peluang masih ada tetapi persaingan ketat. "
                "Pertimbangkan jalur Prestasi Akademik sebagai cadangan.")
    else:
        over = f"{selisih_m:,.0f} m" if selisih_m > 0 else "terlalu jauh"
        return (f"Jarak melebihi batas zona ({over} dari batas {jarak_max:,} m). "
                "Disarankan mendaftar ke sekolah lain yang lebih dekat, "
                "atau gunakan jalur Prestasi Akademik / Afirmasi jika memenuhi syarat.")


# ==========================================
# ANTARMUKA WEB NICEGUI (Pengganti PanelZonasi Tkinter)
# ==========================================
def buat_panel():
    # Membuat Layout 2 Kolom (Kiri untuk input, Kanan untuk hasil)
    with ui.row().classes('w-full items-start gap-6 flex-col md:flex-row'):
        
        # --- KOLOM KIRI (INPUT) ---
        kiri = ui.column().classes('w-full md:w-5/12 bg-[#112240] p-6 rounded-2xl border border-gray-700 shadow-xl')
        
        # --- KOLOM KANAN (HASIL) ---
        kanan = ui.column().classes('w-full md:flex-1 bg-[#152238] p-6 rounded-2xl border border-gray-700 min-h-[400px] justify-center items-center')
        
        with kanan:
            ui.label('Isi data di kiri lalu tekan Hitung').classes('text-gray-400 text-lg text-center')

        # Mengisi Kolom Kiri
        with kiri:
            Ui.judul_section('Panduan Zonasi')
            ui.label(PANDUAN).classes('text-sm text-gray-300 whitespace-pre-line mb-4')

            Ui.judul_section('Pilih Sekolah Tujuan')
            sekolah_opts = list(SEKOLAH_DATA.keys())
            sekolah_select = ui.select(sekolah_opts, value=sekolah_opts[0], label='SMA/SMK Negeri').classes('w-full mb-1').props('dark outlined color="primary"')
            
            # Label info sekolah dinamis
            info_label = ui.label().classes('text-sm text-[#FFD700] mb-4 font-semibold')

            def update_info():
                sek = sekolah_select.value
                if sek:
                    jarak = SEKOLAH_DATA[sek]['jarak_max_m']
                    tipe = SEKOLAH_DATA[sek]['type']
                    info_label.set_text(f"{tipe} · Jarak terjauh diterima (est.): {jarak:,} m")
            
            sekolah_select.on('update:model-value', update_info)
            update_info() # Panggil awal

            Ui.judul_section('Data Jarak')
            jarak_input = ui.number(label='Jarak rumah ke sekolah (meter)', format='%.1f').classes('w-full mb-1').props('dark outlined color="primary"')
            ui.label('Ukur lewat Google Maps — pilih mode Jalan Kaki').classes('text-xs text-gray-400 mb-6 italic')

            # --- FUNGSI TOMBOL ---
            def aksi_hitung():
                sekolah = sekolah_select.value
                raw_jarak = jarak_input.value

                if raw_jarak is None:
                    ui.notify('Masukkan jarak rumah ke sekolah (dalam meter).', type='warning', position='top')
                    return
                if raw_jarak < 0:
                    ui.notify('Jarak tidak boleh negatif.', type='negative', position='top')
                    return
                if raw_jarak > 30000:
                    ui.notify('Jarak terlalu besar (>30 km). Periksa kembali!', type='negative', position='top')
                    return

                # Panggil logika
                hasil = hitung_zonasi(raw_jarak, sekolah)
                pg = SEKOLAH_DATA[sekolah]["passing_grade_est"]
                saran = buat_saran_zonasi(hasil["peluang"], raw_jarak, hasil["jarak_max"], sekolah)

                detail = [
                    ("Sekolah Tujuan", sekolah),
                    ("Jarak Rumah", f"{raw_jarak:,.0f} m"),
                    ("Batas Zona (est.)", f"{hasil['jarak_max']:,} m"),
                    ("Rasio Jarak", f"{hasil['rasio']:.2f}x batas zona"),
                    ("Nilai Akhir Kalkulasi", f"{hasil['nilai_akhir']:.2f}"),
                    ("Est. Passing Grade", f"{pg:.1f}"),
                    ("Status Zona", hasil["status_zona"]),
                ]

                # Kirim ke container Kanan
                kanan.classes('justify-start items-stretch') # Perbaiki posisi dari tengah ke atas
                Ui.render_hasil(
                    container=kanan,
                    peluang=hasil["peluang"],
                    nilai_akhir=hasil["nilai_akhir"],
                    passing_grade=pg,
                    sekolah=sekolah,
                    jalur="Domisili (Zonasi)",
                    detail_rows=detail,
                    saran=saran,
                    catatan_tambahan="Pastikan alamat di Kartu Keluarga sudah terdaftar minimal 1 tahun sebelum pendaftaran PPDB."
                )

            def aksi_reset():
                jarak_input.value = None
                sekolah_select.value = sekolah_opts[0]
                kanan.clear()
                kanan.classes('justify-center items-center')
                with kanan:
                    ui.label('Isi data di kiri lalu tekan Hitung').classes('text-gray-400 text-lg text-center')

            # --- TOMBOL ---
            with ui.row().classes('w-full gap-4 mt-2'):
                ui.button('Hitung Peluang Zonasi', on_click=aksi_hitung).classes('flex-grow bg-[#64FFDA] text-[#0A192F] font-bold py-3 rounded-lg shadow-lg')
                ui.button('Reset', on_click=aksi_reset, color='red-500').classes('text-white font-bold py-3 rounded-lg')