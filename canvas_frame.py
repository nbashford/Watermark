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
            "Top left": None,
            "Top right": None,
            "Bottom left": None,
            "Bottom right": None
        }

        self.tk_image = None
        self.PIL_image = None
        self.PIL_image_plus_text = None
        self.inverse_aspect_ratio = None
        self.canvas_image_text = None

        # self.config(width=400, height=270, highlightthickness=1, border=1)
        # self.config(background='blue')

    def add_image(self, pil_image, max_width=800, max_height=600):

        self.PIL_image = pil_image
        # Calculate aspect ratio and get new height and width for the image
        aspect_ratio = min(max_width / pil_image.width, max_height / pil_image.height)
        self.inverse_aspect_ratio = max(pil_image.width/max_width, pil_image.height / max_height)
        # print(aspect_ratio)
        # print(pil_image.width/max_width)
        # print(pil_image.height / max_height)
        new_width = int(pil_image.width * aspect_ratio)
        new_height = int(pil_image.height * aspect_ratio)

        # Resize image
        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        # self.PIL_image = resized_image  # store the PIL image
        # print(f"Width PIL Image: {resized_image.width}\nHeight PIL Image: {resized_image.height}")
        # print(new_width, new_height)
        tk_image = ImageTk.PhotoImage(resized_image)
        self.tk_image = tk_image  # store the Tkinter canvas image
        # print(f"Width Tkinter Image: {tk_image.width()}\nHeight Tkinter Image: {tk_image.height()}")

        # Display the image on the canvas
        #self.create_image(max_width // 2, max_height // 2, image=tk_image)
        self.create_image(new_width // 2, new_height // 2, image=tk_image)

        # Adjust canvas size to match max dimensions
        self.config(width=new_width, height=new_height)

        self.update_positions(new_width, new_height)

    def update_positions(self, width, height):
        self.positions["Top left"] = (width*0.1, height*0.1)
        self.positions['Bottom left'] = (width*0.1, height*0.9)
        self.positions["Top right"] = (width*0.9, height*0.1)
        self.positions["Bottom right"] = (width*0.9, height*0.9)





    def add_logo(self, text, font, position, colour, size):

        self.remove_logo()

        # Add to TKinter Canvas Image
        self.canvas_image_text = self.create_text(self.positions[position][0], self.positions[position][1],
                         fill=colour, font=(font, size, "italic"), text=text)

        # Add to PIL Image (Hidden) - for saving
        # Make a Copy of the PIL image - since no way to remove text from PIL image
        self.PIL_image_plus_text = self.PIL_image.copy()
        # Set up drawing on image
        draw_text = ImageDraw.Draw(self.PIL_image_plus_text)
        # Get the ttf file:
        ttf_fonts = fonts.FontTffFiles()
        ttf_file = ttf_fonts.get_font_ttf(font)
        # set up font and calc size of font relative to aspect ratio
        font = ImageFont.truetype(ttf_file, size * self.inverse_aspect_ratio)
        # get the R,G,B for the colour
        rgb = ImageColor.getrgb(colour)
        # draw the text on the PIL image - relative position of tkinter image to PIL image (aspect ratio)
        draw_text.text((self.positions[position][0] * self.inverse_aspect_ratio,
                        self.positions[position][1] * self.inverse_aspect_ratio),
                       text, rgb, anchor="mm", font=font)

        #self.PIL_image_plus_text.save('./edited_images/sample-out.jpg')


    def remove_logo(self):
        # remove logo from canvas image
        if self.canvas_image_text:
            self.delete(self.canvas_image_text)

    def get_PIL_image(self):
        return self.PIL_image_plus_text