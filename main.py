import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tkinter as tk
from tkinter import scrolledtext

# Veri ve model işlemleri (aynı)
def model_egit_ve_tahmin_yap():
    df = pd.read_csv("nsl_kdd_sample.csv")
    le1 = LabelEncoder()
    df["protocol_type"] = le1.fit_transform(df["protocol_type"])
    le2 = LabelEncoder()
    df["label"] = le2.fit_transform(df["label"])

    X = df.drop("label", axis=1)
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    sonuçlar = []
    for i in range(len(X_test)):
        sample = X_test.iloc[i]
        tahmin = model.predict([sample.values])[0]
        ip = f"192.168.1.{i+100}"
        if tahmin == 0:
            sonuçlar.append((f"❌ SALDIRI! {ip} IP’si engellendi.", "red"))
        else:
            sonuçlar.append((f"✅ Normal trafik: {ip} IP’sine izin verildi.", "green"))
    return sonuçlar

# Tkinter GUI
def baslat():
    sonuçlar = model_egit_ve_tahmin_yap()
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)  # Önceki metni sil
    for satir, renk in sonuçlar:
        text_area.insert(tk.END, satir + "\n", renk)
    text_area.config(state=tk.DISABLED)

# Arayüz oluştur
pencere = tk.Tk()
pencere.title("Akıllı Güvenlik Duvarı")
pencere.geometry("700x500")
pencere.configure(bg="#282c34")

baslik = tk.Label(pencere, text="Derin Öğrenme ve Uzman Sistemlerle Akıllı Güvenlik Duvarı", 
                  font=("Helvetica", 16, "bold"), fg="white", bg="#282c34")
baslik.pack(pady=15)

baslat_butonu = tk.Button(pencere, text="Başlat", command=baslat, 
                         font=("Helvetica", 14), bg="#61afef", fg="black", activebackground="#98c1ff")
baslat_butonu.pack(pady=10)

text_area = scrolledtext.ScrolledText(pencere, width=80, height=20, font=("Consolas", 12))
text_area.pack(padx=10, pady=10)
text_area.tag_config("red", foreground="red")
text_area.tag_config("green", foreground="lightgreen")
text_area.config(bg="#21252b", fg="white", insertbackground="white", state=tk.DISABLED)

pencere.mainloop()
