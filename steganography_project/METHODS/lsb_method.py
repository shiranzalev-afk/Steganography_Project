import imageio.v2 as imageio

from METHODS.stego_base import StegoMethod
from LSB.encrypt import Encryptor
from LSB.decrypt import Decryptor


class LSBMethod(StegoMethod):

    def hide(
            self,
            input_file,
            text,
            output_file,
            password
    ):

        # קריאת התמונה כמערך פיקסלים
        im = imageio.imread(input_file).astype("uint8")

        # יצירת אובייקט הצפנה עם סיסמה
        enc = Encryptor(password)

        # ביצוע ההסתרה בתוך התמונה
        enc.encrypt(
            im,
            text,
            output_file
        )

    def extract(
            self,
            input_file,
            password
    ):

        im = imageio.imread(input_file)

        dec = Decryptor(password)

        return dec.decrypt(im)