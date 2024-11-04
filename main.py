import tkinter as tk
from tkinter import messagebox
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolo11n.pt')  # Replace with your actual model file

def main_screen():
    root = tk.Tk()
    root.title("Object Detected App")

    # Title
    title = tk.Label(root, text="Object Detected App", font=("Georgia", 20))
    title.pack(pady=20)

    # Main Menu Buttons
    btn_jalan = tk.Button(root, text="Deteksi Jalan Berlubang", width=30, command=lambda: show_message("Deteksi Jalan Berlubang"))
    btn_jalan.pack(pady=10)
    
    btn_buah = tk.Button(root, text="Deteksi Buah Busuk", width=30, command=lambda: show_message("Deteksi Buah Busuk"))
    btn_buah.pack(pady=10)
    
    btn_manusia = tk.Button(root, text="Deteksi Manusia", width=30, command=detect_human)
    btn_manusia.pack(pady=10)

    root.geometry("900x700")
    root.mainloop()

def show_message(deteksi_type):
    messagebox.showinfo("Informasi", f"Memulai {deteksi_type}")

def detect_human():
    # Run the YOLO model on the camera feed
    results = model(source=0, show=True, conf=0.4, save=True)

if __name__ == "__main__":
    main_screen()
