def hide_bitmap(img, plain_text, output_path):
    with open(img, "rb") as f:
        data = f.read()

    marker = b"||BITMAP||"

    with open(output_path, "wb") as f:
        f.write(data)
        f.write(marker)
        f.write(plain_text.encode("utf-8"))


def extract_bitmap(stego_path):
    with open(stego_path, "rb") as f:
        data = f.read()

    marker = b"||BITMAP||"
    idx = data.find(marker)

    if idx == -1:
        return ""

    return data[idx + len(marker):].decode("utf-8")