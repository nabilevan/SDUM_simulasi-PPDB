# Ui.py (Versi NiceGUI Web Modern)

from nicegui import ui

def terapkan_tema():
    """Mengaktifkan Dark Mode dan warna utama aplikasi"""
    ui.dark_mode().enable()
    # Menggunakan palet warna modern (Dark/Neon)
    ui.colors(primary='#64FFDA', secondary='#0A192F', accent='#00BFA5', 
              info='#3b82f6', success='#10b981', warning='#f59e0b', negative='#ef4444')

def judul_section(text):
    """Membuat judul bagian dengan garis bawah rapi"""
    ui.label(text).classes('text-xl font-bold text-[#64FFDA] mt-8 mb-4 border-b border-[#64FFDA]/30 pb-2 w-full')

def render_hasil(container, peluang: float, nilai_akhir: float, passing_grade: float, sekolah: str, jalur: str, detail_rows: list, saran: str, catatan_tambahan: str = ""):
    """Merender tampilan kartu hasil simulasi"""
    
    # 1. Bersihkan hasil lama jika tombol hitung ditekan berkali-kali
    container.clear() 
    
    with container:
        # Menentukan apakah peluangnya tinggi atau rendah (ambang batas 50%)
        diterima = peluang >= 50
        stat_bg = 'bg-green-600' if diterima else 'bg-red-600'
        stat_text = "PELUANG TINGGI" if diterima else "PELUANG RENDAH"

        # 2. Kartu Status Utama (Berwarna Merah/Hijau)
        with ui.column().classes(f'w-full {stat_bg} p-6 rounded-xl text-center text-white items-center shadow-lg'):
            ui.label(stat_text).classes('text-2xl font-bold tracking-widest')
            ui.label(sekolah).classes('text-lg mt-1')
            ui.label(f'Jalur {jalur}').classes('text-sm opacity-80 mt-1')

        # 3. Kartu Persentase (Progress Bar)
        with ui.card().classes('w-full bg-[#112240] p-6 rounded-xl border border-gray-700 mt-4 items-center shadow-lg'):
            ui.label(f'Peluang Diterima: {peluang:.1f}%').classes('text-3xl font-mono text-white mb-2 font-bold')
            warna_bar = 'positive' if diterima else 'negative'
            # Progress bar bawaan NiceGUI
            ui.linear_progress(peluang/100, show_value=False).props(f'color="{warna_bar}" size="20px" rounded').classes('w-full')

        # 4. Kartu Detail Perhitungan
        with ui.card().classes('w-full bg-[#07111F] p-4 rounded-xl border border-gray-800 mt-4'):
            for lab, val in detail_rows:
                with ui.row().classes('w-full justify-between py-2 border-b border-gray-800/50'):
                    ui.label(lab).classes('text-gray-400 text-sm')
                    ui.label(str(val)).classes('text-white font-mono font-bold text-sm')

        # 5. Kartu Saran & Rekomendasi
        with ui.card().classes('w-full bg-blue-900/20 p-5 rounded-xl border border-blue-800/30 mt-4'):
            ui.label('Saran & Rekomendasi').classes('text-lg font-bold text-[#64FFDA] mb-2')
            ui.label(saran).classes('text-gray-300 text-sm')
            if catatan_tambahan:
                ui.label(catatan_tambahan).classes('text-yellow-400 text-sm mt-3 font-semibold')

        # 6. Catatan Kaki (Disclaimer)
        ui.label('⚠ Hasil ini SIMULASI — bukan keputusan resmi PPDB Surabaya.').classes('text-xs text-gray-500 mt-6 text-center w-full')