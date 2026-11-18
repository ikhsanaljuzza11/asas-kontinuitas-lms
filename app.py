
import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="LMS Fisika",
    page_icon="⚛️",
    layout="wide"
)

# KONEKSI DATABASE
@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

try:
    db = get_supabase()
except Exception as e:
    st.error("Koneksi database belum tersedia.")
    st.stop()

# DESAIN
st.markdown("""
<style>
.stApp {
    background: #f5f7fb;
}
[data-testid="stSidebar"] {
    background: #10243a;
}
[data-testid="stSidebar"] * {
    color: white;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

if "profile" not in st.session_state:
    st.session_state.profile = None

# FUNGSI LOGIN
def login(email, password):
    try:
        result = db.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = result.user

        profile = (
            db.table("profiles")
            .select("*")
            .eq("id", user.id)
            .single()
            .execute()
        )

        st.session_state.user = user
        st.session_state.profile = profile.data
        st.rerun()

    except Exception:
        st.error("Email atau password salah, atau akun belum aktif.")

# FUNGSI DAFTAR
def register(name, email, password):
    try:
        result = db.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "display_name": name
                }
            }
        })

        st.success(
            "Pendaftaran berhasil. "
            "Periksa email untuk verifikasi akun jika diminta."
        )

    except Exception:
        st.error("Pendaftaran gagal. Periksa email dan password.")

# HALAMAN BELUM LOGIN
if st.session_state.user is None:

    st.title("⚛️ LMS FISIKA")
    st.caption("Interactive Science & STEM Learning")

    tab1, tab2 = st.tabs(["Login", "Daftar Akun"])

    with tab1:
        st.subheader("Masuk ke LMS")

        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Masuk", use_container_width=True):
            if email and password:
                login(email, password)
            else:
                st.warning("Isi email dan password.")

    with tab2:
        st.subheader("Registrasi Peserta Didik")

        name = st.text_input("Nama tampilan", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input(
            "Password",
            type="password",
            key="reg_password"
        )

        if st.button("Daftar", use_container_width=True):
            if name and email and len(password) >= 8:
                register(name, email, password)
            else:
                st.warning(
                    "Isi seluruh data. Password minimal 8 karakter."
                )

    st.stop()

# PROFIL
profile = st.session_state.profile
nama = profile["display_name"]
role = profile["role"]

# SIDEBAR
st.sidebar.title("⚛️ LMS FISIKA")
st.sidebar.write(f"Pengguna: {nama}")
st.sidebar.write(f"Hak akses: {role.upper()}")

if role == "admin":
    menu_list = [
        "Dashboard Admin",
        "Manajemen Kelas",
        "Pengguna",
        "Laporan"
    ]

elif role == "guru":
    menu_list = [
        "Dashboard Guru",
        "Materi",
        "Aktivitas",
        "Diskusi",
        "Penilaian",
        "Eksperimen",
        "Laporan"
    ]

else:
    menu_list = [
        "Dashboard Siswa",
        "Materi",
        "Diagnostik",
        "Pretest",
        "Aktivitas Belajar",
        "Laboratorium",
        "Diskusi",
        "Nilai",
        "Portofolio"
    ]

menu = st.sidebar.radio("MENU", menu_list)

if st.sidebar.button("Keluar"):
    db.auth.sign_out()
    st.session_state.user = None
    st.session_state.profile = None
    st.rerun()

# DASHBOARD ADMIN
if menu == "Dashboard Admin":
    st.title("Dashboard Administrator")
    st.info("Kelola pengguna, kelas, dan sistem LMS.")

    st.write("Hak akses administrator.")
    st.write("Manajemen data akan dikembangkan pada tahap berikutnya.")

# DASHBOARD GURU
elif menu == "Dashboard Guru":
    st.title("Dashboard Guru")
    st.write(f"Selamat datang, {nama}.")

    st.info(
        "Guru dapat mengelola materi, aktivitas, "
        "diskusi, eksperimen, dan penilaian."
    )

# DASHBOARD SISWA
elif menu == "Dashboard Siswa":
    st.title("Dashboard Peserta Didik")
    st.write(f"Selamat belajar, {nama}!")

    st.info(
        "Ikuti pembelajaran mulai dari diagnostik, "
        "pretest, aktivitas, hingga refleksi."
    )

# MATERI
elif menu == "Materi":
    st.title("Materi Pembelajaran")

    try:
        result = (
            db.table("materials")
            .select("*")
            .execute()
        )

        if result.data:
            for item in result.data:
                with st.expander(item["title"]):
                    st.write(item.get("description") or "")
                    st.write(item.get("content") or "")

                    if item.get("video_url"):
                        st.video(item["video_url"])

                    if item.get("pdf_url"):
                        st.link_button(
                            "Buka PDF",
                            item["pdf_url"]
                        )
        else:
            st.info("Belum ada materi yang diterbitkan.")

    except Exception:
        st.error("Materi belum dapat dimuat.")

# DISKUSI
elif menu == "Diskusi":
    st.title("Forum Diskusi Fisika")

    judul = st.text_input("Judul diskusi")
    pesan = st.text_area("Tulis pendapat atau pertanyaan")

    if st.button("Kirim Diskusi"):
        if judul and pesan:
            try:
                db.table("discussions").insert({
                    "user_id": st.session_state.user.id,
                    "title": judul,
                    "message": pesan
                }).execute()

                st.success("Diskusi berhasil dikirim.")
                st.rerun()

            except Exception:
                st.error(
                    "Diskusi belum dapat dikirim. "
                    "Pastikan pengguna sudah terdaftar dalam kelas."
                )

    try:
        result = (
            db.table("discussions")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        for item in result.data:
            with st.container(border=True):
                st.subheader(item["title"])
                st.write(item["message"])
                st.caption(item["created_at"])

    except Exception:
        st.warning("Forum belum dapat dimuat.")

# NILAI
elif menu == "Nilai":
    st.title("Hasil Pembelajaran")

    try:
        result = (
            db.table("assessments")
            .select("*")
            .eq("student_id", st.session_state.user.id)
            .execute()
        )

        if result.data:
            st.dataframe(
                result.data,
                use_container_width=True
            )
        else:
            st.info("Belum ada hasil penilaian.")

    except Exception:
        st.error("Nilai belum dapat dimuat.")

# HALAMAN PENGEMBANGAN
else:
    st.title(menu)
    st.info(
        "Modul ini akan diaktifkan pada tahap "
        "pengembangan berikutnya."
    )
