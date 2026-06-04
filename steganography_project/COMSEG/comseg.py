import os

SOI = b"\xFF\xD8"
EOI = b"\xFF\xD9"


def find_com_segment(data):
    """
    מחפש COM segment בקובץ JPEG
    מחזיר (start, end) אם קיים, אחרת (-1, -1)
    """

    if not data.startswith(SOI):
        return -1, -1

    i = 2

    while i < len(data) - 1:

        if data[i] == 0xFF and data[i + 1] == 0xFE:
            start = i
            length = int.from_bytes(data[i + 2:i + 4], "big")
            end = start + 2 + length
            return start, end

        if data[i] == 0xFF and data[i + 1] == 0xD9:
            break

        i += 1

    return -1, -1


def hide_comseg(image_path, message, output_path):
    """
    מסתיר הודעה בתוך COM segment
    """

    with open(image_path, "rb") as f:
        data = f.read()

    message_bytes = message.encode("utf-8")
    length = len(message_bytes).to_bytes(2, "big")

    com_segment = b"\xFF\xFE" + length + message_bytes

    start, end = find_com_segment(data)

    # אין COM → מוסיפים לפני סוף התמונה
    if start == -1:
        eoi_index = data.rfind(EOI)
        new_data = data[:eoi_index] + com_segment + data[eoi_index:]

    # יש COM → מחליפים
    else:
        new_data = data[:start] + com_segment + data[end:]

    with open(output_path, "wb") as f:
        f.write(new_data)


def extract_comseg(image_path):
    """
    שולף הודעה מתוך COM segment
    """

    with open(image_path, "rb") as f:
        data = f.read()

    i = 0

    while i < len(data) - 1:

        if data[i] == 0xFF and data[i + 1] == 0xFE:

            length = int.from_bytes(data[i + 2:i + 4], "big")
            message = data[i + 4:i + 4 + length]

            return message.decode("utf-8", errors="ignore")

        i += 1

    return "No COMSEG message found"