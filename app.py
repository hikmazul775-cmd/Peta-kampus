import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, HeatMap

# =============================
# KONFIGURASI HALAMAN
# =============================
st.set_page_config(page_title="Peta Digital Lokasi Kampus", layout="wide")

st.title("📍 Aplikasi Peta Digital Lokasi Kampus")
st.write("Aplikasi ini menampilkan peta interaktif lokasi gedung dan fasilitas kampus.")

# =============================
# DATA LOKASI KAMPUS (BISA DIGANTI CSV)
# =============================
# Jika ingin pakai file CSV, siapkan kolom: nama, lat, lon, kategori

data = {
    "nama": [
        "Rektorat",
        "Perpustakaan",
        "Gedung Teknik",
        "Gedung Ekonomi",
        "Masjid Kampus",
        "Lapangan Olahraga"
    ],
    "lat": [
        -5.147665,
        -5.148200,
        -5.149000,
        -5.147900,
        -5.146800,
        -5.150500
    ],
    "lon": [
        119.432731,
        119.431900,
        119.434200,
        119.430800,
        119.433500,
        119.435100
    ],
    "kategori": [
        "Administrasi",
        "Fasilitas",
        "Akademik",
        "Akademik",
        "Fasilitas",
        "Fasilitas"
    ]
}

df = pd.DataFrame(data)

# =============================
# FILTER KATEGORI
# =============================
st.sidebar.header("🎛️ Filter Lokasi")
kategori_pilihan = st.sidebar.multiselect(
    "Pilih kategori lokasi:",
    options=df['kategori'].unique(),
    default=df['kategori'].unique()
)

df_filter = df[df['kategori'].isin(kategori_pilihan)]

# =============================
# MEMBUAT PETA
# =============================
center_lat = df_filter['lat'].mean()
center_lon = df_filter['lon'].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=17, tiles="OpenStreetMap")

# Marker Cluster
marker_cluster = MarkerCluster().add_to(m)

for idx, row in df_filter.iterrows():
    popup_text = f"""
    <b>{row['nama']}</b><br>
    Kategori: {row['kategori']}<br>
    Koordinat: {row['lat']}, {row['lon']}
    """
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=popup_text,
        tooltip=row['nama'],
        icon=folium.Icon(icon="info-sign", color="blue")
    ).add_to(marker_cluster)

# Heatmap Opsional
if st.sidebar.checkbox("Tampilkan Heatmap"):
    heat_data = df_filter[["lat", "lon"]].values.tolist()
    HeatMap(heat_data).add_to(m)

# =============================
# TAMPILKAN PETA DI STREAMLIT
# =============================
st.subheader("🗺️ Peta Kampus Interaktif")
st_folium(m, width=900, height=600)

# =============================
# TABEL DATA
# =============================
st.subheader("📊 Data Lokasi Kampus")
st.dataframe(df_filter)

# =============================
# UPLOAD CSV
# =============================
st.subheader("📂 Upload Data CSV Lokasi Kampus")
uploaded_file = st.file_uploader("Upload file CSV", type="csv")

if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file)
    st.success("Data berhasil diupload!")
    st.dataframe(df_upload)

    m2 = folium.Map(
        location=[df_upload['lat'].mean(), df_upload['lon'].mean()],
        zoom_start=17
    )

    for idx, row in df_upload.iterrows():
        folium.Marker(
            [row['lat'], row['lon']],
            popup=row['nama'],
            tooltip=row['nama']
        ).add_to(m2)

    st.subheader("🗺️ Peta dari File CSV")
    st_folium(m2, width=900, height=600)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("Dibuat untuk tugas: Aplikasi Peta Digital Lokasi Kampus menggunakan Streamlit & Python")
