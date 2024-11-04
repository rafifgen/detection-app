import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolo11n.pt')  # Replace with your actual model file

# Global variables
stop_flag = False  # Flag to stop the camera feed
cap = None
video_label = None
stop_button = None
exit_button = None

def main_screen():
    global video_label, stop_button, exit_button
    root = tk.Tk()
    root.title("Object Detection App")

    # Title
    title = tk.Label(root, text="Object Detection App", font=("Georgia", 20))
    title.pack(pady=10)

    # Main Menu Buttons
    btn_jalan = tk.Button(root, text="Deteksi Jalan Berlubang", width=30, command=lambda: show_message("Deteksi Jalan Berlubang"))
    btn_jalan.pack(pady=10)
    
    btn_buah = tk.Button(root, text="Deteksi Buah Busuk", width=30, command=lambda: show_message("Deteksi Buah Busuk"))
    btn_buah.pack(pady=10)
    
    btn_manusia = tk.Button(root, text="Deteksi Manusia", width=30, command=start_human_detection)
    btn_manusia.pack(pady=10)

    # Video display area
    video_label = tk.Label(root)
    video_label.pack(pady=10)

    # Initialize Buttons
    initialize_buttons(root)

    root.geometry("900x700")
    root.mainloop()

def initialize_buttons(root):
    global stop_button, exit_button

    # Stop Button (initially hidden)
    stop_button = tk.Button(root, text="Stop Camera", command=stop_human_detection)
    stop_button.pack(pady=10)
    stop_button.pack_forget()  # Hide until the camera starts

    # Exit Button
    exit_button = tk.Button(root, text="Exit App", width=30, command=root.quit)
    exit_button.pack(pady=20)

def show_message(deteksi_type):
    messagebox.showinfo("Informasi", f"Memulai {deteksi_type}")

def start_human_detection():
    global cap, stop_flag, stop_button, exit_button
    stop_flag = False
    cap = cv2.VideoCapture(0)
    update_frame()  # Start updating the video label with frames
    
    # Hide the Exit button and show the Stop button
    if exit_button:
        exit_button.pack_forget()
    stop_button.pack()

def update_frame():
    global cap, stop_flag

    if not stop_flag:
        # Capture a frame from the camera
        ret, frame = cap.read()
        if ret:
            # Run YOLO model for human detection
            results = model.predict(frame, conf=0.4)
            frame = results[0].plot()  # Annotate frame with detection results

            # Convert the frame to an image Tkinter can display
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk  # Keep a reference to avoid garbage collection
            video_label.configure(image=imgtk)  # Update the label

        # Schedule the next frame update
        video_label.after(10, update_frame)
    else:
        cap.release()  # Release the camera resource

def stop_human_detection():
    global stop_flag, exit_button
    stop_flag = True  # Stop updating frames
    video_label.config(image="")  # Clear the video display area
    stop_button.pack_forget()  # Hide the Stop button
    if exit_button:
        exit_button.pack()  # Show the Exit button again

if __name__ == "__main__":
    main_screen()
