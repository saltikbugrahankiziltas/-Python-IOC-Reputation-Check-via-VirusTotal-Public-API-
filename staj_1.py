import requests
import json
import os
import time

API_KEY = "REMOVED_API_KEY"  # <-- Buraya kendi VirusTotal Public API anahtarınızı girin
API_URL = "https://www.virustotal.com/api/v3/ip_addresses/"
HEADERS = {
    "x-apikey": API_KEY
}

# Gerekli dosya ve klasörler
INPUT_FILE = "ips.txt"
MALICIOUS_FILE = "malicious_ips.txt"
NOT_FOUND_FILE = "not_found_ips.txt"
RESPONSES_DIR = "responses"

# responses klasörü yoksa oluştur
os.makedirs(RESPONSES_DIR, exist_ok=True)

# Dosyaları temizle
open(MALICIOUS_FILE, "w").close()
open(NOT_FOUND_FILE, "w").close()

# IP'leri oku
with open(INPUT_FILE, "r") as file:
    ips = [line.strip() for line in file if line.strip()]

for ip in ips:
    print(f"Sorgulanıyor: {ip}")
    response = requests.get(API_URL + ip, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        # JSON'u kaydet
        with open(f"{RESPONSES_DIR}/{ip}.json", "w") as outfile:
            json.dump(data, outfile, indent=2)

        try:
            malicious = data['data']['attributes']['last_analysis_stats']['malicious']
            suspicious = data['data']['attributes']['last_analysis_stats']['suspicious']
            
            if malicious > 0 or suspicious > 0:
                with open(MALICIOUS_FILE, "a") as mfile:
                    mfile.write(ip + "\n")
        except KeyError:
            # Beklenmeyen JSON formatı
            with open(NOT_FOUND_FILE, "a") as nfile:
                nfile.write(ip + "\n")

    elif response.status_code == 404:
        with open(NOT_FOUND_FILE, "a") as nfile:
            nfile.write(ip + "\n")
    else:
        print(f"Hata: {ip} için {response.status_code} döndü")

    # Rate limit'e takılmamak için kısa bekleme
    time.sleep(15)  # Public API için önerilir (rate limit: ~4 istek/dakika)

print("Tamamlandı.")
