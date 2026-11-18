
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LMS Fisika",
    page_icon="⚛️",
    layout="wide"
)

# Desain aplikasi
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}
[data-testid="stSidebar"] {
    background-color: #10243a;
}
[data-testid="stSidebar"] * {
    color: white;
}
.stButton button {
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Penyimpanan nilai sementara
if "nilai" not in st.session_state:
    st.session_state.nilai = []

# Sidebar
st.sidebar.title("⚛️ ASAS KONTINUIAS LMS")
st.sidebar.write("Learning Management System")

menu = st.sidebar.radio(
    "MENU UTAMA",
    [
        "Beranda",
        "Materi",
        "Video Pembelajaran",
        "Latihan Soal",
        "Tugas",
        "Nilai",
        "Tentang"
    ]
)

# BERANDA
if menu == "Beranda":
    st.title("Dashboard ASAS KONTINUITAS LMS")
    st.write("Selamat datang di platform pembelajaran fisika.")

    kolom1, kolom2, kolom3 = st.columns(3)

    kolom1.metric("Materi", "5")
    kolom2.metric("Latihan Soal", "3")
    kolom3.metric("Tugas", "0")

    st.subheader("Selamat Belajar!")
    st.info(
        "Gunakan ASAS KONTINUITAS LMS untuk mempelajari materi, "
        "mengerjakan latihan, dan melihat hasil belajar."
    )

# MATERI
elif menu == "Materi":
    st.title("Materi Pembelajaran")

    materi = {
        "Gerak Lurus":
            "Mempelajari posisi, perpindahan, kecepatan, dan percepatan.",
        "Hukum Newton":
            "Mempelajari hubungan gaya dan gerak benda.",
        "Fluida Statis":
            "Mempelajari tekanan hidrostatis dan hukum Archimedes.",
        "Asas Kontinuitas":
            "Mempelajari hubungan luas penampang dan kecepatan aliran.",
        "Hukum Bernoulli":
            "Mempelajari hubungan tekanan dan kecepatan fluida."
    }

    pilihan = st.selectbox(
        "Pilih materi fisika",
        list(materi.keys())
    )

    st.subheader(pilihan)
    st.write(materi[pilihan])

# VIDEO
elif menu == "Video Pembelajaran":
    st.title("Video Pembelajaran")

    link = st.text_input("Masukkan tautan video YouTube")

    if link:
        st.video(link)

# LATIHAN SOAL
elif menu == "Latihan Soal":
    st.title("Latihan Soal Fisika")

    soal = [
        {
            "pertanyaan": "Apa satuan SI untuk gaya?",
            "opsi": ["Joule", "Newton", "Watt", "Pascal"],
            "jawaban": "Newton"
        },
        {
            "pertanyaan": "Apa satuan SI untuk kecepatan?",
            "opsi": ["m/s", "m/s²", "Newton", "Joule"],
            "jawaban": "m/s"
        },
        {
            "pertanyaan": "Apa rumus tekanan hidrostatis?",
            "opsi": ["ρgh", "F/A", "m/v", "W/t"],
            "jawaban": "ρgh"
        }
    ]

    jawaban = []

    for i, s in enumerate(soal):
        st.write(f"**Soal {i+1}. {s['pertanyaan']}**")

        pilih = st.radio(
            "Pilih jawaban:",
            s["opsi"],
            key=f"soal_{i}"
        )

        jawaban.append(pilih)

    if st.button("Periksa Jawaban"):
        benar = 0

        for i, s in enumerate(soal):
            if jawaban[i] == s["jawaban"]:
                benar += 1
                st.success(f"Soal {i+1}: Jawaban benar!")
            else:
                st.error(
                    f"Soal {i+1}: Jawaban belum tepat. "
                    f"Jawaban benar: {s['jawaban']}"
                )

        skor = benar / len(soal) * 100
        st.session_state.nilai.append(skor)

        st.metric("Nilai Akhir", f"{skor:.0f}")

# TUGAS
elif menu == "Tugas":
    st.title("Pengumpulan Tugas")

    nama = st.text_input("Nama siswa")
    judul = st.text_input("Judul tugas")

    file = st.file_uploader(
        "Unggah tugas",
        type=["pdf", "docx", "jpg", "png"]
    )

    if st.button("Kumpulkan Tugas"):
        if nama and judul and file:
            st.success("File tugas berhasil dipilih.")
        else:
            st.warning("Lengkapi semua data terlebih dahulu.")

# NILAI
elif menu == "Nilai":
    st.title("Rekap Nilai Siswa")

    if st.session_state.nilai:
        df = pd.DataFrame({
            "Percobaan": range(
                1, len(st.session_state.nilai) + 1
            ),
            "Nilai": st.session_state.nilai
        })

        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada nilai latihan.")

# TENTANG
elif menu == "Tentang":
    st.title("Tentang LMS Fisika")

    st.write("""
    LMS Fisika merupakan platform pembelajaran digital
    yang dirancang untuk membantu guru dan peserta didik
    dalam kegiatan pembelajaran fisika.
    """)

    st.write("Dikembangkan menggunakan Python dan Streamlit.")
