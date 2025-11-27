import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ======================
# KONFIGURASI STREAMLIT
# ======================
st.set_page_config(page_title="Peta UMKM Sulawesi Barat", layout="wide")
st.title("🗺️ Peta Digital Lokasi UMKM di Sulawesi Barat")

st.markdown("""
Aplikasi ini menampilkan lokasi UMKM di Provinsi **Sulawesi Barat** menggunakan peta interaktif.  
Anda bisa melakukan filter berdasarkan **kabupaten** & **kategori UMKM**.
""")

# ======================
# DATA UMKM SIAP PAKAI
# ======================
data = {
    "nama_umkm": [
        "Warung Makan Sederhana", "Toko Kue Manis", "Butik Muslimah Cantik",
        "Toko Sembako Murah", "Kedai Kopi Santai", "Toko Oleh-Oleh Sulbar",
        "Bengkel Motor Jaya", "Laundry Bersih Selalu", "Rumah Makan Laut Segar",
        "Toko Elektronik Maju Tech"
    ],
    "kategori": [
        "Kuliner", "Kuliner", "Fashion",
        "Sembako", "Kuliner", "Kerajinan",
        "Otomotif", "Jasa", "Kuliner", "Elektronik"
    ],
    "kabupaten": [
        "Polewali Mandar", "Polewali Mandar", "Mamuju",
        "Mamuju", "Majene", "Majene",
        "Polewali Mandar", "Mamuju Tengah", "Mamuju", "Pasangkayu"
    ],
    "alamat": [
        "Jl. Poros Polman No. 1", "Jl. Jenderal Sudirman 12", "Jl. Ahmad Yani 8",
        "Jl. Trans Sulawesi KM 5", "Jl. Pelabuhan Majene", "Jl. Diponegoro 3",
        "Jl. Poros Wonomulyo", "Jl. Poros Topoyo", "Jl. Pantai Mamuju",
        "Jl. Hasanuddin Pasangkayu"
    ],
    "lat": [-3.4321, -3.4455, -2.6744, -2.6901, -3.5378, -3.5222, -3.4655, -2.7166, -2.6749, -1.1902],
    "lon": [119.3432, 119.3655, 118.8877, 118.9012, 118.9734, 118.9659, 119.3111, 119.0134, 118.8966, 119.3621]
}

df = pd.DataFrame(data)

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter Data")

kab_opts = ["Semua"] + sorted(df["kabupaten"].unique())
kat_opts = ["Semua"] + sorted(df["kategori"].unique())

pilih_kab = st.sidebar.selectbox("Pilih Kabupaten", kab_opts)
pilih_kat = st.sidebar.selectbox("Pilih Kategori UMKM", kat_opts)

filtered = df.copy()

if pilih_kab != "Semua":
    filtered = filtered[filtered["kabupaten"] == pilih_kab]

if pilih_kat != "Semua":
    filtered = filtered[filtered["kategori"] == pilih_kat]

st.write(f"### 🔍 Total UMKM ditemukan: {len(filtered)}")

# ======================
# PETA FOLIUM
# ======================
# Titik tengah peta rata-rata semua titik
mid_lat = filtered["lat"].mean()
mid_lon = filtered["lon"].mean()

m = folium.Map(location=[mid_lat, mid_lon], zoom_start=8)

# Tambahkan marker ke peta
for _, row in filtered.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]],
        tooltip=row["nama_umkm"],
        popup=f"""
        <b>{row['nama_umkm']}</b><br>
        Kategori: {row['kategori']}<br>
        Kabupaten: {row['kabupaten']}<br>
        Alamat: {row['alamat']}
        """
    ).add_to(m)

st.subheader("🗺️ Peta Lokasi UMKM")
st_folium(m, width=900, height=500)

# ======================
# TABEL DATA
# ======================
st.subheader("📋 Tabel Data UMKM")
st.dataframe(filtered)
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ======================
# KONFIGURASI STREAMLIT
# ======================
st.set_page_config(page_title="Peta UMKM Sulawesi Barat", layout="wide")
st.title("🗺️ Peta Digital Lokasi UMKM di Sulawesi Barat")

st.markdown("""
Aplikasi ini menampilkan lokasi UMKM di Provinsi **Sulawesi Barat** menggunakan peta interaktif.  
Anda bisa melakukan filter berdasarkan **kabupaten** & **kategori UMKM**.
""")

# ======================
# DATA UMKM SIAP PAKAI
# ======================
data = {
    "nama_umkm": [
        "Warung Makan Sederhana", "Toko Kue Manis", "Butik Muslimah Cantik",
        "Toko Sembako Murah", "Kedai Kopi Santai", "Toko Oleh-Oleh Sulbar",
        "Bengkel Motor Jaya", "Laundry Bersih Selalu", "Rumah Makan Laut Segar",
        "Toko Elektronik Maju Tech"
    ],
    "kategori": [
        "Kuliner", "Kuliner", "Fashion",
        "Sembako", "Kuliner", "Kerajinan",
        "Otomotif", "Jasa", "Kuliner", "Elektronik"
    ],
    "kabupaten": [
        "Polewali Mandar", "Polewali Mandar", "Mamuju",
        "Mamuju", "Majene", "Majene",
        "Polewali Mandar", "Mamuju Tengah", "Mamuju", "Pasangkayu"
    ],
    "alamat": [
        "Jl. Poros Polman No. 1", "Jl. Jenderal Sudirman 12", "Jl. Ahmad Yani 8",
        "Jl. Trans Sulawesi KM 5", "Jl. Pelabuhan Majene", "Jl. Diponegoro 3",
        "Jl. Poros Wonomulyo", "Jl. Poros Topoyo", "Jl. Pantai Mamuju",
        "Jl. Hasanuddin Pasangkayu"
    ],
    "lat": [-3.4321, -3.4455, -2.6744, -2.6901, -3.5378, -3.5222, -3.4655, -2.7166, -2.6749, -1.1902],
    "lon": [119.3432, 119.3655, 118.8877, 118.9012, 118.9734, 118.9659, 119.3111, 119.0134, 118.8966, 119.3621]
}

df = pd.DataFrame(data)

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter Data")

kab_opts = ["Semua"] + sorted(df["kabupaten"].unique())
kat_opts = ["Semua"] + sorted(df["kategori"].unique())

pilih_kab = st.sidebar.selectbox("Pilih Kabupaten", kab_opts)
pilih_kat = st.sidebar.selectbox("Pilih Kategori UMKM", kat_opts)

filtered = df.copy()

if pilih_kab != "Semua":
    filtered = filtered[filtered["kabupaten"] == pilih_kab]

if pilih_kat != "Semua":
    filtered = filtered[filtered["kategori"] == pilih_kat]

st.write(f"### 🔍 Total UMKM ditemukan: {len(filtered)}")

# ======================
# PETA FOLIUM
# ======================
# Titik tengah peta rata-rata semua titik
mid_lat = filtered["lat"].mean()
mid_lon = filtered["lon"].mean()

m = folium.Map(location=[mid_lat, mid_lon], zoom_start=8)

# Tambahkan marker ke peta
for _, row in filtered.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]],
        tooltip=row["nama_umkm"],
        popup=f"""
        <b>{row['nama_umkm']}</b><br>
        Kategori: {row['kategori']}<br>
        Kabupaten: {row['kabupaten']}<br>
        Alamat: {row['alamat']}
        """
    ).add_to(m)

st.subheader("🗺️ Peta Lokasi UMKM")
st_folium(m, width=900, height=500)

# ======================
# TABEL DATA
# ======================
st.subheader("📋 Tabel Data UMKM")
st.dataframe(filtered)
