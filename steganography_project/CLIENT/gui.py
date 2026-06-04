import tkinter as tk
from tkinter import filedialog, messagebox
from client import send_request

# ===================== COLORS =====================
BG = "#ffe6f2"
DARK = "#d1006f"
BUTTON = "#ff3385"
ACCENT = "#ff99c8"


# ===================== FILE DIALOG =====================

def choose_file():
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
    )
    if path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, path)


# ===================== UI UPDATE =====================

def update_ui(*args):
    """Show/hide fields depending on mode + method"""

    # password only for LSB
    if method_var.get() == "lsb":
        password_frame.pack(pady=8)
    else:
        password_frame.pack_forget()
        entry_password.delete(0, tk.END)

    # message only for hide
    if action_var.get() == "hide":
        message_frame.pack(pady=8)
    else:
        message_frame.pack_forget()
        entry_message.delete(0, tk.END)

    result_label.config(text="")


# ===================== RUN ACTION =====================

def run_action():
    path = entry_path.get()
    method = method_var.get()
    password = entry_password.get()
    action = action_var.get()

    if not path:
        messagebox.showerror("Error", "Please choose an image")
        return

    if action == "hide":
        text = entry_message.get()
        if not text:
            messagebox.showerror("Error", "Please enter a message")
            return
    else:
        text = ""

    if method == "lsb" and not password:
        messagebox.showerror("Error", "Please enter password")
        return

    try:
        result = send_request(path, text, method, action, password)

        if action == "hide":
            result_label.config(
                text=f"✅ Image created successfully!\nSaved as:\n{result}"
            )
            messagebox.showinfo("Success", "Image created successfully!")
        else:
            result_label.config(
                text=f"🔓 Hidden Message:\n\n{result}"
            )
            messagebox.showinfo("Done", "Message extracted successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ===================== WINDOW =====================
root = tk.Tk()
root.title("Steganography System")
root.geometry("650x650")
root.configure(bg=BG)

# ===================== SCROLL AREA =====================
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg=BG)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# ===================== TITLE =====================

tk.Label(
    scroll_frame,
    text="🔐 Steganography System",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=DARK
).pack(pady=20)

# ===================== ACTION =====================

action_var = tk.StringVar(value="hide")

mode_frame = tk.Frame(scroll_frame, bg=BG)
mode_frame.pack(pady=10)

tk.Label(
    mode_frame,
    text="Choose Action:",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=DARK
).pack()

tk.Radiobutton(
    mode_frame,
    text="Hide Message",
    variable=action_var,
    value="hide",
    command=update_ui,
    bg=BG,
    fg=DARK,
    selectcolor=ACCENT
).pack()

tk.Radiobutton(
    mode_frame,
    text="Extract Message",
    variable=action_var,
    value="extract",
    command=update_ui,
    bg=BG,
    fg=DARK,
    selectcolor=ACCENT
).pack()

# ===================== FILE =====================

file_frame = tk.Frame(scroll_frame, bg=BG)
file_frame.pack(pady=10)

tk.Label(
    file_frame,
    text="Choose Image:",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=DARK
).pack()

entry_path = tk.Entry(file_frame, width=45, font=("Arial", 11))
entry_path.pack(pady=5)

tk.Button(
    file_frame,
    text="Browse",
    command=choose_file,
    bg=BUTTON,
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
).pack(pady=5)

# ===================== METHOD =====================

method_var = tk.StringVar(value="lsb")

method_frame = tk.Frame(scroll_frame, bg=BG)
method_frame.pack(pady=10)

tk.Label(
    method_frame,
    text="Choose Method:",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=DARK
).pack()

tk.OptionMenu(
    method_frame,
    method_var,
    "lsb",
    "bitmap",
    "comseg",
    "eof",
    command=update_ui
).pack()

# ===================== MESSAGE =====================

message_frame = tk.Frame(scroll_frame, bg=BG)

tk.Label(
    message_frame,
    text="Secret Message:",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=DARK
).pack()

entry_message = tk.Entry(message_frame, width=45, font=("Arial", 11))
entry_message.pack()

# ===================== PASSWORD =====================

password_frame = tk.Frame(scroll_frame, bg=BG)

tk.Label(
    password_frame,
    text="LSB Password:",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=DARK
).pack()

entry_password = tk.Entry(password_frame, show="*", width=35, font=("Arial", 11))
entry_password.pack()

# ===================== RUN BUTTON (BOTTOM) =====================

run_button_frame = tk.Frame(scroll_frame, bg=BG)
run_button_frame.pack(pady=30)

tk.Button(
    run_button_frame,
    text="▶ Run Action",
    command=run_action,
    bg=BUTTON,
    fg="white",
    font=("Arial", 14, "bold"),
    width=20,
    height=2
).pack()

# ===================== RESULT =====================

result_label = tk.Label(
    scroll_frame,
    text="",
    bg=BG,
    fg=DARK,
    font=("Arial", 12, "bold"),
    justify="center"
)
result_label.pack(pady=20)

# ===================== INIT =====================

update_ui()
root.mainloop()
