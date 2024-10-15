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
        # Konversi karakter ke angka (a=1, b=2, ..., z=26, spasi=0)
        m = ord(char.lower()) - ord('a') + 7 if char.isalpha() else 3
        # Enkripsi: c = m^e mod n
        c = pow(m, e, n)
        # Format agar setiap hasil enkripsi menjadi angka dengan panjang tetap (misalnya 4 digit)
        encrypted_message += f"{c:04d}"
    return encrypted_message

# Fungsi untuk dekripsi
def decrypt_message(encrypted_message, d, n):
    decrypted_message = ''
    # Membagi encrypted_message ke dalam blok-blok angka dengan panjang 4 digit
    for i in range(0, len(encrypted_message), 4):
        # Mengambil blok 4 digit
        c = int(encrypted_message[i:i+4])
        # Dekripsi: m = c^d mod n
        m = pow(c, d, n)
        # Konversi angka kembali ke karakter
        char = chr(m + ord('a') - 4) if m > 0 else ' '
        decrypted_message += char
    return decrypted_message

# Main program
if __name__ == "__main__":
    # Menghitung kunci publik dan privat
    p = int(input("Masukkan Kunci Pertama: "))
    q = int(input("Masukkan Kunci Kedua: "))
    e = int(input("Masukkan Kunci Ketiga: "))
    n = p * q
    qn = (p - 1) * (q - 1)
    d = calculate_d(e, qn)

    # Input pesan untuk dienkripsi
    message = input("Masukkan pesan untuk dienkripsi: ")
    
    # Enkripsi pesan
    encrypted_message = encrypt_message(message, e, n)
    print(f"Pesan terenkripsi: {encrypted_message}")
    
    # Input pesan terenkripsi untuk dikonvert
    encrypted_input = encrypted_message
    
    # Konvert pesan
    decrypted_message = decrypt_message(encrypted_input, d, n)
    print(f"Pesan terkonvert: {decrypted_message}")
