
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LMS Fisika",
    page_icon="⚛️",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
[data-testid="stSidebar"] {
    background-color: #10243a;
}
[data-testid="stSidebar"] * {
    color: white;
}
.stButton button {
    border-radius: 9px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

if "nilai" not in st.session_state:
    st.session_state.nilai = []

st.sidebar.title("⚛️ LMS FISIKA")
st.sidebar.caption("Learning Management System")

menu = st.sidebar.radio(
    "MENU PEMBELAJARAN",
    [
        "Beranda",
        "Materi",
        "Video",
        "Latihan Soal",
        "Tugas",
        "Nilai",
        "Tentang"
    ]
)

if menu == "Beranda":
    st.title("Dashboard LMS Fisika")
    st.write("Selamat datang di platform pembelajaran fisika.")

    a, b, c = st.columns(3)
    a.metric("Materi", "5")
    b.metric("Latihan", "1")
    c.metric("Tugas", "0")

    st.subheader("Selamat Belajar!")
    st.info(
        "Pelajari materi, kerjakan latihan, "
        "dan lihat hasil pembelajaranmu."
    )

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
        "Pilih materi",
        list(materi.keys())
    )

    st.subheader(pilihan)
    st.write(materi[pilihan])

elif menu == "Video":
    st.title("Video Pembelajaran")
    link = st.text_input("Masukkan link video YouTube")

    if link:
        st.video(link)

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
                st.success(f"Soal {i+1}: Benar")
            else:
                st.error(
                    f"Soal {i+1}: Belum tepat. "
                    f"Jawaban benar: {s['jawaban']}"
                )

        skor = benar / len(soal) * 100
        st.session_state.nilai.append(skor)
        st.metric("Nilai Akhir", f"{skor:.0f}")

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
            st.success("Data tugas siap dikumpulkan.")
        else:
            st.warning("Lengkapi semua data terlebih dahulu.")

elif menu == "Nilai":
    st.title("Rekap Nilai")

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

elif menu == "Tentang":
    st.title("Tentang LMS Fisika")
    st.write(
        "LMS Fisika merupakan platform pembelajaran "
        "digital untuk mendukung kegiatan belajar fisika."
    )
    st.write("Dikembangkan menggunakan Python dan Streamlit.")
