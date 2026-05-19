# Jalur Prestasi Akademik (Kuota 25%) - Versi NiceGUI

import math
from nicegui import ui
import Ui
from Data import SEKOLAH_DATA, JALUR_INFO

PANDUAN = """• Kuota  : 25%, dari total kursi sekolah.
• Rumus  : Nilai Akhir = (Rapor × 60%) + (Rata-rata TKA × 40%)
• TKA    : Tes Kemampuan Akademik meliputi Matematika &
           Bahasa Indonesia (diselenggarakan Dinas Pendidikan).
• Rapor  : Rata-rata nilai semester 1 sampai 5 dari SMP.
• Nilai akhir tertinggi → prioritas diterima.

Tips :
  ✦ Fokus pada nilai Matematika & B. Indonesia di rapor.
  ✦ Latihan soal TKA dari tahun-tahun sebelumnya.
  ✦ Nilai TKA sangat berpengaruh (bobot 40%)."""

# ==========================================
# FUNGSI LOGIKA
# ==========================================
def hitung_prestasi_akademik(rapor, tka_mtk, tka_bindo, sekolah):
    tka_avg     = (tka_mtk + tka_bindo) / 2
    nilai_akhir = rapor * 0.60 + tka_avg * 0.40
    pg          = SEKOLAH_DATA[sekolah]["passing_grade_est"]
    selisih     = nilai_akhir - pg
    peluang     = 1 / (1 + math.exp(-selisih * 0.35)) * 100
    peluang     = round(min(peluang, 100), 1)
    return {
        "tka_avg"    : round(tka_avg, 2),
        "nilai_akhir": round(nilai_akhir, 2),
        "peluang"    : peluang,
        "selisih"    : round(selisih, 2),
        "pg"         : pg,
    }

def buat_saran_akademik(hasil, rapor, tka_mtk, tka_bindo, sekolah):
    na, pg, sel, p = hasil["nilai_akhir"], hasil["pg"], hasil["selisih"], hasil["peluang"]
    saran = []
    if p >= 80:
        saran.append("Nilai sangat kompetitif! Pertahankan performa ini hingga PPDB dibuka.")
        saran.append("Pastikan seluruh berkas rapor dan sertifikat TKA disiapkan lebih awal.")
    elif p >= 60:
        saran.append(f"Peluang baik, selisih dengan passing grade {sel:+.2f}.")
        if tka_mtk < tka_bindo:
            saran.append("Nilai TKA Matematika lebih rendah — fokus latihan soal Matematika.")
        else:
            saran.append("Nilai TKA B. Indonesia perlu ditingkatkan.")
    elif p >= 40:
        saran.append(f"Nilai akhir ({na:.2f}) masih di bawah estimasi passing grade ({pg}).")
        saran.append("Rekomendasi :\n  • Ikuti bimbel intensif untuk TKA.\n"
                     "  • Minta guru memperbaiki nilai rapor yang belum optimal.\n"
                     "  • Pertimbangkan sekolah dengan passing grade lebih rendah.")
    else:
        alts = [n for n, d in SEKOLAH_DATA.items()
                if n != sekolah and
                1 / (1 + math.exp(-(na - d["passing_grade_est"]) * 0.35)) * 100 >= 55][:2]
        saran.append("Peluang di sekolah ini rendah untuk jalur Prestasi Akademik.")
        if alts:
            saran.append("Alternatif sekolah :\n  • " + "\n  • ".join(alts))
        saran.append("Pertimbangkan jalur Domisili atau Afirmasi jika memenuhi syarat.")
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
            Ui.judul_section('Panduan Prestasi Akademik')
            ui.label(PANDUAN).classes('text-sm text-gray-300 whitespace-pre-line mb-4')

            Ui.judul_section('Pilih Sekolah Tujuan')
            sekolah_opts = list(SEKOLAH_DATA.keys())
            sekolah_select = ui.select(sekolah_opts, value=sekolah_opts[0], label='SMA/SMK Negeri').classes('w-full mb-1').props('dark outlined color="primary"')
            
            # Label info sekolah dinamis
            pg_label = ui.label().classes('text-sm text-[#FFD700] mb-4 font-semibold')
            def update_pg():
                sek = sekolah_select.value
                if sek:
                    pg_label.set_text(f"Est. Passing Grade: {SEKOLAH_DATA[sek]['passing_grade_est']}")
            sekolah_select.on('update:model-value', update_pg)
            update_pg() 

            Ui.judul_section('Nilai Rapor & TKA')
            rapor_input = ui.number(label='Rata-rata Rapor Smt 1-5 (0-100)', format='%.2f').classes('w-full mb-2').props('dark outlined color="primary"')
            tka_mtk_input = ui.number(label='TKA Matematika (0-100)', format='%.2f').classes('w-full mb-2').props('dark outlined color="primary"')
            tka_bindo_input = ui.number(label='TKA B. Indonesia (0-100)', format='%.2f').classes('w-full mb-6').props('dark outlined color="primary"')

            # --- FUNGSI TOMBOL ---
            def aksi_hitung():
                sekolah = sekolah_select.value
                rapor = rapor_input.value
                mtk = tka_mtk_input.value
                bindo = tka_bindo_input.value

                if rapor is None or mtk is None or bindo is None:
                    ui.notify('Harap isi semua nilai rapor dan TKA!', type='warning', position='top')
                    return
                if not (0 <= rapor <= 100) or not (0 <= mtk <= 100) or not (0 <= bindo <= 100):
                    ui.notify('Semua nilai harus berada di rentang 0 hingga 100.', type='negative', position='top')
                    return

                hasil = hitung_prestasi_akademik(rapor, mtk, bindo, sekolah)
                saran = buat_saran_akademik(hasil, rapor, mtk, bindo, sekolah)

                detail = [
                    ("Sekolah Tujuan", sekolah),
                    ("Rata-rata Rapor", f"{rapor:.2f}  (bobot 60%)"),
                    ("TKA Matematika", f"{mtk:.2f}"),
                    ("TKA Bahasa Indonesia", f"{bindo:.2f}"),
                    ("Rata-rata TKA", f"{hasil['tka_avg']:.2f}  (bobot 40%)"),
                    ("Nilai Akhir Kalkulasi", f"{hasil['nilai_akhir']:.2f}"),
                    ("Est. Passing Grade", f"{hasil['pg']:.1f}"),
                    ("Selisih", f"{hasil['selisih']:+.2f}"),
                ]

                # Render Hasil ke Kolom Kanan
                kanan.classes('justify-start items-stretch')
                Ui.render_hasil(
                    container=kanan,
                    peluang=hasil["peluang"],
                    nilai_akhir=hasil["nilai_akhir"],
                    passing_grade=hasil["pg"],
                    sekolah=sekolah,
                    jalur="Prestasi Akademik",
                    detail_rows=detail,
                    saran=saran
                )

                # Kotak Kontribusi Nilai Tambahan
                with kanan:
                    with ui.card().classes('w-full bg-[#1A2840] p-4 rounded-xl mt-4 border border-blue-800/50'):
                        ui.label('Kontribusi Komponen Nilai').classes('font-bold text-[#64FFDA] mb-2 text-sm border-b border-gray-700 pb-2')
                        
                        val_rapor = rapor * 0.6
                        val_tka = hasil['tka_avg'] * 0.4
                        total_val = val_rapor + val_tka
                        pct_rapor = (val_rapor / total_val * 100) if total_val else 0
                        pct_tka = (val_tka / total_val * 100) if total_val else 0

                        with ui.row().classes('w-full justify-between mt-2'):
                            ui.label('Rapor (60%)').classes('text-sm text-gray-400')
                            ui.label(f"{val_rapor:.2f}  ({pct_rapor:.1f}%)").classes('text-sm text-white font-mono font-bold')
                        with ui.row().classes('w-full justify-between mt-1'):
                            ui.label('TKA (40%)').classes('text-sm text-gray-400')
                            ui.label(f"{val_tka:.2f}  ({pct_tka:.1f}%)").classes('text-sm text-white font-mono font-bold')


            def aksi_reset():
                sekolah_select.value = sekolah_opts[0]
                rapor_input.value = None
                tka_mtk_input.value = None
                tka_bindo_input.value = None
                kanan.clear()
                kanan.classes('justify-center items-center')
                with kanan:
                    ui.label('Isi data di kiri lalu tekan Hitung').classes('text-gray-400 text-lg text-center')

            # --- TOMBOL ---
            with ui.row().classes('w-full gap-4 mt-2'):
                ui.button('Hitung', on_click=aksi_hitung).classes('flex-grow bg-[#64FFDA] text-[#0A192F] font-bold py-3 rounded-lg shadow-lg')
                ui.button('Reset', on_click=aksi_reset, color='red-500').classes('text-white font-bold py-3 rounded-lg')