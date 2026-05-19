# Jalur Prestasi Non-Akademik (5%) - Versi NiceGUI

import math
from nicegui import ui
import Ui
from Data import SEKOLAH_DATA, JALUR_INFO, PRESTASI_BOBOT, JUARA_BOBOT

PANDUAN = """• Kuota  : 5%, dari total kursi sekolah.
• Cara input :
  1. Pilih sekolah tujuan.
  2. Masukkan jumlah lomba yang pernah MENANG/JUARA.
  3. Klik "(+) Buat Form Lomba".
  4. Isi detail tiap lomba: jenis, tingkat, posisi juara.
• Bobot : Juara 1 Internasional >> Juara 1 Nasional >> dst.
• Semua lomba dihitung secara akumulatif."""

JENIS_LOMBA = [
    "Akademik (Olimpiade, KSN, LCC, dll.)",
    "Sains & Teknologi",
    "Olahraga",
    "Seni & Budaya",
    "Karya Tulis / Penelitian",
    "Lainnya",
]
JANGKAUAN_LIST = list(PRESTASI_BOBOT.keys())[1:]
JUARA_LIST     = list(JUARA_BOBOT.keys())

# ==========================================
# FUNGSI LOGIKA (Sama seperti versi asli)
# ==========================================
def hitung_lomba_tunggal(jangkauan, posisi):
    return PRESTASI_BOBOT[jangkauan] * JUARA_BOBOT[posisi]

def hitung_prestasi_non(lomba_list, sekolah):
    skor_lomba  = [hitung_lomba_tunggal(l["jangkauan"], l["posisi"]) for l in lomba_list]
    total_skor  = sum(skor_lomba)
    if total_skor == 0:
        nilai_akhir = 0.0
    else:
        nilai_akhir = min(math.log1p(total_skor) / math.log1p(36) * 100, 100)
    pg      = SEKOLAH_DATA[sekolah]["passing_grade_est"]
    selisih = nilai_akhir - pg
    peluang = 1 / (1 + math.exp(-selisih * 0.09)) * 100
    return {
        "skor_lomba" : skor_lomba,
        "total_skor" : round(total_skor, 2),
        "nilai_akhir": round(nilai_akhir, 2),
        "peluang"    : round(min(peluang, 100), 1),
        "pg"         : pg,
        "selisih"    : round(nilai_akhir - pg, 2),
    }

def buat_saran_non(hasil, lomba_list):
    p, na, pg = hasil["peluang"], hasil["nilai_akhir"], hasil["pg"]
    saran = []
    if p >= 75:
        saran.append("Prestasi sangat kuat! Siapkan sertifikat/piagam asli yang dilegalisir.")
    elif p >= 50:
        saran.append("Prestasi cukup kompetitif. Lengkapi semua dokumen lomba.")
        saran.append("Tips :\n  • Lomba nasional & internasional memberikan bobot terbesar.\n"
                     "  • Tambah lomba baru sebelum PPDB untuk meningkatkan skor.")
    elif p >= 30:
        saran.append(f"Nilai akhir ({na:.2f}) masih di bawah passing grade ({pg}).")
        saran.append("Saran :\n  • Ikuti lomba tingkat yang lebih luas.\n"
                     "  • Posisi juara lebih tinggi meningkatkan bobot signifikan.\n"
                     "  • Pertimbangkan jalur Prestasi Akademik sebagai alternatif.")
    else:
        saran.append("Skor prestasi belum cukup kompetitif untuk jalur ini.")
        saran.append("Rekomendasi : gunakan jalur Domisili, Afirmasi, atau Prestasi Akademik.")
    if lomba_list and hasil["skor_lomba"]:
        best_idx = hasil["skor_lomba"].index(max(hasil["skor_lomba"]))
        best = lomba_list[best_idx]
        saran.append(f"Lomba terbaik: {best['jangkauan']} — {best['posisi']} "
                     f"(Skor: {hasil['skor_lomba'][best_idx]:.2f})")
    return "\n\n".join(saran)

# ==========================================
# ANTARMUKA WEB NICEGUI
# ==========================================
def buat_panel():
    # Menyimpan referensi elemen input dari form dinamis
    form_lomba_refs = []

    with ui.row().classes('w-full items-start gap-6 flex-col md:flex-row'):
        
        # --- KOLOM KIRI (INPUT UTAMA) ---
        kiri = ui.column().classes('w-full md:w-5/12 bg-[#112240] p-6 rounded-2xl border border-gray-700 shadow-xl')
        
        # --- KOLOM KANAN (HASIL & FORM DINAMIS) ---
        kanan = ui.column().classes('w-full md:flex-1 bg-[#152238] p-6 rounded-2xl border border-gray-700 min-h-[400px]')

        # -----------------------------
        # DESAIN KOLOM KIRI
        # -----------------------------
        with kiri:
            Ui.judul_section('Panduan Non-Akademik')
            ui.label(PANDUAN).classes('text-sm text-gray-300 whitespace-pre-line mb-4')

            Ui.judul_section('Sekolah Tujuan & Jumlah Lomba')
            sekolah_opts = list(SEKOLAH_DATA.keys())
            sekolah_select = ui.select(sekolah_opts, value=sekolah_opts[0], label='SMA/SMK Negeri').classes('w-full mb-4').props('dark outlined color="primary"')
            
            with ui.row().classes('w-full items-center gap-2 mb-4'):
                jml_input = ui.number(label='Jumlah Lomba (1-20)', value=1, format='%d').classes('flex-grow').props('dark outlined color="primary"')
                
                # Fungsi untuk membuat baris lomba dinamis di kolom kanan
                def buat_form_lomba():
                    jml = int(jml_input.value or 0)
                    if not (1 <= jml <= 20):
                        ui.notify('Jumlah lomba harus antara 1 sampai 20!', type='warning')
                        return
                    
                    container_form_lomba.clear()
                    form_lomba_refs.clear()

                    with container_form_lomba:
                        ui.label(f'Formulir Detail Lomba ({jml} Lomba)').classes('font-bold text-[#FFD700] mb-2 mt-4')
                        for i in range(jml):
                            with ui.card().classes('w-full bg-[#1A2840] p-4 rounded-lg mb-3 border border-gray-700'):
                                ui.label(f'Lomba #{i+1}').classes('font-bold text-[#64FFDA] mb-2')
                                jenis = ui.select(JENIS_LOMBA, value=JENIS_LOMBA[0], label='Jenis Lomba').classes('w-full mb-2').props('dark outlined')
                                with ui.row().classes('w-full gap-2 flex-nowrap'):
                                    jangkauan = ui.select(JANGKAUAN_LIST, value=JANGKAUAN_LIST[0], label='Tingkat / Jangkauan').classes('w-1/2').props('dark outlined')
                                    posisi = ui.select(JUARA_LIST, value=JUARA_LIST[0], label='Posisi Juara').classes('w-1/2').props('dark outlined')
                                
                                # Simpan agar nilainya bisa dibaca nanti
                                form_lomba_refs.append({'jenis': jenis, 'jangkauan': jangkauan, 'posisi': posisi})
                        
                        ui.button('Hitung Peluang Non-Akademik', on_click=aksi_hitung).classes('w-full bg-[#64FFDA] text-[#0A192F] font-bold py-3 mt-4 rounded-lg shadow-lg')

                ui.button(icon='add', on_click=buat_form_lomba).classes('bg-[#3b82f6] text-white py-3 px-4 rounded-lg').tooltip('Buat Form Lomba')

            ui.label('Masukkan jumlah lomba lalu klik tombol (+) biru.').classes('text-xs text-gray-400 italic mb-4')
            
            ui.button('Reset Simulasi', on_click=lambda: aksi_reset(), color='red-500').classes('w-full text-white font-bold py-3 mt-4 rounded-lg')

        # -----------------------------
        # DESAIN KOLOM KANAN
        # -----------------------------
        with kanan:
            container_hasil = ui.column().classes('w-full')
            container_form_lomba = ui.column().classes('w-full')

            # Tampilan awal kolom kanan
            with container_form_lomba:
                with ui.column().classes('w-full items-center justify-center p-12 opacity-50'):
                    ui.label('Belum ada form lomba.').classes('text-xl text-white')
                    ui.label('Masukkan jumlah lomba di sebelah kiri.').classes('text-sm text-gray-400')

        # --- FUNGSI TOMBOL HITUNG & RESET ---
        def aksi_hitung():
            sekolah = sekolah_select.value

            if not form_lomba_refs:
                ui.notify('Tambahkan dan isi form lomba terlebih dahulu!', type='warning', position='top')
                return

            lomba_list = []
            for ref in form_lomba_refs:
                lomba_list.append({
                    "jenis": ref['jenis'].value,
                    "jangkauan": ref['jangkauan'].value,
                    "posisi": ref['posisi'].value
                })

            hasil = hitung_prestasi_non(lomba_list, sekolah)
            saran = buat_saran_non(hasil, lomba_list)

            detail = [
                ("Sekolah Tujuan", sekolah),
                ("Jumlah Lomba", str(len(lomba_list))),
                ("Total Skor Raw", f"{hasil['total_skor']:.2f}"),
                ("Nilai Akhir Kalkulasi", f"{hasil['nilai_akhir']:.2f}"),
                ("Est. Passing Grade", f"{hasil['pg']:.1f}"),
                ("Selisih", f"{hasil['selisih']:+.2f}"),
            ]

            # Scroll ke atas secara virtual dengan menyembunyikan form
            container_form_lomba.clear()
            
            Ui.render_hasil(
                container=container_hasil,
                peluang=hasil["peluang"],
                nilai_akhir=hasil["nilai_akhir"],
                passing_grade=hasil["pg"],
                sekolah=sekolah,
                jalur="Prestasi Non-Akademik",
                detail_rows=detail,
                saran=saran
            )

            # Rincian Skor Per Lomba
            with container_hasil:
                with ui.card().classes('w-full bg-[#1A2840] p-4 rounded-xl mt-4 border border-blue-800/50'):
                    ui.label('Rincian Skor Per Lomba').classes('font-bold text-[#FFD700] mb-2 text-sm border-b border-gray-700 pb-2')
                    for i, (lomba, skor) in enumerate(zip(lomba_list, hasil["skor_lomba"])):
                        with ui.row().classes('w-full justify-between mt-2'):
                            ui.label(f"#{i+1} {lomba['jangkauan']} · {lomba['posisi']}").classes('text-sm text-gray-300')
                            ui.label(f"Skor: {skor:.2f}").classes('text-sm text-[#64FFDA] font-mono font-bold')
                            
                ui.button('Kembali ke Form Lomba', on_click=buat_form_lomba).classes('w-full bg-[#3b82f6] text-white py-2 mt-4 rounded-lg')

        def aksi_reset():
            sekolah_select.value = sekolah_opts[0]
            jml_input.value = 1
            form_lomba_refs.clear()
            container_hasil.clear()
            container_form_lomba.clear()
            with container_form_lomba:
                with ui.column().classes('w-full items-center justify-center p-12 opacity-50'):
                    ui.icon('emoji_events', size='4rem').classes('text-[#64FFDA] mb-4')
                    ui.label('Belum ada form lomba.').classes('text-xl text-white')
                    ui.label('Masukkan jumlah lomba di sebelah kiri.').classes('text-sm text-gray-400')