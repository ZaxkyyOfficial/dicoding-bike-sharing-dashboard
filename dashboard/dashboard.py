import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling visual matplotlib & seaborn
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 11
})

# Load Data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df_main = load_data()

# ----------------- SIDEBAR FILTER -----------------
st.sidebar.image("https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=300&q=80", use_container_width=True)
st.sidebar.title("🚴 Filter Analisis")
st.sidebar.markdown("Sesuaikan rentang waktu dan parameter data di bawah ini:")

# Filter Rentang Tanggal
min_date = df_main['dteday'].min().date()
max_date = df_main['dteday'].max().date()

date_range = st.sidebar.date_input(
    label="Pilih Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter Musim
all_seasons = sorted(df_main['season_label'].dropna().unique().tolist())
selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim (Season)",
    options=all_seasons,
    default=all_seasons
)

# Filter Kondisi Cuaca
all_weather = sorted(df_main['weather_label'].dropna().unique().tolist())
selected_weather = st.sidebar.multiselect(
    label="Pilih Kondisi Cuaca (Weather)",
    options=all_weather,
    default=all_weather
)

# Filter Tipe Hari
day_type_options = ["Semua", "Hari Kerja (Working Day)", "Akhir Pekan/Libur (Weekend/Holiday)"]
selected_day_type = st.sidebar.selectbox("Pilih Tipe Hari", day_type_options)

# Penanganan range tanggal (bila user hanya klik 1 tanggal)
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date

# Filter Dataframe
filtered_df = df_main[
    (df_main['dteday'].dt.date >= start_date) &
    (df_main['dteday'].dt.date <= end_date) &
    (df_main['season_label'].isin(selected_seasons)) &
    (df_main['weather_label'].isin(selected_weather))
]

if selected_day_type == "Hari Kerja (Working Day)":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif selected_day_type == "Akhir Pekan/Libur (Weekend/Holiday)":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# ----------------- MAIN CONTENT -----------------
st.title("🚲 Capital Bikeshare: Interactive Analytics Dashboard")
st.markdown("""
Dashboard interaktif ini menyajikan wawasan komprehensif mengenai pola penyewaan sepeda, dampak cuaca/musim, serta segmentasi perilaku pengguna (Casual vs Registered) berdasarkan dataset historis Capital Bikeshare.
""")

st.divider()

# Empty State Check
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih. Silakan sesuaikan filter sidebar Anda.")
    st.stop()

# Metric Cards
total_rentals = int(filtered_df['cnt'].sum())
total_registered = int(filtered_df['registered'].sum())
total_casual = int(filtered_df['casual'].sum())

reg_pct = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
casual_pct = (total_casual / total_rentals * 100) if total_rentals > 0 else 0

daily_agg = filtered_df.groupby('dteday')['cnt'].sum()
avg_daily_rentals = int(daily_agg.mean()) if not daily_agg.empty else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Penyewaan (Total Bikes)", value=f"{total_rentals:,}")
with col2:
    st.metric(label="Pengguna Terdaftar (Registered)", value=f"{total_registered:,}", delta=f"{reg_pct:.1f}%")
with col3:
    st.metric(label="Pengguna Santai (Casual)", value=f"{total_casual:,}", delta=f"{casual_pct:.1f}%")
with col4:
    st.metric(label="Rata-rata Harian (Daily Mean)", value=f"{avg_daily_rentals:,}")

st.divider()

# Tabs untuk Visualisasi
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren Waktu", 
    "⛅ Musim & Cuaca (Bisnis 1)", 
    "⏰ Pola Jam Pengguna (Bisnis 2)", 
    "🏷️ Segmentasi Lanjutan (Binning)"
])

# ----------------- TAB 1: Tren Waktu -----------------
with tab1:
    st.subheader("Tren Penyewaan Sepeda Harian Sepanjang Waktu")
    
    daily_trend = filtered_df.groupby('dteday')[['cnt', 'registered', 'casual']].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily_trend['dteday'], daily_trend['cnt'], label='Total Rentals', color='#1f77b4', linewidth=1.8)
    ax.plot(daily_trend['dteday'], daily_trend['registered'], label='Registered', color='#2ca02c', alpha=0.7, linestyle='--')
    ax.plot(daily_trend['dteday'], daily_trend['casual'], label='Casual', color='#ff7f0e', alpha=0.7, linestyle=':')
    ax.set_title("Fluktuasi Harian Penyewaan Sepeda", fontweight='bold', pad=12)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    st.info("💡 **Insight Tren:** Pertumbuhan volume penyewaan meningkat signifikan dari tahun 2011 ke 2012, dengan lonjakan tajam pada pertengahan tahun (musim panas dan gugur).")

# ----------------- TAB 2: Musim & Cuaca (Pertanyaan Bisnis 1) -----------------
with tab2:
    st.subheader("Pengaruh Musim & Kondisi Cuaca Terhadap Penyewaan Sepeda")
    st.markdown("**Pertanyaan Bisnis 1:** *Bagaimana pengaruh kondisi cuaca dan musim terhadap rata-rata penyewaan sepeda harian selama periode 2011–2012, sebagai dasar bagi tim operasional dalam menjadwalkan kuota unit sepeda dan masa servis armada?*")
    
    col_season, col_weather = st.columns(2)
    
    with col_season:
        season_avg = filtered_df.groupby('season_label')['cnt'].mean().reset_index()
        season_avg = season_avg.sort_values(by='cnt', ascending=False)
        
        fig, ax = plt.subplots(figsize=(7, 4.5))
        palette_s = ['#2b5c8f' if x == season_avg['cnt'].max() else '#7fa8d0' for x in season_avg['cnt']]
        sns.barplot(data=season_avg, x='season_label', y='cnt', palette=palette_s, ax=ax)
        ax.set_title("Rata-rata Penyewaan per Musim", fontweight='bold')
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Penyewaan / Jam")
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{height:.1f}", (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        
    with col_weather:
        weather_avg = filtered_df.groupby('weather_label')['cnt'].mean().reset_index()
        weather_avg = weather_avg.sort_values(by='cnt', ascending=False)
        
        fig, ax = plt.subplots(figsize=(7, 4.5))
        palette_w = ['#2b5c8f' if x == weather_avg['cnt'].max() else '#9bb7d4' for x in weather_avg['cnt']]
        sns.barplot(data=weather_avg, x='weather_label', y='cnt', palette=palette_w, ax=ax)
        ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca", fontweight='bold')
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Penyewaan / Jam")
        plt.xticks(rotation=15)
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{height:.1f}", (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        
    st.success("""
    📌 **Temuan Kunci:**
    - **Musim Gugur (Fall)** mencatatkan rata-rata penyewaan sepeda tertinggi, disusul oleh **Musim Panas (Summer)**. Musim semi (Spring) mencatat performa terendah karena temperatur yang masih dingin.
    - Cuaca cerah (**Clear**) sangat disukai pengguna dengan rata-rata penyewaan tertinggi. Cuaca buruk (**Light Snow/Rain**) menurunkan animo penyewaan hingga lebih dari 60%.
    """)

# ----------------- TAB 3: Casual vs Registered (Pertanyaan Bisnis 2) -----------------
with tab3:
    st.subheader("Pola Penyewaan Jam Sibuk: Pengguna Casual vs Registered")
    st.markdown("**Pertanyaan Bisnis 2:** *Bagaimana perbandingan rata-rata penyewaan antara pengguna casual dan registered berdasarkan jam dalam sehari (khususnya jam sibuk komuter 07:00–09:00 dan 17:00–19:00) pada hari kerja selama periode 2011–2012, sebagai dasar arahan tim pemasaran untuk kampanye konversi pelanggan dan tim operasional untuk rebalancing stasiun?*")
    
    # Filter data hari kerja & weekend untuk perbandingan
    df_wd = filtered_df[filtered_df['workingday'] == 1].groupby('hr')[['casual', 'registered']].mean().reset_index()
    df_nwd = filtered_df[filtered_df['workingday'] == 0].groupby('hr')[['casual', 'registered']].mean().reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
    
    # Hari Kerja
    if not df_wd.empty:
        ax1.plot(df_wd['hr'], df_wd['registered'], label='Registered', color='#1f77b4', marker='o', linewidth=2)
        ax1.plot(df_wd['hr'], df_wd['casual'], label='Casual', color='#ff7f0e', marker='s', linewidth=2)
        ax1.axvspan(7, 9, color='lightgray', alpha=0.4, label='Peak Pagi (07-09)')
        ax1.axvspan(17, 19, color='lightgray', alpha=0.4, label='Peak Sore (17-19)')
        ax1.set_title("Hari Kerja (Working Day): Pola Komuter", fontweight='bold')
        ax1.set_xlabel("Jam (0 - 23)")
        ax1.set_ylabel("Rata-rata Penyewaan")
        ax1.set_xticks(range(0, 24, 2))
        ax1.legend(loc='upper right')
    else:
        ax1.text(0.5, 0.5, 'Tidak ada data Hari Kerja', ha='center', va='center')
        
    # Akhir Pekan / Hari Libur
    if not df_nwd.empty:
        ax2.plot(df_nwd['hr'], df_nwd['registered'], label='Registered', color='#2ca02c', marker='o', linewidth=2)
        ax2.plot(df_nwd['hr'], df_nwd['casual'], label='Casual', color='#d62728', marker='s', linewidth=2)
        ax2.set_title("Akhir Pekan/Libur (Weekend/Holiday): Pola Rekreasi", fontweight='bold')
        ax2.set_xlabel("Jam (0 - 23)")
        ax2.set_xticks(range(0, 24, 2))
        ax2.legend(loc='upper right')
    else:
        ax2.text(0.5, 0.5, 'Tidak ada data Akhir Pekan', ha='center', va='center')
        
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    st.success("""
    📌 **Temuan Kunci:**
    - Pada **Hari Kerja**, terjadi fenomena *bimodal distribution* (dua puncak tajam): jam **08:00** pagi (rata-rata 450+ unit) dan jam **17:00–18:00** sore (rata-rata 460–520+ unit), didominasi penuh oleh **pengguna Registered** untuk keperluan komuter berangkat/pulang kantor.
    - Pada **Akhir Pekan/Libur**, pola berubah menjadi *unimodal* (lonceng tunggal): penyewaan meningkat perlahan dari siang hingga sore (12:00–16:00), dengan proporsi pengguna **Casual** yang meningkat signifikan untuk aktivitas rekreasi.
    """)

# ----------------- TAB 4: Segmentasi Lanjutan (Binning) -----------------
with tab4:
    st.subheader("Teknik Analisis Lanjutan: Binning Kelompok Waktu & Tingkat Permintaan")
    st.markdown("""
    Teknik **Binning (Rule-based Clustering)** dilakukan tanpa model Machine Learning guna mengelompokkan data ke dalam kategori yang mudah ditindaklanjuti oleh manajemen operasional:
    1. **Time-of-Day Grouping**: Mengelompokkan jam ke dalam 4 sesi kerja harian (Dini Hari, Pagi, Siang/Sore, Malam).
    2. **Daily Demand Level**: Mengelompokkan total volume sewa harian menjadi *Low Demand*, *Medium Demand*, dan *High Demand*.
    """)
    
    col_bin1, col_bin2 = st.columns(2)
    
    with col_bin1:
        time_group_df = filtered_df.groupby('time_group')['cnt'].agg(['sum', 'mean']).reindex([
            'Dini Hari (00-05)', 'Pagi (06-11)', 'Siang/Sore (12-17)', 'Malam (18-23)'
        ]).reset_index()
        
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.barplot(data=time_group_df, x='time_group', y='sum', palette='Blues_d', ax=ax)
        ax.set_title("Total Volume Sewa per Kelompok Waktu", fontweight='bold')
        ax.set_xlabel("Kelompok Waktu")
        ax.set_ylabel("Total Sepeda Disewa")
        plt.xticks(rotation=15)
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{height/1000:.1f}k", (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        
    with col_bin2:
        # Binning Tingkat Permintaan Harian
        daily_totals = filtered_df.groupby('dteday')['cnt'].sum().reset_index()
        if len(daily_totals) >= 3:
            daily_totals['demand_cat'] = pd.qcut(
                daily_totals['cnt'], 
                q=3, 
                labels=['Low Demand', 'Medium Demand', 'High Demand']
            )
            demand_counts = daily_totals['demand_cat'].value_counts().reindex(['Low Demand', 'Medium Demand', 'High Demand'])
            
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.pie(
                demand_counts.values, 
                labels=demand_counts.index, 
                autopct='%1.1f%%', 
                colors=['#e74c3c', '#f39c12', '#27ae60'],
                startangle=140,
                explode=(0.04, 0.04, 0.04)
            )
            ax.set_title("Proporsi Hari Berdasarkan Level Permintaan", fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.write("Rentang data terlalu sedikit untuk segmentasi kuantil harian.")
            
    st.info("""
    🎯 **Aplikasi Bisnis dari Segmentasi:**
    - **Time Grouping:** Sesi **Siang/Sore (12:00-17:00)** dan **Malam (18:00-23:00)** menyumbang lebih dari 65% total sirkulasi armada harian. Sesi **Dini Hari (00:00-05:00)** merupakan jendela optimal untuk pemeliharaan unit dan redistribusi docking station.
    - **Demand Level:** Hari-hari dengan status *Low Demand* terkorelasi erat dengan cuaca hujan ekstrem atau hari di awal musim semi.
    """)

# Footer
st.caption("Proyek Analisis Data - Bike Sharing Dataset | Dicoding Submission | Author: Senior Data Analyst")

