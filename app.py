# =============================================
# FINAL - APLIKASI PETA DIGITAL KAMPUS UNSA
# STREAMLIT + PYTHON (STABIL)
# =============================================
# Cara menjalankan:
# 1. pip install streamlit pandas folium streamlit-folium
# 2. streamlit run app.py
# =============================================

import streamlit as st
import pandas as pd

# Cek ketersediaan folium
folium_available = True
try:
    import folium
    from folium.plugins import MarkerCluster, HeatMap
    from streamlit_folium import st_folium
except Exception:
    folium_available = False

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(page_title="Peta Digital Kampus UNSA", layout="wide")
st.title("📍 Aplikasi Peta Digital Kampus Universitas Al Asyariah Mandar")
st.write("Menampilkan peta interaktif lokasi gedung dan fasilitas Kampus UNSA.")

# =============================================
# DATA DEFAULT - TITIK LOKASI DI KAMPUS UNSA
# (Simulasi posisi sekitar koordinat kampus)
# =============================================
data = {
    "nama": [
        "Rektorat",
        "Perpustakaan",
        "Gedung Fakultas Kesehatan",
        "Gedung Fakultas Teknik",
        "Masjid Kampus",
        "Lapangan Olahraga"
    ],
    "lat": [
        -3.404352,     # Rektorat
        -3.404150,     # Perpustakaan
        -3.404700,     # Fikes
        -3.403900,     # Fakultas Teknik
        -3.404500,     # Masjid
        -3.403600      # Lapangan
    ],
    "lon": [
        119.305593,    # Rektorat
        119.305800,    # Perpustakaan
        119.305300,    # Fikes
        119.306000,    # Fakultas Teknik
        119.305450,    # Masjid
        119.306200     # Lapangan
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

# =============================================
# SIDEBAR FILTER
# =============================================
st.sidebar.header("🎛️ Filter Lokasi")
kategori_pilihan = st.sidebar.multiselect(
    "Pilih kategori:",
    options=df['kategori'].unique(),
    default=df['kategori'].unique()
)

df_filter = df[df['kategori'].isin(kategori_pilihan)]

# =============================================
# TAMPILAN PETA
# =============================================
st.subheader("🗺️ Peta Kampus UNSA")

# fallback coordinates (menggunakan koordinat UNSA)
center_lat = -3.404352
center_lon = 119.305593

if folium_available:
    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    cluster = MarkerCluster().add_to(m)

    for _, row in df_filter.iterrows():
        popup = f"""
        <b>{row['nama']}</b><br>
        Kategori: {row['kategori']}<br>
        Koordinat: {row['lat']}, {row['lon']}
        """
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=popup,
            tooltip=row['nama'],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(cluster)

    if st.sidebar.checkbox("Tampilkan Heatmap"):
        heat_data = df_filter[["lat", "lon"]].values.tolist()
        if heat_data:
            HeatMap(heat_data).add_to(m)

    st_folium(m, width=900, height=600)

else:
    st.warning(
        "Folium belum terinstall. Menampilkan peta sederhana.\n"
        "Install dengan: pip install folium streamlit-folium"
    )
    if not df_filter.empty:
        df_map = df_filter.rename(columns={"lat": "latitude", "lon": "longitude"})
        st.map(df_map[["latitude", "longitude"]])
    else:
        st.info("Tidak ada data lokasi untuk ditampilkan pada peta sederhana.")

# =============================================
# TABEL DATA
# =============================================
st.subheader("📊 Data Lokasi Kampus UNSA")
st.dataframe(df_filter)

# =============================================
# UPLOAD CSV
# =============================================
st.subheader("📂 Upload File CSV")
uploaded_file = st.file_uploader("Upload CSV (nama, lat, lon, kategori)", type="csv")

if uploaded_file is not None:
    try:
        df_upload = pd.read_csv(uploaded_file)
        st.success("File berhasil diupload!")

        if not {'nama', 'lat', 'lon'}.issubset(df_upload.columns):
            st.error("CSV wajib memiliki kolom: nama, lat, lon")
        else:
            st.dataframe(df_upload)

            up_center_lat = df_upload['lat'].mean() if not df_upload.empty else center_lat
            up_center_lon = df_upload['lon'].mean() if not df_upload.empty else center_lon

            if folium_available:
                m2 = folium.Map(location=[up_center_lat, up_center_lon], zoom_start=18)

                for _, row in df_upload.iterrows():
                    folium.Marker(
                        location=[row['lat'], row['lon']],
                        popup=row['nama'],
                        tooltip=row['nama']
                    ).add_to(m2)

                st.subheader("🗺️ Peta dari CSV")
                st_folium(m2, width=900, height=600)
            else:
                df_map2 = df_upload.rename(columns={"lat": "latitude", "lon": "longitude"})
                if not df_map2.empty:
                    st.map(df_map2[["latitude", "longitude"]])
                else:
                    st.info("CSV kosong, tidak ada data peta untuk ditampilkan.")

    except Exception as e:
        st.error("Gagal membaca file CSV")
        st.write(e)

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.caption(
    "Aplikasi Peta Digital Kampus UNSA - Streamlit Python (Final Version)\n"
    "Pastikan folium sudah terinstall agar peta interaktif aktif."
)
