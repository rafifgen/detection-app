import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk, Label
from PIL import Image, ImageTk
import cv2
import os
import json
from ultralytics import YOLO

# Functions for menu buttons
def clear_body():
    """Clear all widgets inside the body frame."""
    for widget in body_frame.winfo_children():
        widget.destroy()

def home():
    """Home Page Content."""
    clear_body()
    
    content_frame = tk.Frame(body_frame, bg="lightgray", width=500, height=300)
    content_frame.pack(expand=True, pady=50)
    
    welcome_label = tk.Label(content_frame, text="SELAMAT DATANG:", bg="lightgray", fg="black", font=("Arial", 12, "bold"))
    welcome_label.pack(pady=(20, 0))
    
    desc_label = tk.Label(content_frame, text="BLABLABLA", bg="lightgray", fg="black", font=("Arial", 12))
    desc_label.pack()
    
    guide_label = tk.Label(content_frame, text="PANDUAN:", bg="lightgray", fg="black", font=("Arial", 12, "bold"))
    guide_label.pack(pady=(20, 0))
    
    guide_text = tk.Label(content_frame, text="BLA BLA BLA", bg="lightgray", fg="black", font=("Arial", 12))
    guide_text.pack()

def upload_dataset():
    """Upload Dataset Page."""
    clear_body()

    def browse_directory():
        directory = filedialog.askdirectory()
        path_entry.delete(0, tk.END)
        path_entry.insert(0, directory)

    def save_dataset():
        dataset_name = name_entry.get().strip()
        directory_path = path_entry.get().strip()
        
        if not dataset_name or not directory_path:
            messagebox.showerror("Error", "Please fill out all fields!")
            return

        # Create the main dataset directory
        main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset", dataset_name)
        os.makedirs(main_dataset_dir, exist_ok=True)
        
        # Process files in the directory
        image_extensions = (".png", ".jpg", ".jpeg")
        counter = 1

        for file in os.listdir(directory_path):
            if file.lower().endswith(image_extensions):
                file_path = os.path.join(directory_path, file)
                
                try:
                    # Open image and convert to PNG
                    img = Image.open(file_path)
                    img = img.convert("RGB")  # Ensure RGB format
                    
                    # Save with sequential numbering in the named subfolder
                    output_file_path = os.path.join(main_dataset_dir, f"{counter}.png")
                    img.save(output_file_path, "PNG")
                    counter += 1

                except Exception as e:
                    print(f"Error processing {file}: {e}")
        
        messagebox.showinfo("Success", f"Dataset '{dataset_name}' has been saved successfully!")

    # UI Elements
    tk.Label(body_frame, text="UPLOAD DATASET", font=("Arial", 16, "bold")).pack(pady=10)

    # Dataset Name
    tk.Label(body_frame, text="NAME OF DATASET:", font=("Arial", 12)).pack()
    name_entry = tk.Entry(body_frame, width=40)
    name_entry.pack(pady=5)

    # Path to Directory
    tk.Label(body_frame, text="PATH TO DIRECTORY:", font=("Arial", 12)).pack()
    path_frame = tk.Frame(body_frame)
    path_frame.pack(pady=5)

    path_entry = tk.Entry(path_frame, width=30)
    path_entry.pack(side="left", padx=(0, 5))

    browse_button = tk.Button(path_frame, text="Browse", command=browse_directory, bg="lightgray")
    browse_button.pack(side="left")

    # Submit Button
    submit_button = tk.Button(body_frame, text="SUBMIT", command=save_dataset, bg="lightgray", padx=20, pady=10)
    submit_button.pack(pady=20)

def annotate():
    clear_body()
    
    # Path to the main dataset directory
    main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")
    selected_dataset = {"name": None}  # To track selected dataset
    label_entries = []  # To store label entry references
    
    # ---------------- Step 1: Pick Dataset ---------------- #
    def step1():
        clear_body()
        
        def pick_dataset(event=None):
            dataset_name = dataset_dropdown.get().strip()
            if dataset_name in dataset_list:
                selected_dataset["name"] = dataset_name
                step2()  # Move to Step 2
        
        # Load dataset names
        dataset_list = [d for d in os.listdir(main_dataset_dir) if os.path.isdir(os.path.join(main_dataset_dir, d))]
        
        tk.Label(body_frame, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(body_frame, text="SELECT DATASET:", font=("Arial", 12)).pack(pady=5)
        
        # Searchable dropdown
        search_frame = tk.Frame(body_frame)
        search_frame.pack(pady=10)
        
        dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50)
        dataset_dropdown.pack(side="left", padx=5)
        dataset_dropdown.bind("<<ComboboxSelected>>", pick_dataset)
        
        submit_button = tk.Button(body_frame, text="SUBMIT", command=lambda: pick_dataset())
        submit_button.pack(pady=10)
    
    # ---------------- Step 2: Fill Labels.json ---------------- #
    def step2():
        clear_body()
        label_entries.clear()  # Clear any existing entries
        
        def pick_color(entry):
            color_code = colorchooser.askcolor(title="Pick a Color")[1]
            if color_code:
                entry.delete(0, tk.END)
                entry.insert(0, color_code)
        
        def add_label_form():
            form_frame = tk.Frame(label_frame)
            form_frame.pack(pady=5, fill="x")
            
            name_entry = tk.Entry(form_frame, width=30)
            name_entry.pack(side="left", padx=5)
            name_entry.insert(0, "LABEL")
            
            color_entry = tk.Entry(form_frame, width=15)
            color_entry.pack(side="left", padx=5)
            
            color_button = tk.Button(form_frame, text="PICK COLOR", command=lambda: pick_color(color_entry), bg="lightgray")
            color_button.pack(side="left", padx=5)
            
            label_entries.append((name_entry, color_entry))
        
        def save_labels_and_continue():
            labels_data = []
            for name_entry, color_entry in label_entries:
                name = name_entry.get().strip()
                color = color_entry.get().strip()
                if name and color:
                    labels_data.append({"name": name, "color": color})
            
            if not labels_data:
                messagebox.showerror("Error", "Please add at least one label.")
                return
            
            # Save labels.json
            dataset_path = os.path.join(main_dataset_dir, selected_dataset["name"])
            json_path = os.path.join(dataset_path, "labels.json")
            
            try:
                with open(json_path, "w") as json_file:
                    json.dump(labels_data, json_file, indent=4)
                step3(selected_dataset["name"])  # Move to Step 3
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        
        tk.Label(body_frame, text="STEP 2: CREATE LABELS.JSON", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame for dynamic forms
        global label_frame
        label_frame = tk.Frame(body_frame)
        label_frame.pack(pady=10, fill="x")
        
        # Add initial form
        add_label_form()
        
        # Buttons
        tambah_button = tk.Button(body_frame, text="TAMBAH LABEL", command=add_label_form, bg="lightgray", padx=10, pady=5)
        tambah_button.pack(pady=5)
        
        save_button = tk.Button(body_frame, text="SAVE", command=save_labels_and_continue, bg="lightgray", padx=20, pady=10)
        save_button.pack(pady=10)
    
    # ---------------- Step 3: Display PNG Files ---------------- #
    # Global variable for image navigation
    current_image_index = 0
    image_files = []

    def step3(dataset_name):
        """Step 3: Display images with navigation."""
        global current_image_index, image_files
        clear_body()

        # Path to the dataset folder
        dataset_path = os.path.join("list_of_dataset", dataset_name)

        # Get all PNG files in the folder
        image_files = [f for f in os.listdir(dataset_path) if f.endswith(".png")]
        if not image_files:
            messagebox.showerror("Error", "No images found in the selected dataset.")
            return

        # Sort the image files to ensure correct navigation order
        image_files.sort()
        current_image_index = 0  # Reset to the first image

        # Frame to hold navigation and image
        nav_frame = tk.Frame(body_frame, bg="white")
        nav_frame.pack(pady=10)

        # Label for dataset name
        dataset_label = tk.Label(body_frame, text=dataset_name, font=("Arial", 16, "bold"))
        dataset_label.pack()

        # Prev Button
        prev_button = tk.Button(nav_frame, text="PREV", command=lambda: navigate_image(-1), bg="lightgray", padx=10, pady=5)
        prev_button.pack(side="left", padx=10)

        # Current Image Name
        image_name_label = tk.Label(nav_frame, text="", font=("Arial", 14))
        image_name_label.pack(side="left", padx=10)

        # Next Button
        next_button = tk.Button(nav_frame, text="NEXT", command=lambda: navigate_image(1), bg="lightgray", padx=10, pady=5)
        next_button.pack(side="left", padx=10)

        # Frame for displaying the image
        image_frame = tk.Frame(body_frame, bg="white")
        image_frame.pack(pady=10)

        # Canvas for the image
        canvas = tk.Canvas(image_frame, width=500, height=500, bg="lightgray")
        canvas.pack()

        def display_image():
            """Load and display the current image."""
            image_path = os.path.join(dataset_path, image_files[current_image_index])
            img = Image.open(image_path)
            img = img.resize((500, 500))  # Resize for display purposes
            img_tk = ImageTk.PhotoImage(img)

            # Clear the canvas
            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.image = img_tk  # Keep a reference to avoid garbage collection

            # Update the current image name
            image_name_label.config(text=image_files[current_image_index])

        def navigate_image(step):
            """Navigate between images."""
            global current_image_index
            current_image_index += step

            # Ensure index is within bounds
            if current_image_index < 0:
                current_image_index = len(image_files) - 1
            elif current_image_index >= len(image_files):
                current_image_index = 0

            # Display the updated image
            display_image()

        # Display the first image initially
        display_image()

    # ---------------- Main UI Setup ---------------- #
    tk.Label(body_frame, text="ANNOTATE DATASETS", font=("Arial", 20, "bold")).pack(pady=10)
    step1()  # Start with Step 1

def train():
    clear_body()
    label = tk.Label(body_frame, text="Train Page", font=("Arial", 14))
    label.pack(pady=20)

def predict():
    clear_body()
    
    # Path to the main dataset directory
    main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")
    selected_dataset = {"name": None}  # To track selected dataset
    
    # ---------------- Step 1: Pick Dataset ---------------- #
    def step1():
        clear_body()
        
        def pick_dataset(event=None):
            dataset_name = dataset_dropdown.get().strip()
            if dataset_name in dataset_list:
                selected_dataset["name"] = dataset_name
                step2()  # Move to Step 2
        
        # Load dataset names
        dataset_list = [d for d in os.listdir(main_dataset_dir) if os.path.isdir(os.path.join(main_dataset_dir, d))]
        
        tk.Label(body_frame, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(body_frame, text="SELECT DATASET:", font=("Arial", 12)).pack(pady=5)
        
        # Searchable dropdown
        search_frame = tk.Frame(body_frame)
        search_frame.pack(pady=10)
        
        dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50)
        dataset_dropdown.pack(side="left", padx=5)
        dataset_dropdown.bind("<<ComboboxSelected>>", pick_dataset)
        
        submit_button = tk.Button(body_frame, text="SUBMIT", command=lambda: pick_dataset())
        submit_button.pack(pady=10)

    # ---------------- Step 2: List Files with .pt Extension ---------------- #
    def step2():
        clear_body()

        dataset_name = selected_dataset["name"]
        dataset_path = os.path.join(main_dataset_dir, dataset_name)

        # Get all .pt files in the dataset folder
        pt_files = [f for f in os.listdir(dataset_path) if f.endswith(".pt")]
        
        if not pt_files:
            messagebox.showinfo("No Files Found", f"No .pt files found in {dataset_name}.")
            return
        
        # Display .pt files
        tk.Label(body_frame, text="FILES WITH .PT EXTENSION", font=("Arial", 16, "bold")).pack(pady=10)
        
        for pt_file in pt_files:
            tk.Label(body_frame, text=pt_file, font=("Arial", 12)).pack(pady=5)

            step3(dataset_name, pt_file)
            break

    def step3(dataset_name, pt_file):
        model = YOLO(f"list_of_dataset/{dataset_name}/{pt_file}")
        model = YOLO("best.pt")

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Cannot open webcam")
            exit()

        # Function to update the camera feed
        def update_frame():
            ret, frame = cap.read()  # Read a frame from the camera
            if ret:
                # Convert the frame from BGR to RGB
                results = model(frame, stream=True)
                for result in results:
                    annotated_frame = result.plot()
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
                # Convert the frame into an Image object
                img = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(img)
                
                # Update the image displayed in the label
                label.img_tk = img_tk  # Store a reference to avoid garbage collection
                label.configure(image=img_tk)
            
            # Call this function again after 10ms to update the feed
            label.after(10, update_frame)
        
        # Start the update loop
        label = Label(root)
        label.pack()
        update_frame()

        pass

    tk.Label(body_frame, text="PREDICT DATASETS", font=("Arial", 20, "bold")).pack(pady=10)
    step1()  # Start with Step 1

def exit_app():
    root.destroy()

# Main window
root = tk.Tk()
root.title("Menu Interface")
root.geometry("800x500")  # Set window size
root.configure(bg="white")

# Top Menu Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(side="top", fill="x")

buttons = [
    ("HOME", home),
    ("UPLOAD DATASET", upload_dataset),
    ("ANNOTATE", annotate),
    ("TRAIN", train),
    ("PREDICT", predict),
    ("EXIT", exit_app),
]

for text, command in buttons:
    button = tk.Button(button_frame, text=text, command=command, bg="lightgray", padx=10, pady=10)
    button.pack(side="left", fill="x", expand=True)

# Body Frame - For Changing Content
body_frame = tk.Frame(root, bg="white", width=800, height=400)
body_frame.pack(expand=True, fill="both")

# Load the Home Page Initially
home()

# Run the application
root.mainloop()
