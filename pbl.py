import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import pandas as pd
from datetime import datetime

# Fungsi untuk membuat kunci RSA (public dan private)
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Simpan private key
    with open("private_key.pem", "wb") as priv_file:
        priv_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Simpan public key
    with open("public_key.pem", "wb") as pub_file:
        pub_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

# Fungsi untuk mengenkripsi data
def encrypt_data(data):
    with open("public_key.pem", "rb") as pub_file:
        public_key = serialization.load_pem_public_key(pub_file.read(), backend=default_backend())

    ciphertext = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# Fungsi untuk login
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Cek apakah login sesuai
    if username == "Arsyad" and password == "admin123":
        messagebox.showinfo("Login Info", "Login berhasil!")
        login_window.destroy()  # Tutup login window
        
        # Buka window input barang
        open_item_input_window()
    else:
        messagebox.showerror("Login Gagal", "Username atau Password salah!")

# Fungsi untuk input barang setelah login
def open_item_input_window():
    item_window = tk.Tk()
    item_window.title("Input Data Barang")
    
    # Label dan Entry untuk input data barang
    tk.Label(item_window, text="Nama Barang:").grid(row=0)
    tk.Label(item_window, text="Harga Barang:").grid(row=1)
    tk.Label(item_window, text="Jumlah Barang:").grid(row=2)
    tk.Label(item_window, text="Tanggal:").grid(row=3)

    nama_barang_entry = tk.Entry(item_window)
    harga_barang_entry = tk.Entry(item_window)
    jumlah_barang_entry = tk.Entry(item_window)

    # Tampilkan tanggal otomatis
    tanggal = datetime.now().strftime("%Y-%m-%d")
    tanggal_label = tk.Label(item_window, text=tanggal)
    
    nama_barang_entry.grid(row=0, column=1)
    harga_barang_entry.grid(row=1, column=1)
    jumlah_barang_entry.grid(row=2, column=1)
    tanggal_label.grid(row=3, column=1)

    # Fungsi untuk menyimpan data ke Excel
    def simpan_data():
        nama_barang = nama_barang_entry.get()
        harga_barang = harga_barang_entry.get()
        jumlah_barang = jumlah_barang_entry.get()
        
        if not (nama_barang and harga_barang and jumlah_barang):
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return

        data = {
            "Nama Barang": [nama_barang],
            "Harga Barang": [harga_barang],
            "Jumlah Barang": [jumlah_barang],
            "Tanggal": [tanggal]
        }
        df = pd.DataFrame(data)
        
        # Simpan data ke file Excel
        df.to_excel("data_barang.xlsx", index=False)
        messagebox.showinfo("Berhasil", "Data berhasil disimpan!")
        item_window.destroy()

    # Tombol untuk menyimpan data
    tk.Button(item_window, text="Simpan", command=simpan_data).grid(row=4, column=1, pady=10)

    item_window.mainloop()

# Generate RSA keys jika belum ada
try:
    open("public_key.pem", "rb")
except FileNotFoundError:
    generate_rsa_keys()

# GUI Login menggunakan tkinter
login_window = tk.Tk()
login_window.title("Login Page")

tk.Label(login_window, text="Nama:").grid(row=0)
tk.Label(login_window, text="Password:").grid(row=1)

username_entry = tk.Entry(login_window)
password_entry = tk.Entry(login_window, show='*')

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

tk.Button(login_window, text='Login', command=login).grid(row=2, column=1, sticky=tk.W, pady=4)

login_window.mainloop()
