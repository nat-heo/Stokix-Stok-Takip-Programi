import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import json  # Verileri kaydetmek için

# --------------------------------------Görsel Ayarlar--------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --------------------------------------Giriş Ekranı--------------------------------------
giris_penceresi = ctk.CTk()
giris_penceresi.geometry("450x500")
giris_penceresi.title("Stokix Giriş")

# --------------------------------------Stok Ekranı--------------------------------------
stok_penceresi = ctk.CTkToplevel()
stok_penceresi.title("Stokix")
stok_penceresi.geometry("450x500")
stok_penceresi.withdraw()

def show_giris():
    stok_penceresi.withdraw()
    giris_penceresi.deiconify()

def show_stok():
    giris_penceresi.withdraw()
    stok_penceresi.deiconify()

def giris_kontrol():
    kullanici = giris_kullanici.get().strip()
    sifre = giris_sifre.get().strip()
    
    if kullanici == "Admin" and sifre == "123":
        messagebox.showinfo("Başarılı", "Giriş Başarılı!")
        show_stok()
    else:
        messagebox.showerror("Hata", "Hatalı Kullanıcı Adı veya Şifre!")

# --------------------------------------Giriş Ekranı Arayüzü--------------------------------------
giris_frame = ctk.CTkFrame(master=giris_penceresi)
giris_frame.pack(pady=20, padx=40, fill='both', expand=True)

giris_kullanici = ctk.CTkEntry(master=giris_frame, placeholder_text="Kullanıcı Adınızı Giriniz!")
giris_kullanici.pack(pady=12, padx=10)

giris_sifre = ctk.CTkEntry(master=giris_frame, placeholder_text="Şifre Giriniz!", show="*")
giris_sifre.pack(pady=12, padx=10)

giris_buton = ctk.CTkButton(master=giris_frame, text="Giriş", command=giris_kontrol)
giris_buton.pack(pady=12, padx=10)

# --------------------------------------Stok Takip Sistemi--------------------------------------
ana_cerceve = ctk.CTkFrame(master=stok_penceresi)
ana_cerceve.pack(pady=20, padx=40, fill='both', expand=True)

urun_giris = ctk.CTkEntry(master=ana_cerceve, placeholder_text="Ürün Adı", width=200, height=30)
urun_giris.grid(row=1, column=0, padx=10, pady=5)

miktar_giris = ctk.CTkEntry(master=ana_cerceve, placeholder_text="Miktar", width=200, height=30)
miktar_giris.grid(row=2, column=0, padx=10, pady=5)

liste_kutusu = ctk.CTkTextbox(master=ana_cerceve, width=350, height=150)
liste_kutusu.grid(row=0, column=0, padx=10, pady=5,)

stoklar = {}

def veriyi_yukle():
    global stoklar
    try:
        with open("stoklar.json", "r") as dosya:
            stoklar = json.load(dosya)
    except FileNotFoundError:
        stoklar = {}

def veriyi_kaydet():
    with open("stoklar.json", "w") as dosya:
        json.dump(stoklar, dosya)

def stok_ekle():
    urun_kodu = urun_giris.get().strip()
    miktar = miktar_giris.get().strip()

    if urun_kodu and miktar.isdigit():
        miktar = int(miktar)
        stoklar[urun_kodu] = stoklar.get(urun_kodu, 0) + miktar
        listeyi_guncelle()
        veriyi_kaydet()

def stok_azalt():
    urun_kodu = urun_giris.get().strip()
    miktar = miktar_giris.get().strip()

    if urun_kodu in stoklar and miktar.isdigit():
        miktar = int(miktar)
        if stoklar[urun_kodu] > miktar:
            stoklar[urun_kodu] -= miktar
        else:
            del stoklar[urun_kodu]
        listeyi_guncelle()
        veriyi_kaydet()

def stok_ara():
    arama_kodu = urun_giris.get().strip()
    liste_kutusu.delete("1.0", "end")

    if arama_kodu in stoklar:
        liste_kutusu.insert("end", f"{arama_kodu}: {stoklar[arama_kodu]} adet\n")
    else:
        liste_kutusu.insert("end", "Ürün bulunamadı.\n")

def listeyi_guncelle():
    liste_kutusu.delete("1.0", "end")
    for urun, miktar in stoklar.items():
        liste_kutusu.insert("end", f"{urun}: {miktar} adet\n")

veriyi_yukle()
listeyi_guncelle()

# Butonlar
ekle_butonu = ctk.CTkButton(master=ana_cerceve, text="Ekle", width=200, height=30, command=stok_ekle)
ekle_butonu.grid(row=3, column=0, padx=10, pady=5)

azalt_butonu = ctk.CTkButton(master=ana_cerceve, text="Azalt", width=200, height=30, command=stok_azalt)
azalt_butonu.grid(row=4, column=0, padx=10, pady=5)

arama_butonu = ctk.CTkButton(master=ana_cerceve, text="Ara", width=200, height=30, command=stok_ara)
arama_butonu.grid(row=5, column=0, padx=10, pady=5)

hesapcikis_butonu = ctk.CTkButton(master=ana_cerceve, text="Çıkış Yap", width=200, height=30, command=show_giris)
hesapcikis_butonu.grid(row=6, column=0, padx=10, pady=5)

giris_penceresi.mainloop()
