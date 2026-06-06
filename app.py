"""
==========================================
 Aplikasi EcoSurface: Pemantauan Air
==========================================

Aplikasi ini dibuat untuk membantu kegiatan pemantauan kualitas air permukaan.
Terdapat dua fitur utama:
1. Panduan Sampling (Wadah, Pengawet, Holding Time)
2. Evaluasi Baku Mutu (Perbandingan hasil analisis)

Author: [Nama Anda]
Framework: Streamlit (Python)
"""

# ==========================================
# IMPORT LIBRARY
# ==========================================
import streamlit as st
import pandas as pd

# ==========================================
# KONFIGURASI HALAMAN (PAGE CONFIG)
# ==========================================
st.set_page_config(
    page_title="EcoSurface - Kualitas Air",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DATA: PANDUAN SAMPLING (FITUR 1)
# ==========================================
# Dictionary ini menyimpan informasi teknis untuk setiap parameter.
# Mengikuti standar seperti SNI atau EPA guidelines.
SAMPLING_GUIDE = {
    "pH": {
        "wadah": "Botol Plastik (PE)",
        "volume": "100 mL",
        "pengawet": "Tidak ada",
        "penyimpanan": "4°C",
        "holding_time": "Segera analisa (< 2 jam)",
        "catatan": "Kalibrasi alat ukur pH wajib dilakukan setiap hari."
    },
    "Suhu": {
        "wadah": "Botol Kaca",
        "volume": "1 L",
        "pengawet": "Tidak ada",
        "penyimpanan": "In situ / On site",
        "holding_time": "Segera dibaca",
        "catatan": "Pengukuran dilakukan langsung di lokasi pengambilan."
    },
    "TSS (Total Suspended Solid)": {
        "wadah": "Botol Kaca / PE",
        "volume": "1 L",
        "pengawet": "Tidak ada",
        "penyimpanan": "4°C",
        "holding_time": "Maks 7 hari",
        "catatan": "Hindari pengadukan kuat saat pengambilan agar padatan tidak terlarut."
    },
    "TDS (Total Dissolved Solid)": {
        "wadah": "Botol PE",
        "volume": "500 mL",
        "pengawet": "Tidak ada",
        "penyimpanan": "4°C",
        "holding_time": "Maks 28 hari",
        "catatan": "Sebelum analisis, sample disaring dengan filter 0.45 μm."
    },
    "DO (Dissolved Oxygen)": {
        "wadah": "Botol Kaca Amber + Seal Cap",
        "volume": "300 mL",
        "pengawet": "Reagen Winkler",
        "penyimpanan": "4°C",
        "holding_time": "Maks 8 jam",
        "catatan": "Hindari gelembung udara saat pengisian botol."
    },
    "BOD (Biochemical Oxygen Demand)": {
        "wadah": "Botol Kaca Amber",
        "volume": "1 L",
        "pengawet": "H2SO4 pH < 2",
        "penyimpanan": "4°C",
        "holding_time": "Maks 48 jam (idealnya < 6 jam)",
        "catatan": "Jika analisa > 48 jam, bekukan di -20°C."
    },
    "COD (Chemical Oxygen Demand)": {
        "wadah": "Botol Kaca",
        "volume": "500 mL",
        "pengawet": "H2SO4 hingga pH < 2",
        "penyimpanan": "4°C",
        "holding_time": "Maks 28 hari",
        "catatan": "Sampel harus segera didinginkan setelah pengambilan."
    },
    "Nitrat": {
        "wadah": "Botol PE",
        "volume": "250 mL",
        "pengawet": "H2SO4 hingga pH < 2",
        "penyimpanan": "4°C",
        "holding_time": "Maks 28 hari",
        "catatan": "Hindari kontak langsung kulit."
    },
    "Fosfat": {
        "wadah": "Botol PE",
        "volume": "250 mL",
        "pengawet": "H2SO4 hingga pH < 2",
        "penyimpanan": "4°C",
        "holding_time": "Maks 28 hari",
        "catatan": "Cuci botol dengan HCl sebelum pakai."
    },
    "Total Coliform": {
        "wadah": "Botol Steril",
        "volume": "100 mL",
        "pengawet": "Na2S2O3 (Natrium Tiosulfat)",
        "penyimpanan": "4°C",
        "holding_time": "Maks 24 jam",
        "catatan": "Jaga sterilisasi wadah."
    }
    # Tambahkan parameter lain sesuai kebutuhan di sini
}

# ==========================================
# DATA: BAKU MUTU (FITUR 2)
# ==========================================
# Baku Mutu Air Permukaan (Contoh: Berdasarkan PermenLH No. 5 Tahun 2014
 
# Struktur: 'nilai' adalah angka baku mutu
# 'tipe' adalah logika perbandingan:
# - '<=' : Nilai hasil harus lebih kecil dari sama dengan baku mutu (umum)
# - '>=' : Nilai hasil harus lebih besar dari sama dengan baku mutu (khusus DO/Nitrat)
WATER_STANDARDS = {
    "pH": {"nilai": 9.0, "tipe": "<="},
    "TSS": {"nilai": 50, "tipe": "<="},
    "DO": {"nilai": 4.0, "tipe": ">="},
    "BOD": {"nilai": 3, "tipe": "<="},
    "COD": {"nilai": 25, "tipe": "<="},
    "Nitrat": {"nilai": 0.5, "tipe": "<="},
    "Fosfat": {"nilai": 0.5, "tipe": "<="},
    "Total Coliform": {"nilai": 100, "tipe": "<="}
}

# ==========================================
# FUNGSI TAMPILAN (UI HELPERS)
# ==========================================
def show_card(title, icon, content_html):
    """Membuat kotak/card sederhana menggunakan HTML/CSS."""
    st.markdown(f"""
    <div style="
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #4CAF50;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h4 style="margin-top:0; color: #264c3e;">{icon} {title}</h4>
        {content_html}
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# HALAMAN UTAMA (DASHBOARD)
# ==========================================
def home_page():
    st.title("💧 Dashboard EcoSurface")
    st.markdown("""
    Selamat datang di **EcoSurface**, aplikasi untuk membantu kegiatan pemantauan kualitas air permukaan.
    Gunakan menu di sidebar untuk navigasi.
    """)
    
    st.divider()
    
    # Metric Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📊 Parameter Sampling", value=len(SAMPLING_GUIDE))
    with col2:
        st.metric(label="⚖️ Parameter Baku Mutu", value=len(WATER_STANDARDS))
    with col3:
        st.metric(label="🗂️ Standar Regulasi", value="PermenLH 5/2014")
        
    st.divider()
    
    st.subheader("📌 Quick Start")
    col_left, col_right = st.columns(2)
    with col_left:
        st.info("**Fitur 1: Panduan Sampling**\n\nBelum tahu wadah apa yang harus digunakan untuk sampel Nitrat? Gunakan menu Panduan Sampling untuk melihat detailnya.")
    with col_right:
        st.info("**Fitur 2: Evaluasi Baku Mutu**\n\nHasil lab COD Anda adalah 30 mg/L? Cek apakah air tersebut masih memenuhi baku mutu di menu Evaluasi.")

# ==========================================
# FITUR 1: PANDUAN SAMPLING
# ==========================================
def sampling_page():
    st.title("🧪 Panduan Sampling")
    st.markdown("Pilih parameter kualitas air untuk melihat detail teknis pengambilan sampel.")
    
    st.divider()
    
    # Dropdown Menu
    list_parameters = list(SAMPLING_GUIDE.keys())
    list_parameters.insert(0, "-- Pilih Parameter --") # Opsi default
    
    selected_param = st.selectbox(
        "Pilih Parameter Analisis:",
        list_parameters
    )
    
    if selected_param != "-- Pilih Parameter --":
        # Ambil data dari dictionary
        details = SAMPLING_GUIDE[selected_param]
        
        # Tampilan dalam Kolom (Columns)
        c1, c2 = st.columns(2)
        
        with c1:
            show_card("📦 Wadah & Volume", "🏺", 
                      f"<b>Wadah:</b> {details['wadah']}<br>"
                      f"<b>Volume Min:</b> {details['volume']}")
            
            show_card("🧊 Penyimpanan", "❄️", 
                      f"<b>Suhu:</b> {details['penyimpanan']}<br>"
                      f"<b>Holding Time:</b> {details['holding_time']}")
        
        with c2:
            show_card("🧪 Pengawet", "⚗️", 
                      f"<b>Bahan:</b> {details['pengawet']}")
            
            show_card("📝 Catatan", "📄", 
                      f"<i>{details['catatan']}</i>")
                      
    else:
        st.warning("Silakan pilih parameter di atas!")

# ==========================================
# FITUR 2: EVALUASI BAKU MUTU
# ==========================================
def evaluation_page():
    st.title("📈 Evaluasi Baku Mutu")
    st.markdown("Bandingkan hasil analisis laboratorium dengan baku mutu yang berlaku.")
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Input Data")
        
        # Input Parameter
        list_std_params = list(WATER_STANDARDS.keys())
        list_std_params.insert(0, "-- Pilih Parameter --")
        
        select_eval_param = st.selectbox("Pilih Parameter:", list_std_params)
        
        # Input Nilai Hasil
        float_nilai_hasil = st.number_input(
            "Masukkan Nilai Hasil Analisis:", 
            min_value=0.0, 
            step=0.1,
            format="%.2f"
        )
        
        # Button Proses
        proses = st.button("💡 Cek Kualitas", type="primary")

    with col2:
        if proses and select_eval_param != "-- Pilih Parameter --":
            # Ambil data baku mutu
            std_data = WATER_STANDARDS[select_eval_param]
            nilai_baku = std_data['nilai']
            tipe_operator = std_data['tipe']
            
            # Logika Evaluasi
            is_safe = False
            if tipe_operator == "<=":
                is_safe = float_nilai_hasil <= nilai_baku
                status_text = "MENUHI BAKU MUTU" if is_safe else "TIDAK MEMENUHI BAKU MUTU"
                diff = float_nilai_hasil -
