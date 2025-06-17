#!/bin/bash

TARGET_DIR="/opt/scripts"
BASELINE_FILE="/opt/scripts/baseline_hashes.txt"
REPORT_FILE="/opt/scripts/integrity_report.txt"
TEMP_FILE="/tmp/current_hashes.tmp"

# Mevcut SHA256 hash'leri al
find "$TARGET_DIR" -type f -exec sha256sum {} \; | sort > "$TEMP_FILE"

# İlk çalıştırma: baseline dosyası yoksa oluştur ve çık
if [ ! -f "$BASELINE_FILE" ]; then
    cp "$TEMP_FILE" "$BASELINE_FILE"
    exit 0
fi

# Farkları karşılaştır ve raporla
diff "$BASELINE_FILE" "$TEMP_FILE" > "$REPORT_FILE"

# Geçici dosya silinmezse klasörü doldurabilir
rm -f "$TEMP_FILE"
