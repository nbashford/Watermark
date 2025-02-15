"""
Frame within Notebook tab
- - for adding text logos to display image
"""
from tkinter import *
from tkinter import ttk

NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')


class LogoFrame(Frame):
    def __init__(self, root, tab):
        super().__init__(tab)
        self.parent = root  # reference to root

        # **** set up Frame -------------------------
        self.pack(fill='both', expand=True)
        self.pack_propagate(False)
        # set up grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # holds value of current text logo
        self.logo = None

        # **** Widgets -------------------------------
        # text explaining the entry field
        self.logo_label = Label(self, text="Add logo text:",
                                fg='black', font=NORM_FONT)
        self.logo_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

        # entry field for adding logo
        self.logo_input = Entry(self, width=14, fg='black', bg="lightgrey")
        self.logo_input.grid(row=0, column=1, pady=10, padx=10, sticky='w')
        self.logo_input.bind("<Return>",  # allowing return key to activate entry
                             lambda event: self.update_logo_list())

        # button to add text from the entry field
        self.update_logo_button = Button(self, text="Add text", fg='black', width=10,
                                         command=self.update_logo_list,
                                         state=DISABLED)
        self.update_logo_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        # button activated when any key pressed in entry field
        self.logo_input.bind("<Key>", lambda e: self.update_logo_button.config(state=NORMAL))

        # seperator
        self.seperator = ttk.Separator(self, orient="horizontal", )
        self.seperator.grid(row=1, columnspan=5, sticky="ew", pady=10)

        # LOGO Selection option menu
        self.logos = []
        self.logo_var = StringVar(self)
        self.logo_var.set("Select Logo")
        self.logo_choice = OptionMenu(self,
                                      self.logo_var,
                                      value="Please add Logo above",
                                      *self.logos,
                                      command=self.activate_logo_button)
        self.logo_choice.grid(row=2, column=0, padx=10, pady=10)
        self.logo_choice.config(width=10)

        # logo PLACEMENT option menu
        self.orientations = ["Top left", "Top right", "Bottom right", "Bottom left"]
        self.orientation_var = StringVar(self)
        self.orientation_var.set("Logo Placement")
        self.logo_orientation = OptionMenu(self,
                                           self.orientation_var,
                                           *self.orientations,
                                           command=self.activate_logo_button)
        self.logo_orientation.grid(row=2, column=1, padx=10, pady=10)
        self.logo_orientation.config(width=10)

        # logo COLOUR option menu
        self.colors = ["blue", "grey", "red", "green", "yellow", "Orange"]
        self.color_var = StringVar(self)
        self.color_var.set("Select Colour")
        self.colour_choice = OptionMenu(self,
                                        self.color_var,
                                        *self.colors,
                                        command=self.activate_logo_button)
        self.colour_choice.grid(row=2, column=2, padx=10, pady=10)
        self.colour_choice.config(width=10)

        # logo FONT option menu
        self.fonts = ["Arial", "Courier", "Georgia", "Verdana", "Comic Sans MS", "Times New Roman"]
        self.font_var = StringVar(self)
        self.font_var.set("Select Font")
        self.font_choice = OptionMenu(self,
                                      self.font_var,
                                      *self.fonts,
                                      command=self.activate_logo_button)
        self.font_choice.grid(row=2, column=3, padx=10, pady=10)
        self.font_choice.config(width=10)

        # logo SIZE option menu
        self.sizes = ["10", "11", "12", "13", "14", "15", "16", "17", "18"]
        self.size_var = StringVar(self)
        self.size_var.set("Font size")
        self.size_choice = OptionMenu(self,
                                      self.size_var,
                                      *self.sizes,
                                      command=self.activate_logo_button)
        self.size_choice.grid(row=2, column=4, padx=10, pady=10)
        self.size_choice.config(width=10)

        # seperator
        self.second_seperator = ttk.Separator(self, orient="horizontal")
        self.second_seperator.grid(row=3, columnspan=5, sticky="ew", pady=10)

        # add logo label button
        self.add_logo_button = Button(self,
                                      text="Add Logo",
                                      fg='black', bg='green',
                                      width=10, font=BOLD_FONT,
                                      state=DISABLED,
                                      command=self.get_logo_details)
        self.add_logo_button.grid(row=4, column=0, padx=10, pady=10)

        # save button to save image with logo
        self.save_button = Button(self, text="Save Image",
                                  fg='black', bg='blue',
                                  width=10, font=BOLD_FONT,
                                  state=DISABLED,
                                  command=self.parent.save_image)
        self.save_button.grid(row=4, column=4)

    def update_logo_list(self):
        """
        updates the text logo option menu with the added text
        """
        logo_name = self.logo_input.get()
        if logo_name and logo_name not in self.logos:
            self.logos.append(logo_name)
            self.logo_var.set(logo_name)  # Set to the latest logo added
            self.logo_choice['menu'].delete(0, 'end')  # Clear current labels
            for logo in self.logos:  # update the option menu
                self.logo_choice['menu'].add_command(label=logo, command=lambda value=logo: self.logo_var.set(value))
            self.logo_input.delete("0", END)  # delete placeholder

    def activate_logo_button(self, choice):
        """
        checks all option menu choices are valid
        """
        if (self.logo_var.get() in self.logos
                and self.font_var.get() in self.fonts
                and self.orientation_var.get() in self.orientations
                and self.color_var.get() in self.colors
                and self.size_var.get() in self.sizes):
            # activate the add logo button
            self.add_logo_button.config(state=NORMAL, bg='green')

    def get_logo_details(self):
        """
        get all option menu selections,
        pass to root to pass to canvas to display text.
        Activates the save button
        """
        # get the text, font, position, colour, size
        position = self.orientation_var.get()
        colour = self.color_var.get()
        font = self.font_var.get()
        text = self.logo_var.get()
        size = int(self.size_var.get())
        # pass to root then canvas to add text logo
        self.parent.add_to_canvas(text=text, font=font, position=position, colour=colour, size=size)
        self.save_button.config(state=NORMAL)

