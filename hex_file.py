# Memuat file model .pt dan mengonversinya ke format heksadesimal
def convert_pt_to_hex(file_path):
    with open(file_path, 'rb') as f:
        binary_data = f.read()  # Membaca file dalam mode biner
        hex_data = binary_data.hex()  # Mengonversi biner ke heksadesimal
    return hex_data

# Ganti dengan path file .pt yang sesuai
file_path = 'yolo11n.pt'
hex_representation = convert_pt_to_hex(file_path)

# Menampilkan sebagian dari representasi heksadesimal
print(hex_representation[:1000])  # Menampilkan 1000 karakter pertama