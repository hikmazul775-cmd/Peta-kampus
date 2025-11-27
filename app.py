# =============================================
# FINAL - PETA DIGITAL KAMPUS SE-SULAWESI BARAT
# STREAMLIT + PYTHON
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
st.set_page_config(page_title="Peta Kampus Sulawesi Barat", layout="wide")
st.title("📍 Peta Digital Kampus di Provinsi Sulawesi Barat")
st.write("Menampilkan peta interaktif berbagai kampus dan perguruan tinggi di seluruh Sulawesi Barat.")

# =============================================
# DATA KAMPUS SELURUH SULBAR
# =============================================
data = {
    "nama": [
        "Universitas Sulawesi Barat (Unsulbar)",
        "Universitas Al Asyariah Mandar (UNSA)",
        "Institut Agama Islam DDI Polman",
        "Universitas Tomakaka (Untika) Mamuju",
        "STIE Muhammadiyah Mamuju",
        "Politeknik Negeri Mamuju",
        "STIKES Bina Generasi Polewali",
        "STKIP Parman Majene",
        "STIP YAPI Polman"
    ],
    "lat": [
        -3.540200,   # Unsulbar Majene
        -3.404352,   # UNSA Polman
        -3.459800,   # IAI DDI Polman
        -2.680180,   # Untika Mamuju
        -2.672700,   # STIE Muhammadiyah
        -2.647550,   # Politeknik Negeri Mamuju
        -3.432500,   # STIKES Bina Generasi
        -3.540700,   # STKIP Parman
        -3.432100    # STIP YAPI Polman
    ],
    "lon": [
        118.970500,  # Unsulbar Majene
        119.305593,  # UNSA Polman
        119.326800,  # IAI DDI Polman
        118.885890,  # Untika Mamuju
        118.898700,  # STIE Muhammadiyah
        118.884200,  # Politeknik Mamuju
        119.354300,  # STIKES Bina Generasi
        118.977000,  # STKIP Parman
        119.348900   # STIP YAPI Polman
    ],
    "kategori": [
        "Universitas",
        "Universitas",
        "Institut",
        "Universitas",
        "Sekolah Tinggi",
        "Politeknik",
        "Sekolah Tinggi",
        "Sekolah Tinggi",
        "Sekolah Tinggi"
    ]
}

df = pd.DataFrame(data)

# =============================================
# SIDEBAR FILTER
# =============================================
st.sidebar.header("🎛️ Filter Lokasi Kampus")
kategori_pilihan = st.sidebar.multiselect(
    "Pilih kategori perguruan tinggi:",
    options=df['kategori'].unique(),
    default=df['kategori'].unique()
)

df_filter = df[df['kategori'].isin(kategori_pilihan)]

# =============================================
# TAMPILAN PETA (CENTER = TENGAH SULBAR)
# =============================================
st.subheader("🗺️ Peta Kampus di Sulawesi Barat")

center_lat = -3.2
center_lon = 119.1

if folium_available:
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9)

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
            icon=folium.Icon(color="blue", icon="university")
        ).add_to(cluster)

    if st.sidebar.checkbox("Tampilkan Heatmap"):
        heat_data = df_filter[["lat", "lon"]].values.tolist()
        HeatMap(heat_data).add_to(m)

    st_folium(m, width=900, height=600)

else:
    st.warning("Folium tidak tersedia. Menggunakan tampilan peta default Streamlit.")
    df_map = df_filter.rename(columns={"lat": "latitude", "lon": "longitude"})
    st.map(df_map[["latitude", "longitude"]])

# =============================================
# TABEL DATA
# =============================================
st.subheader("📊 Daftar Kampus di Sulawesi Barat")
st.dataframe(df_filter)

# =============================================
# UPLOAD CSV
# =============================================
st.subheader("📂 Upload File CSV")
uploaded_file = st.file_uploader("Upload CSV (nama, lat, lon, kategori)", type="csv")

if uploaded_file is not None:
    try:
        df_upload = pd.read_csv(uploaded_file)
        st.success("Upload berhasil!")

        if not {'nama', 'lat', 'lon'}.issubset(df_upload.columns):
            st.error("CSV wajib memiliki kolom: nama, lat, lon")
        else:
            st.dataframe(df_upload)

            avg_lat = df_upload['lat'].mean()
            avg_lon = df_upload['lon'].mean()

            if folium_available:
                m2 = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

                for _, row in df_upload.iterrows():
                    folium.Marker(
                        location=[row['lat'], row['lon']],
                        popup=row['nama'],
                        tooltip=row['nama']
                    ).add_to(m2)

                st.subheader("🗺️ Peta dari CSV")
                st_folium(m2, width=900, height=600)

    except Exception as e:
        st.error("Gagal membaca CSV!")
        st.write(e)

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.caption("Peta Digital Kampus Sulawesi Barat · Streamlit + Python")
