from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
import fonts
import save_pil

NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')

class CanvasFrame(Canvas):
    def __init__(self, parent):
        super().__init__(parent)

        # self.config(borderwidth="2")
        self.parent = parent
        self.positions = {
            "Top left": [None, ["nw", "lt"]],
            "Top right": [None, ["ne", "rt"]],
            "Bottom left": [None, ["sw", "lb"]],
            "Bottom right": [None, ["se", "rb"]]
        }

        self.tk_image = None
        self.PIL_image = None
        self.PIL_image_with_logo = None
        self.inverse_aspect_ratio = None
        self.canvas_image_text = None

        self.canvas_image_logo = None
        self.overlay_image = None
        self.PIL_image_plus_image = None

    def add_image(self, pil_image, max_width=800, max_height=600):

        self.PIL_image = pil_image
        # Calculate aspect ratio and get new height and width for the image
        aspect_ratio = min(max_width / pil_image.width, max_height / pil_image.height)
        self.inverse_aspect_ratio = max(pil_image.width/max_width, pil_image.height / max_height)
        new_width = int(pil_image.width * aspect_ratio)
        new_height = int(pil_image.height * aspect_ratio)

        # Resize image
        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        self.tk_image = tk_image  # store the Tkinter canvas image

        # Display the image on the canvas
        self.create_image(new_width // 2, new_height // 2, image=tk_image)

        # Adjust canvas size to match max dimensions
        self.config(width=new_width, height=new_height)

        self.update_positions(new_width, new_height)

    def update_positions(self, width, height):
        self.positions["Top left"][0] = (width*0.07, height*0.07)
        self.positions['Bottom left'][0] = (width*0.07, height*0.93)
        self.positions["Top right"][0] = (width*0.93, height*0.07)
        self.positions["Bottom right"][0] = (width*0.93, height*0.93)

    # def add_logo(self, text, font, position, colour, size):
    #
    #     self.remove_logo()
    #
    #     # Add to TKinter Canvas Image
    #     self.canvas_image_text = self.create_text(self.positions[position][0], self.positions[position][1],
    #                      fill=colour, font=(font, size, "italic"), text=text)
    #
    #     # Add to PIL Image (Hidden) - for saving
    #     # Make a Copy of the PIL image - since no way to remove text from PIL image
    #     self.PIL_image_plus_text = self.PIL_image.copy()
    #     # Set up drawing on image
    #     draw_text = ImageDraw.Draw(self.PIL_image_plus_text)
    #     # Get the ttf file:
    #     ttf_fonts = fonts.FontTffFiles()
    #     ttf_file = ttf_fonts.get_font_ttf(font)
    #     # set up font and calc size of font relative to aspect ratio
    #     font = ImageFont.truetype(ttf_file, size * self.inverse_aspect_ratio)
    #     # get the R,G,B for the colour
    #     rgb = ImageColor.getrgb(colour)
    #     # draw the text on the PIL image - relative position of tkinter image to PIL image (aspect ratio)
    #     draw_text.text((self.positions[position][0] * self.inverse_aspect_ratio,
    #                     self.positions[position][1] * self.inverse_aspect_ratio),
    #                    text, rgb, anchor="mm", font=font)

    def add_logo(self, **kwargs):

        self.remove_logo()
        self.PIL_image_with_logo = self.PIL_image.copy()

        if kwargs.get('text'):
            text = kwargs.get('text')
            font = kwargs.get('font')
            position = kwargs.get('position')
            colour = kwargs.get('colour')
            size = kwargs.get('size')

            # Add to TKinter Canvas Image
            self.canvas_image_text = self.create_text(self.positions[position][0][0], self.positions[position][0][1],
                             fill=colour, font=(font, size, "italic"), text=text, anchor=self.positions[position][1][0])

            # Add to PIL Image (Hidden) - for saving
            # Set up drawing on image
            draw_text = ImageDraw.Draw(self.PIL_image_with_logo)
            # Get the ttf file:
            ttf_fonts = fonts.FontTffFiles()
            ttf_file = ttf_fonts.get_font_ttf(font)
            # set up font and calc size of font relative to aspect ratio
            font = ImageFont.truetype(ttf_file, size * self.inverse_aspect_ratio)
            # get the R,G,B for the colour
            rgb = ImageColor.getrgb(colour)
            # draw the text on the PIL image - relative position of tkinter image to PIL image (aspect ratio)
            draw_text.text((self.positions[position][0][0] * self.inverse_aspect_ratio,
                            self.positions[position][0][1] * self.inverse_aspect_ratio),
                           text, rgb, anchor=self.positions[position][1][1], font=font)
        else:
            # here for Image logo placement
            pil_logo = kwargs.get('pil_logo')
            tk_logo = kwargs.get('tk_logo')
            placement = kwargs.get('placement')
            # scale = kwargs.get('scale')


            # Add to the tk image
            self.overlay_image = self.create_image(self.positions[placement][0][0], self.positions[placement][0][1],
                              anchor=self.positions[placement][1][0], image=tk_logo)

            # Add to the PIL image
            if placement == "Top left":
                location = (self.positions[placement][0][0] * self.inverse_aspect_ratio,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio)
            elif placement == "Top right":
                location =(
                    self.positions[placement][0][0] * self.inverse_aspect_ratio - pil_logo.width,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio)
            elif placement == "Bottom left":
                location =(
                    self.positions[placement][0][0] * self.inverse_aspect_ratio,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio - pil_logo.height)
            elif placement == "Bottom right":
                location = (
                    self.positions[placement][0][0] * self.inverse_aspect_ratio - pil_logo.width,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio - pil_logo.height)

            x_placement, y_placement = location
            int_location = (int(round(x_placement)), int(round(y_placement)))
            self.PIL_image_with_logo.paste(pil_logo, int_location, pil_logo)


    def remove_logo(self):
        # remove logo from canvas image
        if self.canvas_image_text:
            self.delete(self.canvas_image_text)
        if self.overlay_image:
            self.delete(self.overlay_image)

    def get_PIL_image(self):
        return self.PIL_image_with_logo

    def get_img_dimensions(self):

        if self.tk_image and self.PIL_image:

            tk_height = self.tk_image.height()
            tk_width = self.tk_image.width()
            tk_dims = (tk_width, tk_height)
            pil_height = self.PIL_image.height
            pil_width = self.PIL_image.width
            pil_dims = (pil_width, pil_height)

            return tk_dims, pil_dims

        else:
            return False
