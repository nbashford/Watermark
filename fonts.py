import os
from PIL import ImageColor

fonts = ["Arial", "Courier", "Georgia", "Verdana", "Comic Sans MS", "Times New Roman"]


class FontTffFiles:

    def __init__(self, fonts=fonts):
        self.fonts = fonts
        self.fonts_dict = self.get_tff_files(self.fonts)

    def get_tff_files(self, fonts):

        font_ttf_list = []
        font_ttf_italic_list = []
        is_available = False

        for font in fonts:
            font_choice = []

            for font_ttf in os.listdir("/System/Library/Fonts"):
                if font in font_ttf:
                    font_choice.append(f"/System/Library/Fonts/{font_ttf}")
                    is_available = True
            for font_ttf in os.listdir("/System/Library/Fonts/Supplemental"):
                if font in font_ttf:
                    font_choice.append(f"/System/Library/Fonts/Supplemental/{font_ttf}")
                    is_available = True
            if not is_available:
                font_choice.append("None")

            font_choice.sort(key=len)

            italic = False
            for font_selection in font_choice:
                if 'Italic' in font_selection:
                    font_ttf_italic_list.append(font_selection)
                    italic = True
                    break
            ttf = False
            for font_selection in font_choice:
                if ".ttf" in font_selection:
                    font_ttf_list.append(font_selection)
                    ttf = True
                    break
            if not italic:
                font_ttf_italic_list.append("None")
            if not ttf:
                font_ttf_list.append("None")

            # print(f"{font}: {is_available}")

        tff_fonts = [[font_ttf_list[i], font_ttf_italic_list[i]] for i in range(len(font_ttf_list))]
        return dict(zip(fonts, tff_fonts))


    def get_fonts(self):
        return self.fonts

    def get_font_dict(self):
        return self.fonts_dict

    def get_font_ttf(self, font, italic=True):
        # if font:
        #     font = font.get('font')
        #     italic = font.get('italic')
        if font in self.fonts and italic:
            ttf_file = self.fonts_dict[font][1]
            if ttf_file == "None":
                ttf_file = self.fonts_dict[font][0]
        else:
            ttf_file = self.fonts_dict[font][0]
        return ttf_file


#
# fonts_class = FontTffFiles()
# print(fonts_class.fonts_dict)
#
# ttf = fonts_class.get_font_ttf('Arial', italic=False)
# ttf_italic = fonts_class.get_font_ttf('Arial')
#
# print(ttf)
# print(ttf_italic)
