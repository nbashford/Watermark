"""
Canvas frame
- displays the tk image of loaded image
- holds the PIL img for saving
- displays text or img logo supplied to main image
- actions taken on tk display image are mirrored to PIL image
"""
from tkinter import *
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
import fonts

NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')


class CanvasFrame(Canvas):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent  # reference to root

        # helper dictionary for overlaying passed logo to both tk and PIL image
        self.positions = {
            "Top left": [None, ["nw", "lt"]],
            "Top right": [None, ["ne", "rt"]],
            "Bottom left": [None, ["sw", "lb"]],
            "Bottom right": [None, ["se", "rb"]]
        }

        # class variables
        self.inverse_aspect_ratio = None  # ratio to resize displayed main tk canvas image
        self.tk_image = None  # current tk image
        self.PIL_image = None  # current PIL image
        self.canvas_image_text = None  # canvas text logo
        self.canvas_image_logo = None  # canvas img logo
        self.PIL_image_with_logo = None  # current PIL image with img or text logo

    def add_image(self, pil_image, max_width=800, max_height=600, portrait=False):
        """
        resizes the passed pil image to fit within the dimensions of the canvas frame.
        stores the reference to the resized tk image, and the inverse aspect ratio
        (ratio to reverse the resizing)
        :param pil_image: a PIL.Image photo
        :param max_width: max width of the canvas frame
        :param max_height: max height of the canvas frame
        :param portrait: if passed image is portrait or not
        :return none
        """
        self.PIL_image = pil_image.copy()  # store original img

        if portrait:  # decrease the max canvas dimensions to fit screen
            max_width = 700
            max_height = 530

        # Calculate aspect ratio
        aspect_ratio = min(max_width / pil_image.width, max_height / pil_image.height)
        # store the inverse aspect ratio
        self.inverse_aspect_ratio = max(pil_image.width / max_width, pil_image.height / max_height)
        # set new height and width for the display image
        new_width = int(pil_image.width * aspect_ratio)
        new_height = int(pil_image.height * aspect_ratio)

        # Resize image
        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_image)  # store the Tkinter image

        # Display the image in center of canvas frame
        self.create_image(new_width // 2, new_height // 2, image=self.tk_image)

        # Adjust canvas size to match max dimensions
        self.config(width=new_width, height=new_height)

        # update the position dictionary with new dimensions for logo placement
        self.update_positions(new_width, new_height)

    def update_positions(self, width, height, offset=0.07):
        """
        update logo position placement coordinates with new img dimensions
        :param width: displayed img width
        :param height: displayed img height
        :param offset: logo placement offset (%) off from img border
        :return: none
        """
        left_top_offset = 0 + offset
        right_bottom_offset = 1 - offset
        self.positions["Top left"][0] = (width*left_top_offset,
                                         height*left_top_offset)
        self.positions['Bottom left'][0] = (width*left_top_offset,
                                            height*right_bottom_offset)
        self.positions["Top right"][0] = (width*right_bottom_offset,
                                          height*left_top_offset)
        self.positions["Bottom right"][0] = (width*right_bottom_offset,
                                             height*right_bottom_offset)

    def add_logo(self, **kwargs):
        """
        Adds either text logo or img logo to main displayed tk image
        and hidden PIL image.
        For text:
         - kwarg arguments obtained
         - passed to the canvas create text function to add text to image
         - action is mirrored for the hidden PIL image to be saved
         - for PIL img the ttf file is obtained for the text
        For Img logo:
         - kwarg arguments obtained
         - canvas image is created and overlayed on displayed image
         - for PIl img - the location to add img is calculated
         - then the img is pasted over the PIL img
        :param kwargs: (for text logo) text, font, position, colour, size
        (for img logo) pil_logo, tk_logo, placement
        :return: none
        """
        self.remove_logo()  # remove any previous canvas text or overlay img
        self.PIL_image_with_logo = self.PIL_image.copy()  # copy orig pil img

        if kwargs.get('text'):  # for text logo
            # get kwargs
            text = kwargs.get('text')
            font = kwargs.get('font')
            position = kwargs.get('position')
            colour = kwargs.get('colour')
            size = kwargs.get('size')

            # Add text to Canvas Image
            self.canvas_image_text = self.create_text(self.positions[position][0][0], self.positions[position][0][1],
                             fill=colour, font=(font, size, "italic"), text=text, anchor=self.positions[position][1][0])

            # Add to PIL Image
            draw_text = ImageDraw.Draw(self.PIL_image_with_logo)  # Set up drawing
            ttf_fonts = fonts.FontTffFiles()
            ttf_file = ttf_fonts.get_font_ttf(font)  # Get the ttf file:
            # get font and calc proportional size
            font = ImageFont.truetype(ttf_file, size * self.inverse_aspect_ratio)
            rgb = ImageColor.getrgb(colour)  # get R,G,B for colour value
            # draw text on PIL image
            draw_text.text((self.positions[position][0][0] * self.inverse_aspect_ratio,
                            self.positions[position][0][1] * self.inverse_aspect_ratio),
                           text, rgb, anchor=self.positions[position][1][1], font=font)

        else:  # for img logo
            # get kwargs
            pil_logo = kwargs.get('pil_logo')
            tk_logo = kwargs.get('tk_logo')
            placement = kwargs.get('placement')

            # Add to the tk image
            self.canvas_image_logo = self.create_image(self.positions[placement][0][0],  # x
                                                       self.positions[placement][0][1],  # y
                                                       anchor=self.positions[placement][1][0],
                                                       image=tk_logo)

            # Add to the PIL image
            # - calc proportional logo placement
            # - PIL paste coordinates are for top left of pasted img
            # - for mimicking anchor placement options of tk image - need to subtract
            # - logo height and/or width for some placements
            if placement == "Top left":
                location = (self.positions[placement][0][0] * self.inverse_aspect_ratio,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio)
            elif placement == "Top right":
                location = (
                    self.positions[placement][0][0] * self.inverse_aspect_ratio - pil_logo.width,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio)
            elif placement == "Bottom left":
                location = (
                    self.positions[placement][0][0] * self.inverse_aspect_ratio,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio - pil_logo.height)
            elif placement == "Bottom right":
                location = (
                    self.positions[placement][0][0] * self.inverse_aspect_ratio - pil_logo.width,
                    self.positions[placement][0][1] * self.inverse_aspect_ratio - pil_logo.height)

            # round and int x, y coordinates
            x_placement, y_placement = location
            int_location = (int(round(x_placement)), int(round(y_placement)))
            # paste img onto main PIl img
            self.PIL_image_with_logo.paste(pil_logo, int_location, pil_logo)

    def remove_logo(self):
        """
        remove any canvas text or img logo
        :return: none
        """
        # remove logo from canvas image
        if self.canvas_image_text:
            self.delete(self.canvas_image_text)
        if self.canvas_image_logo:
            self.delete(self.canvas_image_logo)

    def get_PIL_image(self):
        """
        :return: the PIL image with logo added
        """
        return self.PIL_image_with_logo

    def get_img_dimensions(self):
        """
        returns the dimensions of the tk and PIL image,
        :return: tuple of dimension tuples, or none if no img loaded
        """
        if self.tk_image and self.PIL_image  # if image loaded
            tk_height = self.tk_image.height()
            tk_width = self.tk_image.width()
            tk_dims = (tk_width, tk_height)
            pil_height = self.PIL_image.height
            pil_width = self.PIL_image.width
            pil_dims = (pil_width, pil_height)
            return tk_dims, pil_dims
        else:  # no image loaded
            return False
