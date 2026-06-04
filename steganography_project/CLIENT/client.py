import socket
import json
from crypto_utils import encrypt_data, decrypt_data


def send_request(image_path, method, action,text="", password=""):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8000))

    # קריאת תמונה
    with open(image_path, "rb") as f:
        img_bytes = f.read()


    img_format = image_path.split(".")[-1]

    # יצירת Header עם פרטי הבקשה
    header = {
        "action": action,
        "method": method,
        "text": text if action == "hide" else "",
        "password": password,
        "format": img_format,
        "size": len(img_bytes)
    }

    # שליחת header + image

    # המרת ה-header לבייטים
    header_bytes = json.dumps(header).encode()
    # הצפנת ה-header
    encrypted_header = encrypt_data(header_bytes)
    # חישוב גודל ההודעה
    header_size = len(encrypted_header).to_bytes(4, "big")
    # הצפנת התמונה
    encrypted_image = encrypt_data(img_bytes)
    # חישוב גודל התמונה המוצפנת
    image_size = len(encrypted_image).to_bytes(8, "big")

    # ===== שליחת הנתונים לשרת =====

    # שליחת גודל ה-header
    client.sendall(header_size)
    # שליחת ה-header המוצפן
    client.sendall(encrypted_header)
    # שליחת גודל התמונה
    client.sendall(image_size)
    # שליחת התמונה המוצפנת
    client.sendall(encrypted_image)

    # קבלת תשובה
    result = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        result += chunk
    result = decrypt_data(result)

    # ===== טיפול בתשובה =====
    if action == "hide":

        output_name = f"output_from_server.{img_format}"

        with open(output_name, "wb") as f:
            f.write(result)

        client.close()

        return output_name

    elif action == "extract":

        hidden_message = result.decode(errors="ignore")

        client.close()

        return hidden_message


if __name__ == "__main__":
    path = input("Enter image path: ")
    action = input("Choose action (hide/extract): ")
    method = input("Choose method (eof/bitmap/comseg/lsb): ")

    text = ""
    if action == "hide":
        text = input("Enter message: ")

    send_request(path, text, method, action)