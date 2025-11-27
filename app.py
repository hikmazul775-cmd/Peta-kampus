# =============================================
# FINAL - APLIKASI PETA DIGITAL LOKASI KAMPUS
# STREAMLIT + PYTHON (STABIL & BEBAS ERROR)
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
st.set_page_config(page_title="Peta Digital Lokasi Kampus", layout="wide")
st.title("📍 Aplikasi Peta Digital Lokasi Kampus")
st.write("Menampilkan peta interaktif lokasi gedung dan fasilitas kampus.")

# =============================================
# DATA DEFAULT
# =============================================
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
st.subheader("🗺️ Peta Kampus")

# fallback coordinates if df_filter empty
if df_filter.empty:
    # gunakan rata-rata seluruh dataset atau 0 jika juga kosong
    center_lat = df['lat'].mean() if not df.empty else 0
    center_lon = df['lon'].mean() if not df.empty else 0
else:
    center_lat = df_filter['lat'].mean()
    center_lon = df_filter['lon'].mean()

if folium_available:
    m = folium.Map(location=[center_lat, center_lon], zoom_start=17)

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
    # Perbaikan: gunakan satu string (tanpa memecah baris dengan tanda kutip yang belum ditutup)
    st.warning(
        "Folium belum terinstall. Menampilkan peta sederhana.\n"
        "Install dengan: pip install folium streamlit-folium"
    )
    # ubah nama kolom supaya st.map menerima latitude/longitude
    if not df_filter.empty:
        df_map = df_filter.rename(columns={"lat": "latitude", "lon": "longitude"})
        st.map(df_map[["latitude", "longitude"]])
    else:
        st.info("Tidak ada data lokasi untuk ditampilkan pada peta sederhana.")

# =============================================
# TABEL DATA
# =============================================
st.subheader("📊 Data Lokasi Kampus")
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

            # fallback center coords for uploaded file
            if df_upload.empty:
                up_center_lat = df['lat'].mean() if not df.empty else 0
                up_center_lon = df['lon'].mean() if not df.empty else 0
            else:
                up_center_lat = df_upload['lat'].mean()
                up_center_lon = df_upload['lon'].mean()

            if folium_available:
                m2 = folium.Map(location=[up_center_lat, up_center_lon], zoom_start=17)

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
    "Aplikasi Peta Digital Kampus - Streamlit Python (Final Version - Stabil)\n"
    "Pastikan folium sudah terinstall agar peta interaktif aktif."
)
