"""
gets ttf files for the given fonts from Mac system
- can pass fonts to get other ttf files
"""
import os

# fonts from tkinter application - others can be supplied
provided_fonts = ["Arial", "Courier", "Georgia", "Verdana", "Comic Sans MS", "Times New Roman"]


class FontTffFiles:

    def __init__(self, fonts=provided_fonts):
        self.fonts = fonts
        self.fonts_dict = self.get_tff_files(self.fonts)

    def get_tff_files(self, fonts):
        """
        searches through the two directories on Mac os to file the ttf files
        that match the provided font name.
        gets the normal ttf file and italic ttf file
        - gets the shortest ttf file name matching given font name
        :param fonts: list of fonts
        :return: dictionary mapping original font name to ttf file and italic ttf file
        """
        font_ttf_list = []  # normal fonts
        font_ttf_italic_list = []  # italic fonts
        is_available = False

        for font in fonts:
            font_choice = []
            for font_ttf in os.listdir("/System/Library/Fonts"):
                if font in font_ttf:
                    # add ttf file if name contains font name
                    font_choice.append(f"/System/Library/Fonts/{font_ttf}")
                    is_available = True
            for font_ttf in os.listdir("/System/Library/Fonts/Supplemental"):
                if font in font_ttf:
                    # add ttf file if name contains font name
                    font_choice.append(f"/System/Library/Fonts/Supplemental/{font_ttf}")
                    is_available = True
            if not is_available:
                # add "None" if not ttf file contains file name
                font_choice.append("None")
            # sort by length
            font_choice.sort(key=len)

            # sort into normal and italic - gets shortest of each
            italic = False
            for font_selection in font_choice:
                if 'Italic' in font_selection:
                    # adds first (shortest) italic ttf file
                    font_ttf_italic_list.append(font_selection)
                    italic = True
                    break
            ttf = False
            for font_selection in font_choice:
                if ".ttf" in font_selection:
                    # adds first (shortest) normal ttf file
                    font_ttf_list.append(font_selection)
                    ttf = True
                    break
            if not italic:  # add none
                font_ttf_italic_list.append("None")
            if not ttf:  # add none
                font_ttf_list.append("None")

        # nested list of normal and italic ttf files for each file
        tff_fonts = [[font_ttf_list[i], font_ttf_italic_list[i]] for i in range(len(font_ttf_list))]
        # return dictionary mapping of font name to ttf files
        return dict(zip(fonts, tff_fonts))

    def get_fonts(self):
        """
        returns font names
        """
        return self.fonts

    def get_font_dict(self):
        """
        :return: dictionary mapping or font names to ttf files
        """
        return self.fonts_dict

    def get_font_ttf(self, font, italic=True):
        """
        gets the normal or italic ttf file for the passed font name
        if available
        :param font: name of font
        :param italic: if wanted ttf file is italic
        :return: ttf file for the font
        """
        if italic:
            # get italic ttf file
            ttf_file = self.fonts_dict[font][1]
            if ttf_file == "None":
                # pass the none italic if none
                ttf_file = self.fonts_dict[font][0]
        else:
            # normal ttf file
            ttf_file = self.fonts_dict[font][0]
        return ttf_file
