"""
Aplikasi Peta Digital Lokasi Kampus (Streamlit + Python) — V2 (Perbaikan import & fallback)

Perubahan / perbaikan:
- Menangani masalah ModuleNotFoundError pada saat import folium / streamlit_folium dengan pesan instruktif.
- Menyediakan fallback visualisasi (st.map / pydeck) jika folium tidak tersedia.
- Menambahkan pengecekan format CSV saat upload.
- Menambahkan contoh requirements.txt di komentar untuk deployment ke Streamlit Cloud / Replit.

PETUNJUK SINGKAT:
- Jika Anda melihat error ModuleNotFoundError untuk `folium` atau `streamlit_folium`, jalankan:
    pip install folium streamlit-folium

- Untuk deploy ke Streamlit Cloud, buat file `requirements.txt` berisi (contoh):
    streamlit
    pandas
    folium
    streamlit-folium

- Simpan file ini sebagai `app.py` dan jalankan:
    streamlit run app.py

"""

import streamlit as st
import pandas as pd

# Coba import folium dan streamlit_folium, jika gagal tampilkan instruksi
have_folium = True
try:
    import folium
    from folium.plugins import MarkerCluster, HeatMap
    from streamlit_folium import st_folium
except Exception as e:
    have_folium = False
    _folium_error = str(e)

st.set_page_config(page_title="Peta Digital Lokasi Kampus", layout="wide")
st.title("📍 Aplikasi Peta Digital Lokasi Kampus")
st.write("Jika peta tidak muncul, ikuti petunjuk perbaikan yang ada di bawah.")

# Data contoh
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

# Sidebar filter
st.sidebar.header("🎛️ Filter Lokasi")
if not df.empty:
    kategori_pilihan = st.sidebar.multiselect(
        "Pilih kategori lokasi:",
        options=df['kategori'].unique(),
        default=df['kategori'].unique()
    )
    df_filter = df[df['kategori'].isin(kategori_pilihan)]
else:
    df_filter = df

# Opsi tampilan peta
st.subheader("🗺️ Peta Kampus Interaktif")

if have_folium:
    # Buat peta folium
    center_lat = df_filter['lat'].mean() if not df_filter.empty else 0
    center_lon = df_filter['lon'].mean() if not df_filter.empty else 0
    m = folium.Map(location=[center_lat, center_lon], zoom_start=17, tiles="OpenStreetMap")

    # Marker Cluster
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in df_filter.iterrows():
        popup_text = f"<b>{row['nama']}</b><br>Kategori: {row['kategori']}<br>Koordinat: {row['lat']}, {row['lon']}"
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=popup_text,
            tooltip=row['nama']
        ).add_to(marker_cluster)

    if st.sidebar.checkbox("Tampilkan Heatmap"):
        heat_data = df_filter[["lat", "lon"]].values.tolist()
        HeatMap(heat_data).add_to(m)

    # Tampilkan folium di Streamlit
    try:
        st_folium(m, width=900, height=600)
    except Exception as ex:
        st.error("Terjadi masalah saat menampilkan peta folium. Gunakan fallback peta di bawah atau cek log.")
        st.write(ex)

else:
    # Fallback: gunakan st.map atau pydeck jika folium tidak terinstall
    st.warning("`folium` atau `streamlit_folium` tidak terpasang. Menampilkan peta fallback menggunakan `st.map`.
Untuk memperbaiki: jalankan `pip install folium streamlit-folium` pada lingkungan Python Anda.")
    try:
        # st.map membutuhkan kolom latitude & longitude bernama lat/lon
        st.map(df_filter.rename(columns={'lat': 'latitude', 'lon': 'longitude'})[['latitude', 'longitude']])
    except Exception as ex:
        st.error("Gagal menampilkan peta fallback. Pastikan dataframe memiliki kolom 'lat' dan 'lon'.")
        st.write(ex)

# Tabel data
st.subheader("📊 Data Lokasi Kampus")
st.dataframe(df_filter)

# Upload CSV
st.subheader("📂 Upload Data CSV Lokasi Kampus")
uploaded_file = st.file_uploader("Upload file CSV", type="csv")

if uploaded_file is not None:
    try:
        df_upload = pd.read_csv(uploaded_file)
    except Exception as ex:
        st.error("Gagal membaca file CSV. Pastikan file valid dan gunakan encoding UTF-8.")
        st.write(ex)
        df_upload = None

    if df_upload is not None:
        required_cols = {'nama', 'lat', 'lon'}
        if not required_cols.issubset(set(df_upload.columns)):
            st.error(f"File CSV harus berisi kolom: {', '.join(required_cols)}")
        else:
            st.success("Data berhasil diupload!")
            st.dataframe(df_upload)

            if have_folium:
                m2 = folium.Map(location=[df_upload['lat'].mean(), df_upload['lon'].mean()], zoom_start=17)
                for idx, row in df_upload.iterrows():
                    folium.Marker([row['lat'], row['lon']], popup=row.get('nama', ''), tooltip=row.get('nama', '')).add_to(m2)
                st.subheader("🗺️ Peta dari File CSV")
                st_folium(m2, width=900, height=600)
            else:
                st.info("folium tidak tersedia — menampilkan lokasi sebagai tabel saja.")

# Footer: petunjuk debug jika ada error import
st.markdown("---")
st.caption("Jika mengalami `ModuleNotFoundError: folium`, jalankan: `pip install folium streamlit-folium`. Untuk deploy ke Streamlit Cloud, pastikan file requirements.txt ada di repo Anda.")

# Contoh requirements.txt (letakkan di proyek Anda jika mau deploy):
# streamlit
# pandas
# folium
# streamlit-folium
# NOTE: tambahkan versi paket jika diperlukan, mis. folium==0.14.0
