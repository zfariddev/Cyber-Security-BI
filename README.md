# Cyber-Security-BI



**Siber Güvenlik BI**, karmaşık siber güvenlik loglarını ve tehdit verilerini sadece teknik birer metrik olmaktan çıkarıp; tüm departmanlar için anlamlı, stratejik iş zekasına dönüştüren kurumsal çaplı bir BI projesidir. 

Bu proje; veri sızıntılarını, finansal riskleri ve operasyonel darboğazları analiz ederek her departmanın (Finans, İK, Yazılım, Pazarlama) kendi özelinde veriye dayalı kararlar almasını sağlar.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🏢 Departman Bazlı Karar Mekanizmaları

Siber Güvenlik BI, veriyi demokratikleştirerek karar alma sürecini tüm kuruma yayar:

* **📈 Finans Departmanı:** Siber olayların neden olduğu doğrudan finansal kayıpları (USD) izleyerek bütçe planlaması yapar ve sigorta maliyetlerini optimize eder.
* **👥 İnsan Kaynakları:** Sosyal mühendislik ve oltalama (Phishing) saldırılarına en çok maruz kalan birimleri tespit ederek hedefli eğitim stratejileri geliştirir.
* **💻 Mühendislik & IT:** Sistem zafiyetlerini, kullanılan OS dağılımlarını ve teknik çözüm sürelerini (MTTR) analiz ederek teknolojik altyapı yatırımlarına karar verir.
* **📣 Pazarlama:** Kurumsal marka itibarını doğrudan etkileyebilecek veri sızıntılarını takip eder ve kriz yönetim planlarını bu verilere göre günceller.
* **🛡️ CISO & Güvenlik Operasyonları:** Tüm bu verileri harmanlayarak küresel tehdit coğrafyasına göre personel vardiya planlaması ve savunma hattı konfigürasyonu (Firewall/IPS) yapar.

## 🚀 Öne Çıkan Özellikler

-   **💰 Finansal Risk Analizi:** Saldırı tipine ve departmana göre özelleştirilmiş maliyet projeksiyonları.
-   **🏢 Departman Radar Map:** Hangi birimin hangi tehdit türüne karşı kritik eşikte olduğunu gösteren görsel analizler.
-   **🌍 Küresel Tehdit Görselleştirme:** Dünya haritası üzerinde gerçek zamanlı saldırı kaynağı takibi.
-   **📊 100.000+ Satırlık Dinamik Veri:** `veri_uretici.py` ile oluşturulan, kurumsal hiyerarşiye ve mantıksal kurallara dayanan asimetrik mega veri seti.
-   **⏳ Operasyonel Trend Takibi:** Saldırı yoğunluğuna göre iş gücü optimizasyonu sağlayan zaman serisi analizleri.

## 🛠️ Teknik Altyapı

-   **Dil:** Python 3.9+
-   **Arayüz:** Streamlit (Premium Dark Theme & Glassmorphism)
-   **Veri Analizi:** Pandas & NumPy
-   **Grafik Kütüphanesi:** Plotly (Etkileşimli ve dokunmatik uyumlu)

## 📦 Kurulum ve Kullanım

Sistemi bilgisayarınızda hızlıca ayağa kaldırmak için aşağıdaki adımları izleyebilirsiniz:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/zfariddev/Cyber-Securtiy-BI.git
    cd siber-guvenlik-bi
    ```

2.  **Bağımlılıkları Yükleyin:**
    Gerekli Python kütüphanelerini doğrudan sisteminize kurun:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Sistemi Başlatın:**
    ```bash
    streamlit run app.py
    streamlit run mega_dashboard.py(baska bir terminalde)
    ```

## 📊 Veri Modeli Mantığı

Sistemdeki her bir veri satırı, kurumsal bir birimin karar alma sürecini tetikleyen bir "olaydır". `Action_Taken` (Alınan Önlem) ve `Financial_Impact` (Finansal Etki) arasındaki korelasyon, güvenlik ve altyapı yatırımlarının doğruluğunu test etmek için matematiksel bir temel oluşturur.

---


---
