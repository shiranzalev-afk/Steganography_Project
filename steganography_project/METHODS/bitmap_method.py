from METHODS.stego_base import StegoMethod


class BitmapMethod(StegoMethod):

    def hide(self, input_file, text, output_file):

        # קריאת קובץ התמונה המקורי
        with open(input_file, "rb") as f:
            data = f.read()

        # סימון מיוחד שמפריד בין התמונה למידע המוסתר
        marker = b"||BITMAP||"

        # יצירת קובץ חדש
        with open(output_file, "wb") as f:
            # כתיבת התמונה המקורית
            f.write(data)
            # כתיבת הסימון
            f.write(marker)
            # כתיבת הטקסט המוסתר
            f.write(text.encode("utf-8"))

    def extract(self, input_file):

        with open(input_file, "rb") as f:
            data = f.read()

        marker = b"||BITMAP||"

        idx = data.find(marker)

        if idx == -1:
            return ""

        return data[idx + len(marker):].decode("utf-8")