import pandas as pd
import numpy as np
import time

print("🚨 HİPER-ASİMETRİK VE MANTIKSAL MEGA VERİ SETİ ÜRETİLİYOR 🚨")
start_time = time.time()

n_rows = 100000

departments = ['Human Resources', 'Finance', 'Marketing', 'IT & Security', 'Engineering', 'Executive']
p_dept = [0.55, 0.25, 0.12, 0.05, 0.02, 0.01]

# Logical OS distribution by Department
os_probs = {
    'Human Resources': {'Windows 10': 0.80, 'Windows 11': 0.10, 'macOS': 0.05, 'Android': 0.05},
    'Finance': {'Windows 10': 0.70, 'Windows 11': 0.20, 'macOS': 0.05, 'iOS': 0.05},
    'Marketing': {'macOS': 0.50, 'Windows 11': 0.30, 'iOS': 0.10, 'Windows 10': 0.10},
    'Engineering': {'Linux (Ubuntu)': 0.40, 'macOS': 0.30, 'Windows 11': 0.20, 'Windows 10': 0.10},
    'IT & Security': {'Linux (Ubuntu)': 0.50, 'Windows 11': 0.30, 'macOS': 0.20},
    'Executive': {'macOS': 0.40, 'iOS': 0.30, 'Windows 11': 0.20, 'Android': 0.10}
}

# Logical Attack distribution by Department
attack_probs = {
    'Human Resources': {'Phishing': 0.70, 'Malware': 0.20, 'Ransomware': 0.05, 'Brute Force': 0.05},
    'Finance': {'Phishing': 0.40, 'Ransomware': 0.30, 'Insider Threat': 0.20, 'Malware': 0.10},
    'IT & Security': {'DDoS': 0.35, 'Brute Force': 0.30, 'Zero-Day': 0.15, 'SQL Injection': 0.15, 'Insider Threat': 0.05},
    'Engineering': {'SQL Injection': 0.40, 'DDoS': 0.30, 'Zero-Day': 0.15, 'Malware': 0.15},
    'Marketing': {'Phishing': 0.50, 'DDoS': 0.30, 'Malware': 0.20},
    'Executive': {'Phishing': 0.60, 'Ransomware': 0.30, 'Insider Threat': 0.10}
}

# Logical Target Asset distribution by Attack Type
asset_probs = {
    'Phishing': {'Office 365': 0.80, 'Azure AD': 0.20},
    'Malware': {'Office 365': 0.50, 'Azure AD': 0.30, 'AWS EC2': 0.20},
    'Ransomware': {'AWS S3 Bucket': 0.40, 'On-Prem Database': 0.40, 'Office 365': 0.20},
    'DDoS': {'AWS EC2': 0.60, 'Azure AD': 0.30, 'AWS S3 Bucket': 0.10},
    'Brute Force': {'Azure AD': 0.60, 'Office 365': 0.30, 'AWS EC2': 0.10},
    'SQL Injection': {'On-Prem Database': 0.70, 'AWS EC2': 0.30},
    'Insider Threat': {'On-Prem Database': 0.50, 'AWS S3 Bucket': 0.30, 'Azure AD': 0.20},
    'Zero-Day': {'AWS EC2': 0.50, 'On-Prem Database': 0.50}
}

# Logical Severity distribution by Attack Type
severity_probs = {
    'Zero-Day': {'Critical': 0.70, 'High': 0.30},
    'Ransomware': {'Critical': 0.60, 'High': 0.40},
    'SQL Injection': {'High': 0.70, 'Medium': 0.30},
    'DDoS': {'Medium': 0.60, 'High': 0.30, 'Low': 0.10},
    'Phishing': {'Low': 0.70, 'Medium': 0.25, 'High': 0.05},
    'Malware': {'Low': 0.60, 'Medium': 0.30, 'High': 0.10},
    'Brute Force': {'Low': 0.80, 'Medium': 0.20},
    'Insider Threat': {'High': 0.50, 'Critical': 0.50}
}

actions = ['Blocked', 'Quarantined', 'Alerted Only', 'Allowed']
p_action = [0.85, 0.08, 0.05, 0.02]

countries = ['Russia', 'China', 'USA', 'Unknown', 'Germany', 'Brazil', 'North Korea', 'Seychelles']
p_country = [0.45, 0.35, 0.08, 0.05, 0.03, 0.02, 0.015, 0.005]

df = pd.DataFrame({'Event_ID': np.arange(n_rows)})

print("1. Departmanlar Atanıyor...")
df['Department'] = np.random.choice(departments, n_rows, p=p_dept)
df['User'] = df['Department'].str[:3].str.upper() + "-" + np.random.randint(1000, 9999, size=n_rows).astype(str)

print("2. Mantıksal İşletim Sistemleri Atanıyor...")
def get_os(dept):
    dist = os_probs[dept]
    return np.random.choice(list(dist.keys()), p=list(dist.values()))
df['Device_OS'] = df['Department'].apply(get_os)

print("3. Mantıksal Saldırı Türleri Atanıyor...")
def get_attack(dept):
    dist = attack_probs[dept]
    return np.random.choice(list(dist.keys()), p=list(dist.values()))
df['Attack_Type'] = df['Department'].apply(get_attack)

print("4. Hedeflenen Varlıklar ve Risk Seviyeleri Atanıyor...")
def get_asset(attack):
    dist = asset_probs[attack]
    return np.random.choice(list(dist.keys()), p=list(dist.values()))
df['Target_Asset'] = df['Attack_Type'].apply(get_asset)

def get_severity(attack):
    dist = severity_probs[attack]
    return np.random.choice(list(dist.keys()), p=list(dist.values()))
df['Severity'] = df['Attack_Type'].apply(get_severity)

print("5. Aksiyon ve Kaynak Bilgileri...")
df['Action_Taken'] = np.random.choice(actions, n_rows, p=p_action)
df['Source_Country'] = np.random.choice(countries, n_rows, p=p_country)
df['Source_IP'] = [f"{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}" for _ in range(n_rows)]

print("6. Log-Normal (Gerçekçi) SOC Müdahale Hızları (SLA)...")
resolve_times = np.random.lognormal(mean=2.5, sigma=1.0, size=n_rows)
df['Time_to_Resolve_Mins'] = np.clip(resolve_times, 1, 1440).astype(int)

print("7. Finansal Hasar ve Data Sızıntısı...")
df['Financial_Impact_USD'] = 0
df['Data_Exfiltrated_MB'] = 0
mask_breach = df['Action_Taken'].isin(['Allowed', 'Alerted Only'])

base_costs = {'Phishing': 500, 'Brute Force': 1000, 'Malware': 2500, 'DDoS': 15000, 'SQL Injection': 25000, 'Insider Threat': 40000, 'Ransomware': 150000, 'Zero-Day': 250000}
severity_multiplier = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 5}

for idx in df[mask_breach].index:
    df.loc[idx, 'Financial_Impact_USD'] = int(base_costs.get(df.loc[idx, 'Attack_Type'], 1000) * severity_multiplier.get(df.loc[idx, 'Severity'], 1) * np.random.uniform(0.9, 1.2))
    df.loc[idx, 'Data_Exfiltrated_MB'] = int(np.random.exponential(scale=100))

print("8. Dalgalı Timeline (Hacker Saldırı Dalgaları)...")
days_ago = np.concatenate([
    np.random.normal(10, 2, int(n_rows*0.5)),
    np.random.normal(24, 3, int(n_rows*0.3)),
    np.random.uniform(0, 30, int(n_rows*0.2))
])
days_ago = np.clip(days_ago, 0, 29).astype(int)
seconds_offset = np.random.randint(0, 86400, size=n_rows)
start_date = pd.Timestamp.now().normalize()
df['Timestamp'] = start_date - pd.to_timedelta(days_ago, unit='D') + pd.to_timedelta(seconds_offset, unit='s')
df = df.sort_values('Timestamp').reset_index(drop=True)

df.to_csv("kurumsal_siber_veri.csv", index=False)
print(f"🔥 MANTIKSAL VERİ HAZIR! ({time.time() - start_time:.2f} saniye)")
