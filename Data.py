#Satu-satunya file data untuk edit update data sekolah,
#kuota, bobot prestasi, atau tema warna.

#Tema Warna Aplikasi
WARNA = {
    "bg"        : "#0D1B2A",
    "panel"     : "#152238",
    "card"      : "#1E3050",
    "card2"     : "#243660",
    "border"    : "#2D4A6B",
    "accent"    : "#00C6FF",
    "accent2"   : "#FFD700",
    "success"   : "#22C55E",
    "danger"    : "#EF4444",
    "warning"   : "#F59E0B",
    "info"      : "#818CF8",
    "text"      : "#E2E8F0",
    "subtext"   : "#94A3B8",
    "header_bg" : "#0A1628",
    "hint"      : "#64748B",
}

#passing_grade_est : estimasi nilai minimum akhir untuk diterima
#jarak_max_m       : estimasi jarak terjauh (meter) yang masih diterima
SEKOLAH_DATA = {
    #SMA NEGERI
    "SMAN 1 Surabaya":  {"type":"SMA","akreditasi":"A","passing_grade_est":88,"jarak_max_m":1_200},
    "SMAN 2 Surabaya":  {"type":"SMA","akreditasi":"A","passing_grade_est":87,"jarak_max_m":1_500},
    "SMAN 5 Surabaya":  {"type":"SMA","akreditasi":"A","passing_grade_est":86,"jarak_max_m":1_800},
    "SMAN 6 Surabaya":  {"type":"SMA","akreditasi":"A","passing_grade_est":85,"jarak_max_m":2_000},
    "SMAN 7 Surabaya":  {"type":"SMA","akreditasi":"A","passing_grade_est":84,"jarak_max_m":2_200},
    "SMAN 9 Surabaya":  {"type":"SMA","akreditasi":"A","passing_grade_est":85,"jarak_max_m":2_000},
    "SMAN 11 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":83,"jarak_max_m":2_500},
    "SMAN 13 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":82,"jarak_max_m":2_800},
    "SMAN 15 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":81,"jarak_max_m":3_000},
    "SMAN 16 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":80,"jarak_max_m":3_200},
    "SMAN 17 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":79,"jarak_max_m":3_500},
    "SMAN 19 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":78,"jarak_max_m":3_800},
    "SMAN 20 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":77,"jarak_max_m":4_000},
    "SMAN 21 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":79,"jarak_max_m":3_500},
    "SMAN 22 Surabaya": {"type":"SMA","akreditasi":"A","passing_grade_est":76,"jarak_max_m":4_200},
    #SMK NEGERI
    "SMKN 1 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":82,"jarak_max_m":2_500},
    "SMKN 2 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":81,"jarak_max_m":2_800},
    "SMKN 3 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":80,"jarak_max_m":3_000},
    "SMKN 4 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":79,"jarak_max_m":3_200},
    "SMKN 5 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":80,"jarak_max_m":3_000},
    "SMKN 6 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":78,"jarak_max_m":3_500},
    "SMKN 7 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":77,"jarak_max_m":3_800},
    "SMKN 8 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":76,"jarak_max_m":4_000},
    "SMKN 9 Surabaya":  {"type":"SMK","akreditasi":"A","passing_grade_est":78,"jarak_max_m":3_500},
    "SMKN 10 Surabaya": {"type":"SMK","akreditasi":"A","passing_grade_est":75,"jarak_max_m":4_500},
    "SMKN 12 Surabaya": {"type":"SMK","akreditasi":"A","passing_grade_est":74,"jarak_max_m":5_000},
}

#Jalur & Kuota
JALUR_INFO = {
    "Domisili (Zonasi)"              : {"kuota":35,"desc":"Berdasarkan jarak tempat tinggal ke sekolah."},
    "Afirmasi"                       : {"kuota":30,"desc":"Keluarga tidak mampu, anak buruh, atau penyandang disabilitas."},
    "Prestasi Akademik (Rapor & TKA)": {"kuota":25,"desc":"Gabungan (60%) rata-rata rapor Sem 1–5 dan 40% nilai TKA."},
    "Prestasi Non-Akademik (Lomba)"  : {"kuota": 5,"desc":"Prestasi lomba akademik/non-akademik di luar nilai sekolah."},
    "Mutasi"                         : {"kuota": 5,"desc":"Calon murid yang orang tuanya pindah tugas kerja."},
}

#Bobot Prestasi Lomba
PRESTASI_BOBOT = {
    "Tidak Ada"             :  0,
    "Tingkat Sekolah"       :  2,
    "Tingkat Kecamatan"     :  4,
    "Tingkat Kabupaten/Kota":  7,
    "Tingkat Nasional"      : 12,
    "Tingkat Internasional" : 18,
}

#Bobot berdasarkan posisi juara
JUARA_BOBOT = {
    "Juara 1"         : 1.0,
    "Juara 2"         : 0.8,
    "Juara 3"         : 0.6,
    "Harapan 1"       : 0.4,
    "Harapan 2"       : 0.3,
    "Harapan 3"       : 0.2,
    "Peserta/Finalis" : 0.1,
}