import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import os

st.set_page_config(
    page_title="Peta UMKM Sulawesi Barat",
    layout="wide"
)

st.title("🗺️ Peta Digital Lokasi UMKM di Sulawesi Barat")
st.markdown(
    """
Aplikasi ini menampilkan peta lokasi UMKM di Provinsi **Sulawesi Barat**.  
Data bisa kamu ambil dari **Google Maps** (nama UMKM, alamat, latitude, dan longitude), lalu dimasukkan ke file CSV.

**Fitur:**
- Filter berdasarkan **kabupaten** dan **kategori UMKM**  
- Pencarian berdasarkan **nama UMKM**  
- Peta interaktif (zoom, drag)  
- Tabel data UMKM  
- Visualisasi jumlah UMKM per kabupaten / kategori
"""
)

# =========================
# Fungsi untuk load data
# =========================
@st.cache_data
def load_data(csv_path: str) -> pd.DataFrame:
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # fallback: contoh data jika file belum ada
        df = pd.DataFrame({
            "nama_umkm": [
                "Warung Makan Sederhana", "Toko Kue Manis", "Butik Muslimah Cantik",
                "Toko Sembako Murah", "Kedai Kopi Santai", "Toko Oleh-Oleh Sulbar"
            ],
            "kategori": [
                "Kuliner", "Kuliner", "Fashion",
                "Sembako", "Kuliner", "Kerajinan"
            ],
            "kabupaten": [
                "Polewali Mandar", "Polewali Mandar", "Mamuju",
                "Mamuju", "Majene", "Majene"
            ],
            "alamat": [
                "Jl. Poros Polman No. 1",
                "Jl. Jenderal Sudirman No. 12",
                "Jl. Ahmad Yani No. 8",
                "Jl. Trans Sulawesi KM 5",
                "Jl. Pelabuhan Majene",
                "Jl. Diponegoro No. 3"
            ],
            "lat": [-3.4321, -3.4455, -2.6744, -2.6901, -3.5378, -3.5222],
            "lon": [119.3432, 119.3655, 118.8877, 118.9012, 118.9734, 118.9659],
        })
    return df


# =========================
# Sidebar: Upload & Filter
# =========================
st.sidebar.header("⚙️ Pengaturan & Filter")

uploaded_file = st.sidebar.file_uploader(
    "Upload data UMKM (CSV)",
    type=["csv"],
    help="Format kolom minimal: nama_umkm, kategori, kabupaten, alamat, lat, lon"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data("data_umkm_sulbar.csv")

# Pastikan kolom yang dibutuhkan ada
required_cols = ["nama_umkm", "kategori", "kabupaten", "alamat", "lat", "lon"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"Kolom berikut belum ada di data: {missing_cols}")
    st.stop()

# Bersihkan data
df = df.dropna(subset=["lat", "lon"])

# Filter kabupaten
kabupaten_options = ["Semua"] + sorted(df["kabupaten"].dropna().unique().tolist())
selected_kab = st.sidebar.selectbox("Pilih Kabupaten", kabupaten_options)

# Filter kategori
kategori_options = ["Semua"] + sorted(df["kategori"].dropna().unique().tolist())
selected_kat = st.sidebar.selectbox("Pilih Kategori UMKM", kategori_options)

# Filter nama (search)
search_name = st.sidebar.text_input("Cari Nama UMKM (opsional)", "")

# Terapkan filter
filtered_df = df.copy()

if selected_kab != "Semua":
    filtered_df = filtered_df[filtered_df["kabupaten"] == selected_kab]

if selected_kat != "Semua":
    filtered_df = filtered_df[filtered_df["kategori"] == selected_kat]

if search_name:
    filtered_df = filtered_df[
        filtered_df["nama_umkm"].str.contains(search_name, case=False, na=False)
    ]

st.markdown(f"### 🔍 Hasil Filter: {len(filtered_df)} UMKM ditemukan")

# =========================
# Peta Folium
# =========================
if not filtered_df.empty:
    mean_lat = filtered_df["lat"].mean()
    mean_lon = filtered_df["lon"].mean()
else:
    mean_lat = df["lat"].mean()
    mean_lon = df["lon"].mean()

m = folium.Map(location=[mean_lat, mean_lon], zoom_start=8, control_scale=True)

# Tambahkan marker untuk setiap UMKM
for _, row in filtered_df.iterrows():
    popup_html = f"""
    <b>{row['nama_umkm']}</b><br>
    Kategori: {row['kategori']}<br>
    Kabupaten: {row['kabupaten']}<br>
    Alamat: {row['alamat']}
    """
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=popup_html,
        tooltip=row["nama_umkm"]
    ).add_to(m)

# Tampilkan peta di Streamlit
st.subheader("🗺️ Peta Lokasi UMKM")
st_data = st_folium(m, width="100%", height=500)

# =========================
# Tabel Data UMKM
# =========================
st.subheader("📋 Tabel Data UMKM (sesuai filter)")
st.dataframe(filtered_df.reset_index(drop=True))

# =========================
# Visualisasi Data (statistik)
# =========================
st.subheader("📊 Visualisasi Data UMKM")

tab1, tab2 = st.tabs(["Jumlah per Kabupaten", "Jumlah per Kategori"])

with tab1:
    counts_kab = df.groupby("kabupaten")["nama_umkm"].count().reset_index()
    counts_kab.columns = ["kabupaten", "jumlah_umkm"]
    fig1 = plotly.express.bar(
        counts_kab,
        x="kabupaten",
        y="jumlah_umkm",
        title="Jumlah UMKM per Kabupaten"
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    counts_kat = df.groupby("kategori")["nama_umkm"].count().reset_index()
    counts_kat.columns = ["kategori", "jumlah_umkm"]
    fig2 = plotly.express.bar(
        counts_kat,
        x="kategori",
        y="jumlah_umkm",
        title="Jumlah UMKM per Kategori"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.info(
    """
💡 **Tips: Cara isi data dari Google Maps**
1. Buka Google Maps → cari nama UMKM  
2. Klik kanan di lokasi → pilih "Apa ini di sini?" → salin **koordinat (lat, lon)**  
3. Masukkan ke file **CSV** dengan kolom: `nama_umkm, kategori, kabupaten, alamat, lat, lon`  
4. Upload CSV tersebut lewat sidebar atau simpan sebagai `data_umkm_sulbar.csv`.
"""
)
