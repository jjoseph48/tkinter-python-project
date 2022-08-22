# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:04:44 2022

@author: Gallery
"""
# import modul , numpy dan matplotlib yang akan digunakan untuk memproses 
# gambar, berikan nama alias untuk numpy yaitu np dan matplotlib sebagai plt
import cv2
import numpy as np
import matplotlib.pyplot as plt
# import modul tkinter sebagai tk yang digunakan untuk menampilkan GUI, ambil
# modul ttk juga dari tkinter
import tkinter as tk
from tkinter import ttk, messagebox
# import modul pillow (PIL) dan import juga modul ImageTk dan image yang digu-
# nakan juga untuk memproses gambar
from PIL import ImageTk, Image
import mysql.connector

# Definisikan sebuah kelas dengan nama Produk
class Produk:
    # Pada kelas ini terdapat beberapa atribut yaitu nama, warna, stok dan harga
    nama = ""
    warna = ""
    stok = 0
    harga = 0
    
    # Buat konstruktur untuk kelas Produk dengan parameter berupa seluruh atribut
    def __init__(self, nama, warna, harga, stok):
        self.nama  = nama
        self.warna = warna
        self.harga = harga
        self.stok  = stok
    
    # Buat getter dan setter untuk tiap atribut kecuali stok
    def ambilNama(self):
        return self.nama
    
    def ubahNama(self, nama):
        self.nama = nama
    
    def ambilWarna(self):
        return self.warna
    
    def ubahWarna(self, warna):
        self.warna = warna
    
    def ambilHarga(self):
        return self.harga
    
    def ubahHarga(self, harga):
        self.harga = harga
    
    # Method kurangiBarang() digunakan untuk mengurangi stok barang tiap kali 
    # barang dibeli
    def kurangiBarang(self):
        self.stok = self.stok - 1

# Di bawah ini, kode untuk menghubungkan python dengan mysql
# Jika koneksi berhasil maka koneksi akan dicetak
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Harrypotter48*",
  database = "pad_db"
)
print(mydb)

# Create obyek dari kelas Produk
cangkirA = Produk("Cangkir Hitam", "Hitam", 30000, 10)
cangkirB = Produk("Cangkir Hijau", "Hijau", 35000, 5)
cangkirC = Produk("Cangkir Kuning", "Kuning", 25000, 12)
id = ["J1", "J2", "J3"]

# PathGambar adalah list dari path gambar produk yang dibeli
pathGambar = ['mug.jpg', 'mug2.jpg', 'mug3.jpg']

# Inisiasi dari modul tk menjadi variabel root
root = tk.Tk()
# Atur lebar dan tinggi dari jendela frame
root.geometry('750x400')
# Atur agar jendela frame tidak dapat diubah
root.resizable(False, False)

# Fungsi prosesBarang digunakan tiap kali produk di scan untuk dapat mengetahui
# jumlah dan warna produk sehingga harga total dapat ditentukan
def prosesBarang(path):
    idPenjualan = id.pop()
    # Input gambar dengan method imread dari modul cv2 dan simpan pada variabel
    # image
    image = cv2.imread(path)
    
    # Kode baris 82 sampai 121 merupakan proses deteksi warna dari produk yang 
    # dibeli dengan menggunakan modul cv2 dan numpy
    # Pertama, atur nilai untuk warna dasar
    b = image[:, :, :1]
    g = image[:, :, 1:2]
    r = image[:, :, 2:]

    # hitung rata-rata dari warna dasar
    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)
    
    # Analisa gambar dengan mencari warna paling menonjol di tiap gambar
    if(b_mean < g_mean and g_mean < r_mean):
       # Jika gambar memenuhi syarat di atas, maka warna yang paling menonjol
       # adalah warna kuning, sehingga warnaBarang akan diisi dengan hasil 
       # return dari method ambilWarna dari obyek cangkirC yaitu warna kuning
       warnaBarang = cangkirC.ambilWarna()
       # Setelah itu, isikan entryNamaProduk dengan nama dari obyek cangkirC
       entryNamaProduk.insert(5, cangkirC.ambilNama())
       # Isikan pula entryWarnaProduk dengan nilai dari warnaBarang
       entryWarnaProduk.insert(7, warnaBarang)
    elif(g_mean > r_mean and g_mean > b_mean):
       # Jika gambar memenuhi syarat di atas, maka warna yang paling menonjol
       # adalah warna hijau, sehingga warnaBarang akan diisi dengan hasil 
       # return dari method ambilWarna dari obyek cangkirC yaitu warna hijau
       warnaBarang = cangkirB.ambilWarna()
       # Setelah itu, isikan entryNamaProduk dengan nama dari obyek cangkirB
       entryNamaProduk.insert(5, cangkirB.ambilNama())
       # Isikan pula entryWarnaProduk dengan nilai dari warnaBarang
       entryWarnaProduk.insert(7, warnaBarang)
    else:
       # Jika gambar memenuhi syarat di atas, maka warna yang paling menonjol
       # adalah warna hitam, sehingga warnaBarang akan diisi dengan hasil 
       # return dari method ambilWarna dari obyek cangkirC yaitu warna hitam
       warnaBarang = cangkirA.ambilWarna()
       # Setelah itu, isikan entryNamaProduk dengan nama dari obyek cangkirA
       entryNamaProduk.insert(5, cangkirA.ambilNama())
       # Isikan pula entryWarnaProduk dengan nilai dari warnaBarang
       entryWarnaProduk.insert(7, warnaBarang)
    # Deteksi warna produk selesai
    
    # Kode baris 124 sampai 153 merupakan proses perhitungan produk yang dibeli
    # dengan memproses gambar dengan modul cv2, numpy dan matplotlib
    
    # Langkah pertama adalah mengkonversi gambar menjadi skala abu-abu
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    # Perhitungan jumlah obyek dilakukan dengan mendeteksi pinggiran, hal ini
    # dapat dilakukan dengan memburamkan gambar. Hal tersebut dilakukan dengan 
    # menggunakan method GaussianBlur dari modul cv2
    blur = cv2.GaussianBlur(gray, (11,11), 0)
    # Mendeteksi tepi menggunakan algoritma canny, parameter ke-2 & ke-3 dalam 
    # fungsi cv2.canny() adalah nilai ambang batas. Dimana, nilai antara 30 & 
    # 150 dianggap sebagai tepi untuk suatu gambar. Terdapat perubahan ambang 
    # batas dari kode asli agar tepi dapat terbaca khusus proyek ini
    canny = cv2.Canny(blur, 60, 253, 4)
    # Tepi yang terbuat masih saling terputus, untuk menyatukannya, buat tepi
    # menjadi lebih tebal dengan method dilate di bawah ini
    dilated = cv2.dilate(canny, (1, 1), iterations=0)
    # Proses selanjutnya adalah menghitung kontur pada gambar dan mengkonversi
    # gambar dari BGR menjadi RGB serta menggambar kontur
    (cnt, hierarchy) = cv2.findContours(
        dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 4)
    # Dengan modul pyplot, tampilkan gambar beserta konturnya
    plt.imshow(rgb)
    # Simpan hasil perhitungan kontur ke variabel jumlahBeli
    jumlahBeli = len((cnt))
    
    # Isikan hasil perhitungan objek ke entryJumlahProduk
    entryJumlahProduk.insert(9, str(jumlahBeli))
    # Deteksi jumlah produk selesai

    sql = "INSERT INTO transaksi_penjualan (id_penjualan, `nama_produk`, `harga_produk`, jumlah beli, total_harga) VALUES (%s, %s, %s, %s, %s);"
    # Proses selanjutnya adalah menghitung total harga dari tiap produk yang 
    # dibeli
    if warnaBarang == "Hitam":
        produk = cangkirA
        # Jika cangkir yang dibeli memiliki warna hitam, total harga dihitung
        # dengan mengkalikan harga cangkir hitam dengan jumlah beli
        totalHarga = cangkirA.ambilHarga() * jumlahBeli
        # Panggil method kurangiBarang untuk mengurangi jumlah stok
        cangkirA.kurangiBarang()
        val = (idPenjualan, 'Cangkir hitam', 30000, jumlahBeli, totalHarga,)
    elif warnaBarang == "Hijau":
        produk = cangkirB
        # Jika cangkir yang dibeli memiliki warna hijau, total harga dihitung
        # dengan mengkalikan harga cangkir hijau dengan jumlah beli
        totalHarga = cangkirB.ambilHarga() * jumlahBeli
        # Panggil method kurangiBarang untuk mengurangi jumlah stok
        cangkirB.kurangiBarang()
        val = (idPenjualan, 'Cangkir hijau', 35000, jumlahBeli, totalHarga,)
    else :
        produk = cangkirC
        # Jika cangkir yang dibeli memiliki warna kuning, total harga dihitung
        # dengan mengkalikan harga cangkir kuning dengan jumlah beli
        totalHarga = cangkirC.ambilHarga() * jumlahBeli
        # Panggil method kurangiBarang untuk mengurangi jumlah stok
        cangkirC.kurangiBarang()
        val = (idPenjualan, 'Cangkir kuning', 25000, jumlahBeli, totalHarga,)
    
    # Isikan entryTotalHarga dengan hasil perhitungan di atas
    entryTotalHarga.insert(12, str(totalHarga))
    mycursor = mydb.cursor()

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

# Fungsi dibawah ini akan memanggil fungsi prosesBarang dengan parameter berupa
# hasil pop dari list pathGambar, gunakan try-catch untuk handle index out bound
def pilihGambar():
    try:
        data = pathGambar.pop()
        prosesBarang(data)
    except IndexError:
        messagebox.showerror("PERINGATAN", "Semua Produk Telah Diproses!")
    
    
# Fungsi clear() digunakan untuk menghapus seluruh entry agar dapat digunakan
# untuk perhitungan selanjutnya
def clear():
    entryNamaProduk.delete(0,20)
    entryWarnaProduk.delete(0,10)
    entryJumlahProduk.delete(0,2)
    entryTotalHarga.delete(0,20)
    
# Kode 194 sampai 198 digunakan untuk menampilkan logo perusahaan pada GUI
# Panggil method PhotoImage dari modul ImageTk dengan perintah untuk membuka
# gambar logo.jpg dan menyimpannya pada variabel imgLogo
imgLogo = ImageTk.PhotoImage(Image.open("logo2.jpg"))
# Buat label dengan isi berupa gambar dari imgLogo
labelLogo = ttk.Label(image = imgLogo)
# Atur letak dari labelLogo
labelLogo.grid(
    row = 1,
    column = 3)

# Kode 206 sampai 280 digunakan untuk menampilkan label, button dan entry pada 
# GUI

# Buat button dengan nama buttonScan yang akan digunakan untuk memproses gambar
# dan menampilkannya pada tiap entry yang sesuai. Pada bagian parameter command
# panggil method pilihGambar untuk dapat mengakses fungsi prosesGambar
buttonScan = ttk.Button(root, 
            text = "Scan Produk",
            command = pilihGambar)
# Atur letak buttonScan pada jendela
buttonScan.grid(
    row = 15,
    column = 3)

# Buat button dengan nama buttonBayar yang akan memanggil method clear()
buttonBayar = ttk.Button(root,
                         text = "Bayar",
                         command = clear)
# Atur letak buttonBayarr pada jendela
buttonBayar.grid(
    row = 17,
    column = 3)

# Label-label jarak digunakan untuk memberikan jarak pada tiap label penting
labelJarak = ttk.Label(root)
labelJarak.grid(
    row = 2,
    column = 2)

labelJarak2 = ttk.Label(root, text = "  ")
labelJarak2.grid(
    row = 10,
    column = 1)

labelJarak3 = ttk.Label(root, text = "  ")
labelJarak3.grid(
    row = 14,
    column = 1)

labelJarak4 = ttk.Label(root, text = "  ")
labelJarak4.grid(
    row = 16,
    column = 1)

# Buat labelNamaProduk yang akan menunjukkan nama produk yang telah dianalisa
labelNamaProduk = ttk.Label(root,
                            text = "Nama Produk : ")
# Atur letak label pada jendela
labelNamaProduk.grid(
    row = 5,
    column = 2)
# Buat labelWarnaProduk yang akan menunjukkan warna produk yang telah dianalisa
labelWarnaProduk = ttk.Label(root,
                             text = "Warna Produk : ")
# Atur letak label pada jendela
labelWarnaProduk.grid(
    row = 7,
    column = 2)
# Buat labelJumlahProduk yang akan menunjukkan jumlah produk yang telah dianalisa
labelJumlahProduk = ttk.Label(root,
                              text = "Jumlah beli : ")
# Atur letak label pada jendela
labelJumlahProduk.grid(
    row = 9,
    column = 2)
# Buat labelTotalHarga yang akan menunjukkan total harga produk
labelTotalHarga = ttk.Label(root,
                            text = "Total Harga  : ")
# Atur letak label pada jendela
labelTotalHarga.grid(
    row = 12,
    column = 2)
# Buat entryNamaProduk yang akan berisi nama produk yang dibeli
entryNamaProduk = ttk.Entry(root)
# Atur letak entry pada jendela
entryNamaProduk.grid(
    row = 5,
    column = 3)
# Buat entryWarnaProduk yang akan berisi warna produk yang dibeli
entryWarnaProduk = ttk.Entry(root)
# Atur letak entry pada jendela
entryWarnaProduk.grid(
    row = 7,
    column = 3)
# Buat entryJumlahProduk yang akan berisi jumlah produk yang dibeli
entryJumlahProduk = ttk.Entry(root)
# Atur letak entry pada jendela
entryJumlahProduk.grid(
    row = 9,
    column = 3)
# Buat entryTotalHarga yang akan berisi total harga dari produk yang dibeli
entryTotalHarga = ttk.Entry(root)
# Atur letak entry pada jendela
entryTotalHarga.grid(
    row = 12,
    column  = 3)

# Panggil method mainloop() agar GUI dapat ditampilkan
root.mainloop()
