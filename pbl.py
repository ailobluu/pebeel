import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import pandas as pd

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
    data = username + " " + password

    # Enkripsi data
    encrypted_data = encrypt_data(data)
    encrypted_data_hex = encrypted_data.hex()

    # Simpan data terenkripsi ke file Excel
    df = pd.DataFrame({"Data Terenkripsi": [encrypted_data_hex]})
    df.to_excel("encrypted_login_data.xlsx", index=False)

    messagebox.showinfo("Login Info", f"Login berhasil!\nData terenkripsi disimpan di Excel.")
    login_window.quit()  # Tutup window setelah login

# Generate RSA keys jika belum ada
try:
    open("public_key.pem", "rb")
except FileNotFoundError:
    generate_rsa_keys()

# GUI menggunakan tkinter
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
