from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
import fonts
import save_pil
import re

NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')


class PNGLogoFrame(Frame):
    def __init__(self, root, tab):
        super().__init__(tab)
        self.parent = root

        self.png_folder = './png_folder'

        self.pack(fill='both', expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)


        self.pack_propagate(False)


        # variables for image_logo
        self.image_logo = None # name of the file
        self.image_PIL = None # the current logo image as PIL image
        self.image_logo_resized_tk = None # current logo image resized for tk
        self.image_logo_resized_PIL = None # current logo image resized for PIL



        # load png button
        self.load_png_file = Button(self, text="Add PNG file", fg='black', font=BOLD_FONT,
                                    command=self.upload_png_file
                                    )
        self.load_png_file.grid(row=0, column=0, padx=10, pady=10)


        # seperator
        self.seperator = ttk.Separator(self, orient="horizontal")
        self.seperator.grid(row=1, columnspan=3, sticky="ew", pady=10)

        # option menu for png files
        self.png_files = self.get_png_files()
        self.png_var = StringVar()
        self.png_var.set("Select PNG file")
        self.select_png_option = OptionMenu(self,
                                            self.png_var,
                                            self.png_files,
                                            command=self.activate_add_logo)
        self.select_png_option.grid(row=2, column=0, padx=10, pady=10)

        # placement option menu
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

        # logo SIZE
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



        # add logo label and button
        self.add_logo_button = Button(self,
                                      text="Add Logo",
                                      fg='black',
                                      bg='green',
                                      width=10,
                                      font=BOLD_FONT,
                                      state=DISABLED,
                                      command=self.add_img_logo)
        self.add_logo_button.grid(row=4, column=0, padx=10, pady=10)


        # save button to save image with logo
        self.save_button = Button(self, text="Save Image",
                                  fg='black',
                                  bg='blue',
                                  width=10,
                                  font=BOLD_FONT,
                                  state=DISABLED,
                                  command=self.parent.save_image
                                  )
        self.save_button.grid(row=4, column=2)


    def get_png_files(self):
        if len(self.parent.get_file_names(self.png_folder)) > 0:
            return self.parent.get_file_names(self.png_folder)
        else:
            return ["Add Image Logo Above"]
        # print("Files obtained")
        # return self.parent.get_file_names(self.png_folder)

    def upload_png_file(self):
        self.parent.browse_files(self.png_folder)

        self.update_png_option_menu()

    def update_png_option_menu(self):
        self.png_files = self.get_png_files()
        menu = self.select_png_option["menu"]
        menu.delete(0, "end")

        for file in self.png_files:
            menu.add_command(label=file, command=lambda value=file: (self.png_var.set(value), self.activate_add_logo(value)))


    def activate_add_logo(self, choice):
        if (re.sub(r"[()',]", "", self.png_var.get()) in self.png_files
                and self.size_var.get() in self.sizes
                and self.orientation_var.get() in self.orientations):
            self.add_logo_button.config(state=NORMAL)


    def create_image_logo_PIL(self):

        # get var for file options
        img_choice = self.png_var.get()
        self.image_logo = re.sub(r"[()',]", "", img_choice)
        print(self.image_logo)
        img_path = f"{self.png_folder}/{self.image_logo}"
        print(img_path)
        try:
            self.image_PIL = Image.open(img_path).convert("RGBA")
            print(True)
            return True
        except:
            return False

# this gets called  by the add logo button in this class
    def resize_logo_image(self, scale=0.2, ratio=1):

        scale = scale * ratio
        if self.create_image_logo_PIL(): # make sure image logo has been added

            # print(f"orig. img size = {self.image_PIL.width, self.image_PIL.height}")
            # if self.size_var.get().split('%')[0].isdigit():
            #     scale = int(self.size_var.get().split('%')[0])

            # 1. get TK and PIL dimensions from canvas
            tk_dims, pil_dims = self.parent.get_tk_pil_dimensions()

            # calc the ratio for scaling down the logo image
            tk_ratio = max(self.image_PIL.width/(tk_dims[0]*scale), self.image_PIL.height/(tk_dims[1]*scale))
            pil_ratio = max(self.image_PIL.width/(pil_dims[0]*scale), self.image_PIL.height/(pil_dims[1]*scale))

            # resize the image logo for both tk image and PIL image
            resize_img = self.image_PIL.copy()

            print(int(resize_img.width//tk_ratio))
            print(int(resize_img.height // tk_ratio))

            resized_tk = resize_img.resize(
                (int(resize_img.width//tk_ratio), int(resize_img.height//tk_ratio)), Image.LANCZOS)
            print(resized_tk.size)
            num_channels = 4  # RGBA
            image_memory = resized_tk.width * resized_tk.height * num_channels  # Approx memory in bytes
            print("Approximate memory usage for the image:", image_memory, "bytes")
            self.image_logo_resized_tk = ImageTk.PhotoImage(resized_tk)

            resize_img = self.image_PIL.copy()
            self.image_logo_resized_PIL = resize_img.resize(
                (int(resize_img.width//pil_ratio), int(resize_img.height//pil_ratio)), Image.LANCZOS)

            # print(f"PIL W: {self.image_logo_resized_PIL.width}, PIL H: {self.image_logo_resized_PIL.height}")
            # print(f"tk W: {self.image_logo_resized_tk.width}, tk H: {self.image_logo_resized_tk.height}")


    def add_img_logo(self):

        # scale = self.size_var.get()
        ratio = int(self.size_var.get().split('%')[0])/100
        placement = self.orientation_var.get()
        self.resize_logo_image(ratio=ratio)

        # need to do something about getting the size variable - and altering the scale of logo
        # and to pass it through to affect the placement on the image

        self.parent.add_to_canvas(pil_logo=self.image_logo_resized_PIL,
                                  tk_logo=self.image_logo_resized_tk,
                                  placement=placement,
                                  # scale=scale
                                  )
        self.save_button.config(state=NORMAL)

