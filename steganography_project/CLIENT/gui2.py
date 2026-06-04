import tkinter as tk
from tkinter import filedialog, messagebox
from client import send_request

# ================= COLORS =================
BG = "#ffe6f2"
BUTTON = "#ff3385"
ACCENT = "#ff99c8"
DARK = "#d1006f"
CARD = "#fff5fa"

# ================= WINDOW =================
root = tk.Tk()
root.title("Steganography System")
root.geometry("800x600")
root.configure(bg=BG)
root.resizable(False, False)

# ================= STATE =================
selected_hide_path = tk.StringVar()
selected_extract_path = tk.StringVar()
hide_method = tk.StringVar(value="lsb")
extract_method = tk.StringVar(value="lsb")
password_var = tk.StringVar()
message_var = tk.StringVar()
extract_password_var = tk.StringVar()
result_var = tk.StringVar()

# ================= SCREEN SWITCH =================
def show_frame(frame):
    result_var.set("")
    for f in (home_frame, hide_frame, extract_frame):
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# ================= FILE PICKERS =================
def browse_hide():
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
    if path:
        selected_hide_path.set(path)

def browse_extract():
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
    if path:
        selected_extract_path.set(path)

# ================= LSB PASSWORD TOGGLE =================
def toggle_hide_password(*args):
    if hide_method.get() == "lsb":
        hide_pass_frame.pack(pady=5)
    else:
        hide_pass_frame.pack_forget()

def toggle_extract_password(*args):
    if extract_method.get() == "lsb":
        extract_pass_frame.pack(pady=5)
    else:
        extract_pass_frame.pack_forget()

# ================= ACTIONS =================
def hide_message():
    if not selected_hide_path.get():
        messagebox.showerror("Error", "Please choose image")
        return

    msg = message_var.get()
    method = hide_method.get()
    password = password_var.get()

    try:
        response = send_request(
            action="hide",
            image_path=selected_hide_path.get(),
            method=method,
            text=msg,
            password=password
        )
        result_var.set(f"Saved file:\n{response}")

        messagebox.showinfo("Success", f"Message hidden successfully!\nSaved file:\n{response}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def extract_message():
    if not selected_extract_path.get():
        messagebox.showerror("Error", "Please choose image")
        return

    method = extract_method.get()
    password = extract_password_var.get()

    try:
        response = send_request(
            action="extract",
            image_path=selected_extract_path.get(),
            method=method,
            password=password
        )

        # אם השרת מחזיר טקסט
        result_var.set(str(response))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ================= HOME =================
home_frame = tk.Frame(root, bg=BG)

tk.Label(
    home_frame,
    text="🔐 Steganography System",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=DARK
).pack(pady=40)

tk.Button(
    home_frame,
    text="📝 Hide Message",
    font=("Arial", 14, "bold"),
    bg=BUTTON,
    fg="white",
    width=20,
    height=2,
    command=lambda: show_frame(hide_frame)
).pack(pady=20)

tk.Button(
    home_frame,
    text="🔍 Extract Message",
    font=("Arial", 14, "bold"),
    bg=BUTTON,
    fg="white",
    width=20,
    height=2,
    command=lambda: show_frame(extract_frame)
).pack(pady=10)

tk.Label(
    home_frame,
    text="Steganography Project",
    bg=BG,
    fg=DARK
).pack(side="bottom", pady=20)

# ================= HIDE SCREEN =================
hide_frame = tk.Frame(root, bg=BG)

tk.Label(hide_frame, text="📝 Hide Message", font=("Arial", 22, "bold"), bg=BG, fg=DARK).pack(pady=20)

tk.Button(hide_frame, text="← Back", bg=ACCENT, command=lambda: show_frame(home_frame)).pack(anchor="w", padx=20)

tk.Label(hide_frame, text="Choose Image", bg=BG).pack()
tk.Entry(hide_frame, textvariable=selected_hide_path, width=50).pack()
tk.Button(hide_frame, text="Browse", command=browse_hide, bg=ACCENT).pack(pady=5)

tk.Label(hide_frame, text="Secret Message", bg=BG).pack()
tk.Entry(hide_frame, textvariable=message_var, width=50).pack()

tk.Label(hide_frame, text="Method", bg=BG).pack()
tk.OptionMenu(hide_frame, hide_method, "lsb", "eof", "bitmap", "comseg", command=toggle_hide_password).pack()

hide_pass_frame = tk.Frame(hide_frame, bg=BG)
tk.Label(hide_pass_frame, text="Password", bg=BG).pack()
tk.Entry(hide_pass_frame, textvariable=password_var, show="*").pack()
hide_pass_frame.pack(pady=5)

tk.Button(
    hide_frame,
    text="🟣 Hide Message",
    bg=BUTTON,
    fg="white",
    command=hide_message
).pack(pady=20)

# ================= EXTRACT SCREEN =================
extract_frame = tk.Frame(root, bg=BG)

tk.Label(extract_frame, text="🔍 Extract Message", font=("Arial", 22, "bold"), bg=BG, fg=DARK).pack(pady=20)

tk.Button(extract_frame, text="← Back", bg=ACCENT, command=lambda: show_frame(home_frame)).pack(anchor="w", padx=20)

tk.Label(extract_frame, text="Choose Image", bg=BG).pack()
tk.Entry(extract_frame, textvariable=selected_extract_path, width=50).pack()
tk.Button(extract_frame, text="Browse", command=browse_extract, bg=ACCENT).pack(pady=5)

tk.Label(extract_frame, text="Method", bg=BG).pack()
tk.OptionMenu(extract_frame, extract_method, "lsb", "eof", "bitmap", "comseg", command=toggle_extract_password).pack()

extract_pass_frame = tk.Frame(extract_frame, bg=BG)
tk.Label(extract_pass_frame, text="Password", bg=BG).pack()
tk.Entry(extract_pass_frame, textvariable=extract_password_var, show="*").pack()
extract_pass_frame.pack(pady=5)

tk.Button(
    extract_frame,
    text="🔓 Extract Message",
    bg=BUTTON,
    fg="white",
    command=extract_message
).pack(pady=20)

tk.Label(extract_frame, text="Hidden Message:", bg=BG, fg=DARK).pack()
tk.Label(extract_frame, textvariable=result_var, bg=CARD, fg="black", wraplength=500).pack(pady=10)

# ================= START =================
show_frame(home_frame)
root.mainloop()