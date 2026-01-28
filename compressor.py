import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os


def compress_pdf(input_path, output_path, quality):
    """
    Compress PDF using Ghostscript.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    gs_executable = os.path.join(BASE_DIR, "gs", "gswin64c.exe")
    
    cmd = [
        gs_executable,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print("Ghostscript error:", e)
        return False


def choose_input():
    file = filedialog.askopenfilename(
        title="Select PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file)


def start_compression():
    input_path = input_entry.get().strip()
    if not input_path or not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid PDF file.")
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save compressed PDF as"
    )
    if not output_path:
        return

    quality = quality_var.get()

    status_label.config(text="Compressing...", fg="blue")
    root.update_idletasks()

    ok = compress_pdf(input_path, output_path, quality)
    if ok:
        status_label.config(text="Done!", fg="green")
        messagebox.showinfo("Success", "PDF compressed successfully!")
    else:
        status_label.config(text="Failed.", fg="red")
        messagebox.showerror("Error", "Ghostscript compression failed.")


# -- GUI --

root = tk.Tk()
root.title("PDF Compressor (Ghostscript)")
root.geometry("450x260")
root.resizable(False, False)


# Input label
tk.Label(root, text="Select PDF:", font=("Arial", 11)).pack(pady=5)

frame = tk.Frame(root)
frame.pack()

input_entry = tk.Entry(frame, width=40, font=("Arial", 10))
input_entry.pack(side="left", padx=5)

tk.Button(frame, text="Browse", command=choose_input).pack(side="left")


# Quality dropdown
tk.Label(root, text="Compression level:", font=("Arial", 11)).pack(pady=8)

quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(
    root,
    textvariable=quality_var,
    state="readonly",
    width=25,
    values=[
        "screen",     # smallest file
        "ebook",      # very small
        "printer",    # medium
        "prepress",   # high quality
        "default",    # balanced
    ],
)
quality_dropdown.pack()
quality_dropdown.current(0)  # default = screen


# Compress button
tk.Button(
    root,
    text="Compress PDF",
    font=("Arial", 13),
    command=start_compression
).pack(pady=12)


# Status
status_label = tk.Label(root, text="", font=("Arial", 11))
status_label.pack()


root.mainloop()
