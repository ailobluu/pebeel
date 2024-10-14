import tkinter as tk 
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import pandas as pd
from datetime import datetime
import sqlite3

# Fungsi untuk menghitung GCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Fungsi Algoritma Euclidean
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1 
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

# Mencari nilai d atau kunci privat dekrip
def calculate_d(e, qn):
    gcd_val, d, _ = extended_gcd(e, qn)
    if gcd_val != 1:
        raise ValueError("e dan qn tidak relatif prima. Tidak ada invers.")
    return d % qn

# Fungsi untuk enkripsi
def encrypt_message(message, e, n):
    encrypted_message = ""
    for char in message:
        m = ord(char.lower()) - ord('a') + 3 if char.isalpha() else 0
        c = pow(m, e, n)
        encrypted_message += f"{c:04d}"
    return encrypted_message

# Fungsi untuk dekripsi
def decrypt_message(encrypted_message, d, n):
    decrypted_message = ''
    for i in range(0, len(encrypted_message), 4):
        c = int(encrypted_message[i:i+4])
        m = pow(c, d, n)
        char = chr(m + ord('a') - 8) if m > 0 else ' '
        decrypted_message += char
    return decrypted_message

# RSA Parameters
p = 47
q = 71
e = 79
n = p * q
qn = (p - 1) * (q - 1)
d = calculate_d(e, qn)

# Fungsi login
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Koneksi ke database SQLite
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Cek apakah username dan password cocok
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    
    if result:
        login_window.destroy()
        open_data_entry_window()  # Membuka window untuk memasukkan data barang
    else:
        messagebox.showerror("Login Failed", "Username atau password salah!")
    
    conn.close()

# Fungsi untuk registrasi
def register():
    username = username_entry.get()
    password = password_entry.get()
    
    # Koneksi ke database SQLite
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Membuat tabel jika belum ada
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    # Simpan username dan password
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()  
        messagebox.showinfo("Registrasi Berhasil", "Akun berhasil dibuat!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Registrasi Gagal", "Username sudah digunakan!")
    
    conn.close()

# Fungsi untuk menyimpan data barang
def save_item_data():
    nama_barang = item_name_entry.get()
    harga_barang = item_price_entry.get()
    jumlah_barang = item_quantity_entry.get()
    tanggal_input = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Menghitung harga total
    total_harga = float(harga_barang) * int(jumlah_barang) 
    
    data = f"{nama_barang}, {harga_barang}, {jumlah_barang}, {total_harga}, {tanggal_input}" 
    
    # Enkripsi data
    encrypted_message = encrypt_message(data, e, n)
    decrypted_message = decrypt_message(encrypted_message, d, n)
    
    # Simpan hasil enkripsi ke Excel
    try:
        # Cek apakah file sudah ada
        df = pd.read_excel("encrypted_data_barang.xlsx")
        new_data = pd.DataFrame({
            "Nama Barang": [nama_barang], 
            "Harga Barang": [harga_barang], 
            "Jumlah Barang": [jumlah_barang], 
            "Total Harga": [total_harga], 
            "Tanggal Input": [tanggal_input],  
            "Data Terenkripsi": [encrypted_message]  
        })
        # Gabungkan data baru dengan data yang sudah ada
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        # Jika file tidak ada, buat DataFrame baru
        df = pd.DataFrame({
            "Nama Barang": [nama_barang], 
            "Harga Barang": [harga_barang], 
            "Jumlah Barang": [jumlah_barang], 
            "Total Harga": [total_harga], 
            "Tanggal Input": [tanggal_input],  
            "Data Terenkripsi": [encrypted_message]  
        })
    
    df.to_excel("encrypted_data_barang.xlsx", index=False)
    
    messagebox.showinfo("Data Saved", "Data barang berhasil disimpan dan terenkripsi.")
    data_entry_window.quit()

# Fungsi untuk membuka window input data baranga
def open_data_entry_window():
    global item_name_entry, item_price_entry, item_quantity_entry, data_entry_window
    
    data_entry_window = tk.Tk()
    data_entry_window.title("Data Barang")
    
    tk.Label(data_entry_window, text="Nama Barang:").grid(row=0)
    tk.Label(data_entry_window, text="Harga Barang:").grid(row=1)
    tk.Label(data_entry_window, text="Jumlah Barang:").grid(row=2)
    
    item_name_entry = tk.Entry(data_entry_window)
    item_price_entry = tk.Entry(data_entry_window)
    item_quantity_entry = tk.Entry(data_entry_window)
    
    item_name_entry.grid(row=0, column=1)
    item_price_entry.grid(row=1, column=1)
    item_quantity_entry.grid(row=2, column=1)
    
    tk.Button(data_entry_window, text='Simpan', command=save_item_data).grid(row=3, column=1, pady=4)
    
    data_entry_window.mainloop()

# GUI untuk login dan registrasi
login_window = tk.Tk()
login_window.title("Login Page")

tk.Label(login_window, text="Nama:").grid(row=0)
tk.Label(login_window, text="Password:").grid(row=1)

username_entry = tk.Entry(login_window)
password_entry = tk.Entry(login_window, show='*') 

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

tk.Button(login_window, text='Login', command=login).grid(row=2, column=1, sticky=tk.W, pady=4)
tk.Button(login_window, text='Registrasi', command=register).grid(row=3, column=1, sticky=tk.W, pady=4)

login_window.mainloop()
