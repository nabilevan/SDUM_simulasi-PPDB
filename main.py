# Main.py (Versi NiceGUI Web Modern)

from nicegui import ui
import os

# Mengambil data dari Data.py
try:
    from Data import SEKOLAH_DATA, JALUR_INFO
except ImportError:
    ui.notify("File Data.py tidak ditemukan atau formatnya salah!", type="negative")
    SEKOLAH_DATA = {}
    JALUR_INFO = {
        "Domisili (Zonasi)": {"kuota": 35, "desc": "Seleksi jarak domisili."},
        "Afirmasi": {"kuota": 30, "desc": "Untuk keluarga tidak mampu."}
    }

# IMPORT SEMUA MODUL JALUR YANG SUDAH DIUBAH KE NICEGUI
import Zonasi
import Afirmasi
import PrestasiAkademik
import PrestasiNonAkademik
import Mutasi
import Ui

# --- FUNGSI HELPER UI ---
def terapkan_tema():
    """Mengaktifkan Dark Mode dan warna utama aplikasi"""
    ui.dark_mode().enable()
    ui.colors(primary='#64FFDA', secondary='#0A192F', accent='#00BFA5', 
              info='#3b82f6', success='#10b981', warning='#f59e0b', negative='#ef4444')

def judul_section(text):
    """Membuat judul bagian dengan garis bawah rapi"""
    ui.label(text).classes('text-xl font-bold text-[#64FFDA] mt-8 mb-4 border-b border-[#64FFDA]/30 pb-2 w-full')

# --- HALAMAN UTAMA ---
@ui.page('/')
def index():
    terapkan_tema()

    # --- TOP BAR (Header) ---
    with ui.header(elevated=True).classes('bg-[#0A192F] items-center justify-between px-8 py-4 border-b border-gray-800'):
        ui.label('PPDB Surabaya Simulator').classes('text-2xl font-bold text-[#64FFDA]')
        ui.label('v2.0 | Data estimasi — bukan keputusan resmi').classes('text-sm text-gray-400 hidden md:block')

    # --- KONTEN UTAMA ---
    with ui.column().classes('w-full max-w-6xl mx-auto mt-6 px-4 pb-20'):
        
        # --- TAB NAVIGASI ---
        with ui.tabs().classes('w-full bg-[#112240] text-gray-300 rounded-xl p-2 shadow-lg mb-6') as tabs:
            tab_dash = ui.tab('Dashboard', icon='space_dashboard')
            tab_zon = ui.tab('Zonasi', icon='place')
            tab_afir = ui.tab('Afirmasi', icon='health_and_safety')
            tab_pres_ak = ui.tab('Prestasi Akademik', icon='menu_book')
            tab_pres_non = ui.tab('Prestasi Non', icon='emoji_events')
            tab_mut = ui.tab('Mutasi', icon='transfer_within_a_station')

        # --- ISI TABS ---
        with ui.tab_panels(tabs, value=tab_dash).classes('w-full bg-transparent p-0'):
            
            # ==========================================
            # TAB 1: DASHBOARD UTAMA
            # ==========================================
            with ui.tab_panel(tab_dash).classes('p-0'):
                
                # 1. Hero Banner
                with ui.column().classes('w-full bg-gradient-to-br from-[#07111F] to-[#0A192F] py-12 rounded-2xl text-center items-center mb-8 border border-gray-800 shadow-xl'):
                    ui.label('SIMULASI PPDB').classes('text-5xl font-bold text-[#64FFDA]')
                    ui.label('SMA / SMK Negeri · Kota Surabaya').classes('text-xl text-gray-300 mt-2 font-semibold')
                    ui.label('Simulasi peluang masuk berdasarkan jalur seleksi resmi PPDB Surabaya').classes('text-gray-500 mt-2')

                # 2. Jalur Seleksi & Kuota
                judul_section('Jalur Seleksi & Alokasi Kuota')
                with ui.grid(columns=5).classes('w-full gap-4 mb-8'):
                    for jalur, info in JALUR_INFO.items():
                        nama_pendek = jalur.split("(")[0].strip()
                        with ui.card().classes('bg-[#112240] p-4 items-center text-center border border-gray-700 hover:border-[#64FFDA] transition-colors cursor-pointer shadow-md'):
                            ui.label(f"{info.get('kuota', 0)}%").classes('text-3xl font-bold text-white')
                            ui.label(nama_pendek).classes('text-sm font-bold text-[#64FFDA] mt-1')
                            ui.label(info.get('desc', '')).classes('text-xs text-gray-400 mt-2')

                # 3. Panduan Penggunaan
                judul_section('Panduan Penggunaan')
                panduan_data = [
                    ("1️. Pilih jalur", "Klik tab jalur yang sesuai kondisimu di bagian atas."),
                    ("2️. Isi data", "Masukkan data sesuai panduan di tiap form."),
                    ("3️. Klik Hitung", "Tekan tombol Hitung untuk melihat persentase peluang."),
                    ("4️. Baca saran", "Perhatikan rekomendasi dokumen dan sekolah alternatif."),
                    ("Penting", "Hasil ini adalah SIMULASI. Keputusan resmi hanya dari Dinas Pendidikan Kota Surabaya.")
                ]
                with ui.column().classes('w-full gap-3 mb-8'):
                    for judul, isi in panduan_data:
                        with ui.row().classes('w-full bg-[#112240] p-4 rounded-lg items-center border border-gray-700 shadow-sm'):
                            ui.label(judul).classes('font-bold text-[#00BFA5] w-36')
                            ui.label(isi).classes('text-gray-300 text-sm')

                # 4. Statistik Sekolah Terdaftar
                judul_section('Statistik Sekolah Terdaftar')
                sma_count = sum(1 for d in SEKOLAH_DATA.values() if d.get("type") == "SMA")
                smk_count = sum(1 for d in SEKOLAH_DATA.values() if d.get("type") == "SMK")
                pg_vals = [d.get("passing_grade_est", 0) for d in SEKOLAH_DATA.values()]
                
                with ui.grid(columns=3).classes('w-full gap-4 mb-8'):
                    def stat_card(label, val, text_color):
                        with ui.card().classes('bg-[#112240] p-6 text-center items-center border border-gray-700 shadow-md'):
                            ui.label(val).classes(f'text-3xl font-bold {text_color}')
                            ui.label(label).classes('text-sm text-gray-400 mt-1')

                    if pg_vals:
                        rata_pg = f"{sum(pg_vals)/len(pg_vals):.1f}"
                        max_pg = str(max(pg_vals))
                        min_pg = str(min(pg_vals))
                    else:
                        rata_pg = max_pg = min_pg = "0"

                    stat_card("Total Sekolah", str(len(SEKOLAH_DATA)), "text-[#64FFDA]")
                    stat_card("SMA Negeri", str(sma_count), "text-green-400")
                    stat_card("SMK Negeri", str(smk_count), "text-blue-400")
                    stat_card("PG Tertinggi", max_pg, "text-red-400")
                    stat_card("PG Terendah", min_pg, "text-yellow-400")
                    stat_card("Rata-rata PG", rata_pg, "text-purple-400")

                # 5. Tabel Daftar Sekolah
                judul_section('Daftar Sekolah & Estimasi Passing Grade')
                baris_tabel = []
                for nama, d in sorted(SEKOLAH_DATA.items(), key=lambda x: -x[1].get("passing_grade_est", 0)):
                    jarak_str = f"{d.get('jarak_max_m', 0):,}" if d.get('jarak_max_m') else "-"
                    baris_tabel.append({
                        'nama': nama, 
                        'tipe': d.get('type', '-'), 
                        'akreditasi': d.get('akreditasi', '-'), 
                        'pg': d.get('passing_grade_est', 0), 
                        'jarak': jarak_str
                    })
                kolom_tabel = [
                    {'name': 'nama', 'label': 'Nama Sekolah', 'field': 'nama', 'align': 'left', 'sortable': True},
                    {'name': 'tipe', 'label': 'Tipe', 'field': 'tipe', 'align': 'center', 'sortable': True},
                    {'name': 'akreditasi', 'label': 'Akreditasi', 'field': 'akreditasi', 'align': 'center'},
                    {'name': 'pg', 'label': 'Est. PG', 'field': 'pg', 'sortable': True},
                    {'name': 'jarak', 'label': 'Zona Maks (m)', 'field': 'jarak'}
                ]
                ui.table(columns=kolom_tabel, rows=baris_tabel, pagination=10).classes('w-full bg-[#112240] text-gray-300 border border-gray-700 mb-2').props('dark flat bordered')
                ui.label('⚠ Passing grade & jarak zona adalah ESTIMASI historis — bukan nilai resmi.').classes('text-xs text-gray-500 italic mt-2')

            # ==========================================
            # MENGHUBUNGKAN TAB KE FILE MODUL
            # ==========================================
            with ui.tab_panel(tab_zon).classes('p-0'):
                Zonasi.buat_panel()
                
            with ui.tab_panel(tab_afir).classes('p-0'):
                Afirmasi.buat_panel()
                
            with ui.tab_panel(tab_pres_ak).classes('p-0'):
                PrestasiAkademik.buat_panel()
                
            with ui.tab_panel(tab_pres_non).classes('p-0'):
                PrestasiNonAkademik.buat_panel()
                
            with ui.tab_panel(tab_mut).classes('p-0'):
                Mutasi.buat_panel()

    # --- FOOTER ---
    with ui.footer().classes('bg-[#0A192F] text-gray-500 p-4 border-t border-gray-800 items-center justify-between'):
        ui.label('⚠ Aplikasi ini adalah alat bantu simulasi. Hasil tidak mengikat.').classes('text-xs')
        ui.label('© Simulasi PPDB Surabaya 2025').classes('text-xs')

# --- JALANKAN SERVER ---
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Simulasi PPDB", host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))