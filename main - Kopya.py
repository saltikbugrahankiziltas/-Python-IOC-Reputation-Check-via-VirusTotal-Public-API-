import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# VERİYİ YÜKLE
df = pd.read_csv("nsl_kdd_sample.csv")

# METİN VERİLERİ SAYISALA ÇEVİR
le1 = LabelEncoder()
df["protocol_type"] = le1.fit_transform(df["protocol_type"])

le2 = LabelEncoder()
df["label"] = le2.fit_transform(df["label"])  # normal:1, anomaly:0 olabilir

# MODELİ EĞİT
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# GÜVENLİK DUVARI GİBİ KARAR VER
def guvenlik_duvari(ip, tahmin):
    if tahmin == 0:
        print(f"❌ SALDIRI! {ip} IP’si engellendi.")
    else:
        print(f"✅ Normal trafik: {ip} IP’sine izin verildi.")

# VERİ SAYISINA GÖRE DÖN
for i in range(len(X_test)):
    sample = X_test.iloc[i]
    tahmin = model.predict([sample.values])[0]  # burada .values eklendi
    guvenlik_duvari(f"192.168.1.{i+100}", tahmin)

