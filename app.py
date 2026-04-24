import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# --- SAYFA AYARLARI VE ZORUNLU KARANLIK TEMA ---
st.set_page_config(page_title="SOC Mega Panel", layout="wide", initial_sidebar_state="expanded")
pio.templates.default = "plotly_dark"

# DİKKAT: Önbelleği (Cache) bilerek kapattık! Veri her zaman GÜNCEL olacak.
def load_data():
    df = pd.read_csv("kurumsal_siber_veri.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    return df

df = load_data()
df_breached = df[df['Action_Taken'].isin(['Allowed', 'Alerted Only'])]

# --- YAN MENÜ ---
st.sidebar.image("https://img.icons8.com/color/96/000000/cyber-security.png", width=80)
st.sidebar.title("🛡️ CISO Karar Merkezi")
page = st.sidebar.radio("İş Zekası Panelleri:", [
    "💰 1. CISO Finansal Risk ve Bütçe",
    "🏢 2. Departman Dağılımı (Treemap)",
    "🌍 3. Küresel Tehdit Haritası",
    "☁️ 4. Bulut ve Varlık Güvenliği",
    "💽 5. Veri Sızıntısı (DLP)",
    "⏱️ 6. SOC Müdahale Hızı (SLA)",
    "💻 7. Cihaz ve İşletim Sistemi",
    "🦠 8. Saldırı Vektörleri",
    "🛡️ 9. Firewall Başarı Oranı",
    "⏳ 10. Zamanlı Saldırı Eğilimi"
])

st.sidebar.divider()
st.sidebar.info("Sistem her yenilendiğinde güncel veriyi okur. Önbellek kapalıdır.")

# --- SAYFALAR ---

if page == "💰 1. CISO Finansal Risk ve Bütçe":
    st.title("💰 1. Ekonomik Zarar Endeksi")
    st.success("""
    🧑‍💼 **Karar Alıcı:** CISO (Bilgi Güvenliği Başkanı) ve Yönetim Kurulu
    🔍 **Neyi Anlıyor?** Şirketin güvenlik açıklarından dolayı anlık olarak ne kadar para ve veri kaybettiğini, hangi departmanın en çok maliyet yarattığını görür.
    🎯 **Hangi Kararı Alır?** Siber güvenlik sigortasının (Cyber Insurance) devreye sokulmasına, yeni yıl IT güvenlik bütçesinin artırılmasına ve en çok zarar eden departmana özel denetim başlatılmasına karar verir.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Toplam Ağ Olayı", f"{len(df):,}")
    col2.metric("Kritik Sızıntı (Breach)", f"{len(df_breached):,}", "-Acil", delta_color="inverse")
    col3.metric("Toplam Finansal Zarar", f"${df['Financial_Impact_USD'].sum():,.0f}", "-Bütçe Kaybı", delta_color="inverse")
    col4.metric("Sızdırılan Veri (GB)", f"{df['Data_Exfiltrated_MB'].sum() / 1024:,.1f} GB")
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(df_breached.groupby('Department')['Financial_Impact_USD'].sum().reset_index(), x='Department', y='Financial_Impact_USD', color='Department', text_auto='.2s', title="Departman Bazlı Hasar", template='plotly_dark')
        fig1.update_traces(hovertemplate="<b>Departman:</b> %{x}<br><b>Zarar:</b> $%{y:,.0f}<extra></extra>")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.pie(df_breached, values='Financial_Impact_USD', names='Attack_Type', hole=0.4, title="En Pahalı Saldırılar", template='plotly_dark')
        fig2.update_traces(hovertemplate="<b>Saldırı:</b> %{label}<br><b>Maliyet:</b> $%{value:,.0f}<extra></extra>")
        st.plotly_chart(fig2, use_container_width=True)

elif page == "🏢 2. Departman Dağılımı (Treemap)":
    st.title("🏢 2. İç Tehdit ve Departman Radarı")
    st.success("""
    🧑‍💼 **Karar Alıcı:** IT Direktörü ve İnsan Kaynakları (HR)
    🔍 **Neyi Anlıyor?** Şirketteki hangi departmanın, spesifik olarak hangi siber saldırıya (örn: Pazarlama -> Oltalama) maruz kaldığını oransal olarak anlar.
    🎯 **Hangi Kararı Alır?** Şirket genelindeki bilgisiz personeli tespit eder. En riskli departmanlara zorunlu "Siber Güvenlik Farkındalık Eğitimi" atar. Gerekirse riskli personellerin yetkilerini kısıtlar (Zero-Trust politikası).
    """)
    
    treemap_data = df.groupby(['Department', 'Attack_Type']).size().reset_index(name='Vaka_Sayisi')
    fig = px.treemap(treemap_data, path=[px.Constant("Şirket Geneli"), 'Department', 'Attack_Type'], values='Vaka_Sayisi', color='Vaka_Sayisi', color_continuous_scale='Reds', template='plotly_dark')
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Vaka Sayısı: %{value}<extra></extra>", textinfo="label+value")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, use_container_width=True, height=650)

elif page == "🌍 3. Küresel Tehdit Haritası":
    st.title("🌍 3. Coğrafi Siber Tehdit Haritası")
    st.success("""
    🧑‍💼 **Karar Alıcı:** SOC Analisti ve Ağ (Network) Mühendisi
    🔍 **Neyi Anlıyor?** Şirket sunucularına dünya üzerindeki hangi ülkelerden daha yoğun ve organize saldırılar yapıldığını görür.
    🎯 **Hangi Kararı Alır?** Eğer şirket sadece Türkiye'ye hizmet veriyorsa ve Rusya/Çin'den aşırı trafik geliyorsa; Firewall (Güvenlik Duvarı) üzerinden bu ülkelerin IP bloklarını tamamen yasaklama (Geo-Blocking) kararı alır.
    """)
    
    iso_map = {
        'Russia': 'RUS', 'China': 'CHN', 'USA': 'USA', 
        'Germany': 'DEU', 'Brazil': 'BRA', 'North Korea': 'PRK', 'Seychelles': 'SYC'
    }
    country_counts = df['Source_Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Attacks']
    country_counts['iso_alpha'] = country_counts['Country'].map(iso_map)
    fig = px.choropleth(country_counts, locations="iso_alpha", locationmode='ISO-3', color="Attacks", hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma, template='plotly_dark')
    fig.update_traces(hovertemplate="<b>Ülke:</b> %{hovertext}<br><b>Saldırı Sayısı:</b> %{z}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True, height=600)

elif page == "☁️ 4. Bulut ve Varlık Güvenliği":
    st.title("☁️ 4. Hedeflenen Bilişim Varlıkları")
    st.success("""
    🧑‍💼 **Karar Alıcı:** Bulut Mimarı (Cloud Architect) ve Sistem Yöneticisi
    🔍 **Neyi Anlıyor?** Şirketin fiziksel veritabanları mı (On-Prem) yoksa bulut sistemleri mi (AWS S3, Azure) daha fazla ve daha kritik saldırı alıyor, bunu tespit eder.
    🎯 **Hangi Kararı Alır?** Çok saldırı alan bulut sistemleri için Çok Faktörlü Kimlik Doğrulama (MFA) zorunluluğu getirir ve o sunuculara giden internet trafiğini özel şifreli ağlara (VPN/VPC) taşır.
    """)
    
    fig = px.histogram(df, y='Target_Asset', color='Severity', barmode='group', orientation='h', template='plotly_dark')
    fig.update_traces(hovertemplate="<b>Sistem:</b> %{y}<br><b>Risk Seviyesi:</b> %{data.name}<br><b>Vaka Sayısı:</b> %{x}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

elif page == "💽 5. Veri Sızıntısı (DLP)":
    st.title("💽 5. Data Loss Prevention (DLP)")
    st.success("""
    🧑‍💼 **Karar Alıcı:** Veri Gizliliği Sorumlusu (DPO) ve Hukuk Departmanı
    🔍 **Neyi Anlıyor?** Şirket dışına sızdırılan (çalınan) verilerin gigabayt cinsinden boyutunu ve bu sızıntıların hangi saldırı metoduyla gerçekleştiğini anlar.
    🎯 **Hangi Kararı Alır?** Çalınan veri boyutu kritik seviyedeyse, KVKK ve GDPR kapsamında yasal mercilere zorunlu bildirim yapma kararı alır. Şirket içi USB kullanımını ve bulut disk yüklemelerini teknik olarak yasaklar.
    """)
    
    fig = px.box(df_breached, x='Attack_Type', y='Data_Exfiltrated_MB', color='Attack_Type', template='plotly_dark')
    fig.update_traces(hovertemplate="<b>Saldırı Tipi:</b> %{x}<br><b>Sızan Veri (MB):</b> %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

elif page == "⏱️ 6. SOC Müdahale Hızı (SLA)":
    st.title("⏱️ 6. Olay Müdahale Performansı (Log-Normal)")
    st.success("""
    🧑‍💼 **Karar Alıcı:** SOC Müdürü (Güvenlik Operasyonları Lideri)
    🔍 **Neyi Anlıyor?** Siber güvenlik ekibinin bir krizi ortalama kaç dakikada fark edip kapattığını (Time to Resolve) anlar.
    🎯 **Hangi Kararı Alır?** Müdahale süreleri çok uzunsa (örn: saatler sürüyorsa), analiz sürecini hızlandırmak için Otomasyon (SOAR) yazılımları satın alır veya vardiyalı çalışacak yeni siber güvenlik uzmanları işe alır.
    """)
    
    fig = px.histogram(df, x='Time_to_Resolve_Mins', nbins=100, color_discrete_sequence=['cyan'], template='plotly_dark')
    fig.update_layout(xaxis_title="Çözüm Süresi (Dakika)", yaxis_title="Vaka Sayısı")
    fig.update_traces(hovertemplate="<b>Süre (Dk):</b> %{x}<br><b>Vaka Sayısı:</b> %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

elif page == "💻 7. Cihaz ve İşletim Sistemi":
    st.title("💻 7. Zafiyetli İşletim Sistemleri")
    st.success("""
    🧑‍💼 **Karar Alıcı:** Endpoint (Uç Nokta) Yöneticisi
    🔍 **Neyi Anlıyor?** Şirkette kullanılan cihazlardan (Windows, Mac, Mobil) hangilerinin güvenlik açıklarına karşı daha zayıf olduğunu tespit eder.
    🎯 **Hangi Kararı Alır?** Eski nesil işletim sistemlerinin ağa erişimini keser (Network Access Control - NAC). Kritik açık barındıran cihazlara hafta sonu acil yama (Patch) güncellemesi gönderir.
    """)
    
    fig = px.pie(df, names='Device_OS', hole=0.5, template='plotly_dark')
    fig.update_traces(textinfo='percent+label', hovertemplate="<b>İşletim Sistemi:</b> %{label}<br><b>Saldırı Sayısı:</b> %{value}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🦠 8. Saldırı Vektörleri":
    st.title("🦠 8. Zararlı Yazılım ve Vektör Dağılımı")
    st.success("""
    🧑‍💼 **Karar Alıcı:** Tehdit İstihbarat (Threat Intelligence) Uzmanı
    🔍 **Neyi Anlıyor?** Hackerların şirketi düşürmek için şu anki trendinin ne olduğunu (örn: Sisteme virüs mü atıyorlar, yoksa şifre mi kırmaya çalışıyorlar) analiz eder.
    🎯 **Hangi Kararı Alır?** Eğer fidye yazılımı (Ransomware) trendi artıyorsa, Antivirüs/EDR cihazlarının imza veritabanlarını günceller. DDoS artıyorsa internet bant genişliğini (Bandwidth) artırma kararı alır.
    """)
    
    fig = px.bar(df['Attack_Type'].value_counts().reset_index(), x='Attack_Type', y='count', color='Attack_Type', template='plotly_dark')
    fig.update_traces(hovertemplate="<b>Vektör:</b> %{x}<br><b>Sayı:</b> %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🛡️ 9. Firewall Başarı Oranı":
    st.title("🛡️ 9. Güvenlik Duvarı Performansı")
    st.success("""
    🧑‍💼 **Karar Alıcı:** Siber Güvenlik Altyapı Direktörü
    🔍 **Neyi Anlıyor?** Gelen saldırıların kaçının Firewall tarafından engellendiğini (Blocked) ve kaçının içeri sızdığını (Allowed) oransal olarak anlar.
    🎯 **Hangi Kararı Alır?** İçeri sızma oranı (Allowed) sektör standartlarının (%1-2) üzerine çıktıysa, mevcut Firewall cihazının yetersiz kaldığına karar verir ve yeni nesil IPS (Saldırı Önleme Sistemi) yatırımı yapar.
    """)
    
    fig = px.funnel(df['Action_Taken'].value_counts().reset_index(), x='count', y='Action_Taken', template='plotly_dark')
    fig.update_traces(hovertemplate="<b>Durum:</b> %{y}<br><b>Adet:</b> %{x}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

elif page == "⏳ 10. Zamanlı Saldırı Eğilimi":
    st.title("⏳ 10. Günlük Tehdit Hacmi (Saldırı Dalgaları)")
    st.success("""
    🧑‍💼 **Karar Alıcı:** SOC Vardiya Amiri
    🔍 **Neyi Anlıyor?** Saldırıların ayın veya haftanın hangi günlerinde (veya hafta sonlarında) daha büyük dalgalar halinde (Spike) geldiğini anlar.
    🎯 **Hangi Kararı Alır?** Grafikteki tepe noktalarına bakarak güvenlik uzmanlarının izin günlerini ve gece vardiyalarını planlar. Tatil günleri gelen ani artışlar için sistemi "Yüksek Güvenlik (Lockdown)" moduna geçirir.
    """)
    
    trend = df.groupby('Date').size().reset_index(name='Attack_Count')
    fig = px.line(trend, x='Date', y='Attack_Count', markers=True, line_shape='spline', template='plotly_dark')
    fig.update_traces(hovertemplate="<b>Tarih:</b> %{x}<br><b>Saldırı Sayısı:</b> %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)
