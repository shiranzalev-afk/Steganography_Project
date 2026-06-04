from METHODS.stego_base import StegoMethod

MAGIC = b"EOFSTEG1"


class EOFMethod(StegoMethod):

    def hide(self, data, text, output_file=None):

        secret = text.encode("utf-8")

        length = len(secret).to_bytes(8, "big")

        return data + MAGIC + length + secret

    def extract(self, data):

        idx = data.rfind(MAGIC)

        if idx == -1:
            return b""

        length_start = idx + len(MAGIC)
        length_end = length_start + 8

        size = int.from_bytes(
            data[length_start:length_end],
            "big"
        )

        return data[length_end:length_end + size]