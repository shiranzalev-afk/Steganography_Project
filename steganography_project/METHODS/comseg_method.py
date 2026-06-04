from METHODS.stego_base import StegoMethod
from COMSEG.comseg import hide_comseg, extract_comseg


class ComsegMethod(StegoMethod):

    def hide(self, input_file, text, output_file):

        hide_comseg(
            input_file,
            text,
            output_file
        )

    def extract(self, input_file):

        return extract_comseg(input_file)