import socket
import json
import os
import imageio.v2 as imageio
from pathlib import Path
import threading
from crypto_utils import encrypt_data, decrypt_data

from METHODS.bitmap_method import BitmapMethod
from METHODS.comseg_method import ComsegMethod
from METHODS.eof_method import EOFMethod
from METHODS.lsb_method import LSBMethod

MAGIC = b"EOFSTEG1"

bitmap_method = BitmapMethod()
comseg_method = ComsegMethod()
eof_method = EOFMethod()
lsb_method = LSBMethod()

# ===== EOF =====
def hide_eof_bytes(data, text):
    secret = text.encode("utf-8")
    length = len(secret).to_bytes(8, "big")
    return data + MAGIC + length + secret


def extract_eof_bytes(data):
    idx = data.rfind(MAGIC)
    if idx == -1:
        return b""
    length_start = idx + len(MAGIC)
    length_end = length_start + 8
    size = int.from_bytes(data[length_start:length_end], "big")
    return data[length_end:length_end + size]


# ===== SERVER =====
def handle_client(client_socket):
    try:
        # ===== קבלת header =====
        encrypted_header_size = client_socket.recv(4)

        header_size = int.from_bytes(
            encrypted_header_size,
            "big"
        )

        encrypted_header = client_socket.recv(header_size)

        header = decrypt_data(
            encrypted_header
        ).decode()

        request = json.loads(header)


        action = request["action"]
        method = request["method"]
        text = request.get("text", "")
        password = request.get("password", "1234")
        size = request["size"]
        img_format = request["format"]


        # ===== קבלת גודל תמונה מוצפנת =====
        encrypted_image_size = client_socket.recv(8)

        image_size = int.from_bytes(
            encrypted_image_size,
            "big"
        )

        # ===== קבלת תמונה מוצפנת =====
        encrypted_img = b""

        while len(encrypted_img) < image_size:
            chunk = client_socket.recv(4096)

            if not chunk:
                break

            encrypted_img += chunk

        # ===== פענוח =====
        img_bytes = decrypt_data(encrypted_img)

        # ===== שמירה לפי פורמט אמיתי =====
        input_file = f"temp_input_{threading.get_ident()}.{img_format}"
        with open(input_file, "wb") as f:
            f.write(img_bytes)

        output_file = None

        # ================= HIDE =================
        if action == "hide":

            if method == "eof":
                result_bytes = eof_method.hide(
                    img_bytes,
                    text
                )


            elif method == "bitmap":
                output_file = f"output_{threading.get_ident()}.bmp"
                bitmap_method.hide(
                    input_file,
                    text,
                    output_file
                )
                result_bytes = Path(output_file).read_bytes()

            elif method == "comseg":
                output_file = f"output_{threading.get_ident()}.jpg"
                comseg_method.hide(
                    input_file,
                    text,
                    output_file
                )
                result_bytes = Path(output_file).read_bytes()

            elif method == "lsb":
                output_file = f"output_{threading.get_ident()}.png"
                lsb_method.hide(
                    input_file,
                    text,
                    output_file,
                    password
                )
                result_bytes = Path(output_file).read_bytes()

            else:
                client_socket.send(b"ERROR: unknown method")
                return

            encrypted_result = encrypt_data(result_bytes)

            client_socket.sendall(encrypted_result)

        # ================= EXTRACT =================
        elif action == "extract":

            if method == "eof":
                result = eof_method.extract(
                    img_bytes
                )


            elif method == "bitmap":
                result = bitmap_method.extract(input_file).encode()

            elif method == "comseg":
                result = comseg_method.extract(
                    input_file
                ).encode()

            elif method == "lsb":
                result = lsb_method.extract(
                    input_file,
                    password
                ).encode()

            else:
                result = b"ERROR: unknown method"

            result = encrypt_data(result)
            client_socket.sendall(result)

        # ===== ניקוי =====
        if os.path.exists(input_file):
            os.remove(input_file)
        for f in [input_file, output_file]:
            if os.path.exists(f):
                os.remove(f)

    except Exception as e:
        print("Server error:", e)

    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8000))
    server.listen(5)

    print("Server running on port 8000...")

    while True:

        # המתנה להתחברות לקוח
        client, addr = server.accept()
        print("Connected:", addr)

        # יצירת תהליכון חדש עבור הלקוח
        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )
        # הפעלת התהליכון
        thread.start()


if __name__ == "__main__":
    start_server()