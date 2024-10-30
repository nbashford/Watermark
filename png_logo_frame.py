from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
import fonts
import save_pil

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
                                            "Select PNG file")
        self.select_png_option.grid(row=2, column=0, padx=10, pady=10)

        # placement option menu
        self.orientations = ["Top left", "Top right", "Bottom right", "Bottom left"]
        self.orientation_var = StringVar(self)
        self.orientation_var.set("Logo Placement")
        self.logo_orientation = OptionMenu(self,
                                           self.orientation_var,
                                           *self.orientations,
                                           #command=self.activate_logo_button
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
                                        #command=self.activate_logo_button
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
                                      state=DISABLED
                                      #command=self.get_logo_details
                                      )
        self.add_logo_button.grid(row=4, column=0, padx=10, pady=10)


        # save button to save image with logo
        self.save_button = Button(self, text="Save Image",
                                  fg='black',
                                  bg='blue',
                                  width=10,
                                  font=BOLD_FONT,
                                  state=DISABLED
                                  #command=self.parent.save_image
                                  )
        self.save_button.grid(row=4, column=2)


    def get_png_files(self):
        return self.parent.get_file_names(self.png_folder)

    def upload_png_file(self):
        self.parent.browse_files(self.png_folder)

        self.png_files = self.get_png_files()
        self.update_png_option_menu()

    def update_png_option_menu(self):
        menu = self.select_png_option["menu"]
        menu.delete(0, "end")

        for file in self.png_files:
            menu.add_command(label=file, command=lambda value=file: (self.png_var.set(value), self.png_option_do_something(file)))


    def png_option_do_something(self, file):
        print(file )