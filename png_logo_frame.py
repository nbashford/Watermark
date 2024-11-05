"""
Frame within Notebook tab
- for loading img files for overlaying image logos
"""
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import re

NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')


class ImgLogoFrame(Frame):
    def __init__(self, root, tab):
        super().__init__(tab)

        self.parent = root  # reference to root Tk

        # *** Frame set up -------------------------
        self.pack(fill='both', expand=True)
        self.pack_propagate(False)
        # grid set up
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # variables for image_logo
        self.img_folder = './img_logo_folder'  # folder name to store loaded img logos
        self.image_logo = None  # name of current img file
        self.image_PIL = None  # current image as PIL image
        self.image_logo_resized_tk = None  # logo image resized for tk canvas
        self.image_logo_resized_PIL = None  # logo image resized for PIL

        # *** Widgets ------------------------------
        # load png button
        self.load_img_file = Button(self,
                                    text="Add PNG file",
                                    fg='black', font=BOLD_FONT,
                                    command=self.upload_img_file)
        self.load_img_file.grid(row=0, column=0, padx=10, pady=10)

        # seperator
        self.seperator = ttk.Separator(self, orient="horizontal")
        self.seperator.grid(row=1, columnspan=3, sticky="ew", pady=10)

        # option menu for selecting img files
        self.img_files = self.get_img_files()  # list of files in img_folder
        self.img_var = StringVar()
        self.img_var.set("Select PNG file")
        self.select_img_option = OptionMenu(self,
                                            self.img_var,
                                            *self.img_files,
                                            command=self.activate_add_logo)
        self.select_img_option.grid(row=2, column=0, padx=10, pady=10)

        # img placement option menu
        self.orientations = ["Top left", "Top right", "Bottom right", "Bottom left"]
        self.orientation_var = StringVar(self)
        self.orientation_var.set("Logo Placement")
        self.logo_orientation = OptionMenu(self,
                                           self.orientation_var,
                                           *self.orientations,
                                           command=self.activate_add_logo
                                           )
        self.logo_orientation.grid(row=2, column=1, padx=10, pady=10)
        self.logo_orientation.config(width=10)

        # img size
        self.sizes = ["25%", "50%", "75%", "100%", "125%", "150%", "175%", "200%", "300%"]
        self.size_var = StringVar(self)
        self.size_var.set("Logo size")
        self.size_choice = OptionMenu(self,
                                        self.size_var,
                                        *self.sizes,
                                        command=self.activate_add_logo
                                      )
        self.size_choice.grid(row=2, column=2, padx=10, pady=10)
        self.size_choice.config(width=10)

        # seperator
        self.seperator = ttk.Separator(self, orient="horizontal")
        self.seperator.grid(row=3, columnspan=3, sticky="ew", pady=10)

        # add img logo to tkinter and PIL image button
        self.add_logo_button = Button(self,
                                      text="Add Logo",
                                      fg='black',
                                      bg='green',
                                      width=10,
                                      font=BOLD_FONT,
                                      state=DISABLED,
                                      command=self.add_img_logo)
        self.add_logo_button.grid(row=4, column=0, padx=10, pady=10)

        # save image with logo button
        self.save_button = Button(self, text="Save Image",
                                  fg='black',
                                  bg='blue',
                                  width=10,
                                  font=BOLD_FONT,
                                  state=DISABLED,
                                  command=self.parent.save_image)
        self.save_button.grid(row=4, column=2)

    def get_img_files(self):
        """
        gets all files from img_logo_folder as list
        - returns list if files loaded
        - else: returns placeholder text
        """
        if len(self.parent.get_file_names(self.img_folder)) > 0:
            return self.parent.get_file_names(self.img_folder)
        else:  # placeholder
            return ["Add Image Logo Above"]

    def upload_img_file(self):
        """
        calls root browse_files functions to load file to passed
        img folder
        calls update img option menu to display file names
        """
        self.parent.browse_files(self.img_folder)  # upload file
        self.update_img_option_menu()

    def update_img_option_menu(self):
        """
        updates the img file option menu with the names of files in the img folder
        """
        self.img_files = self.get_img_files()
        menu = self.select_img_option["menu"]
        menu.delete(0, "end")  # deletes current option menu labels

        for file in self.img_files:
            menu.add_command(label=file,
                             command=lambda value=file:
                             (self.img_var.set(value), self.activate_add_logo(value)))

    def activate_add_logo(self, choice):
        """
        activates button to add img logo to main image if option menus selected
        (No placeholder text selected)
        """
        if (re.sub(r"[()',]", "", self.img_var.get()) in self.img_files
                and self.size_var.get() in self.sizes
                and self.orientation_var.get() in self.orientations):
            self.add_logo_button.config(state=NORMAL)

    def create_image_logo_PIL(self):
        """
        creates a PIL image from the selected option menu file.
        Displays error if unable to open
        """
        # get var for file options
        img_choice = self.img_var.get()
        self.image_logo = re.sub(r"[()',]", "", img_choice)
        img_path = f"{self.img_folder}/{self.image_logo}"
        try:
            self.image_PIL = Image.open(img_path).convert("RGBA")
            return True
        except (FileNotFoundError, ValueError, TypeError) as e:
            self.parent.show_help(title="Open Img Error",
                                  message=f"Image: {self.image_logo}\n"
                                          f"was not able to be loaded."
                                          f"\n\n{e}")
            return False

    def resize_logo_image(self, scale=0.2, ratio=1.0):
        """
        resizes the loaded image logo to x% scale of the display image
        - for both tk canvas and PIL image - since each has different dimensions
        - img scale adjusted if logo size value is passed as ratio
        """
        scale = scale * ratio
        if self.create_image_logo_PIL(): # make sure image logo has been added
            # get TK and PIL dimensions from canvas
            tk_dims, pil_dims = self.parent.get_tk_pil_dimensions()
            # calc ratio for scaling down logo image against both TK and PIL images
            tk_ratio = max(self.image_PIL.width/(tk_dims[0]*scale),
                           self.image_PIL.height/(tk_dims[1]*scale))
            pil_ratio = max(self.image_PIL.width/(pil_dims[0]*scale),
                            self.image_PIL.height/(pil_dims[1]*scale))
            # resize img logo for tk image (display) and PIL image (saving) using ratios
            # - tk image
            resize_img = self.image_PIL.copy()
            resized_tk = resize_img.resize((int(resize_img.width//tk_ratio),
                                            int(resize_img.height//tk_ratio)),
                                           Image.LANCZOS)
            self.image_logo_resized_tk = ImageTk.PhotoImage(resized_tk)  # the resized tk image
            # - PIL image
            resize_img = self.image_PIL.copy()
            self.image_logo_resized_PIL = resize_img.resize((int(resize_img.width//pil_ratio),
                                                             int(resize_img.height//pil_ratio)),
                                                            Image.LANCZOS)

    def add_img_logo(self):
        """
        gets option menu selections then creates PIL image and resizes.
        calls root function to pass image to canvas
        """
        ratio = int(self.size_var.get().split('%')[0])/100
        placement = self.orientation_var.get()
        self.resize_logo_image(ratio=ratio)  # creates PIL image and resizes
        # Adds to canvas frame and PIL display image
        self.parent.add_to_canvas(pil_logo=self.image_logo_resized_PIL,
                                  tk_logo=self.image_logo_resized_tk,
                                  placement=placement)
        # activate save button
        self.save_button.config(state=NORMAL)

