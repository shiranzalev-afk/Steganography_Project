from pathlib import Path

MAGIC = b"EOFSTEG1"


def hide_eof(carrier_path: str, secret_path: str, output_path: str):
    carrier = Path(carrier_path).read_bytes()
    secret = Path(secret_path).read_bytes()

    length_bytes = len(secret).to_bytes(8, byteorder="big")
    stego_data = carrier + MAGIC + length_bytes + secret

    Path(output_path).write_bytes(stego_data)


def extract_eof(stego_path: str, output_secret_path: str):
    data = Path(stego_path).read_bytes()

    idx = data.rfind(MAGIC)

    if idx == -1:
        raise ValueError("No hidden data found.")

    length_start = idx + len(MAGIC)
    length_end = length_start + 8

    secret_len = int.from_bytes(data[length_start:length_end], byteorder="big")

    secret_start = length_end
    secret_end = secret_start + secret_len

    secret = data[secret_start:secret_end]

    Path(output_secret_path).write_bytes(secret)