"""
TODO 1: add mechanism to add img files to application
TODO 2: add way to add logo to image and change the orientation placement

self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
                        text="Click the bubbles that are multiples of two.")
 - therefore -
 def add_logo(text, font, position, colour):
- where to place - within Canvas frame

- called by root
self.canvas.add_logo()

- called by `logo frame
self.parent.add_to_canvas(text, font, position, colour)
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
import fonts
import save_pil

NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')


class App(Tk):
    def __init__(self):
        super().__init__()
        # Root set up -------------------------------
        self.title("Add logo to image app")
        self.minsize(width=1000, height=800)
        self.config(padx=5, pady=5)

        # Configure grid rows and columns to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.current_img = None


        # FRAMES -------------------------------------
        # Frame one - initial frame to load image
        self.frame1 = FrameOne(self)

        # Canvas Frame - to place image
        self.canvas = CanvasFrame(self)

        # logo functionality frame
        self.logo_frame = LogoFrame(self)


        # Label to select file -----------------------
        self.label = Label(self, text="Select file to load: ",
                           fg="black", font=NORM_FONT)
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="e")  # still to add

        # Option menu to select file ------------------
        self.img_files = self.get_file_names()
        self.option_var = StringVar(self)
        self.option_var.set("None Selected")
        self.file_option = OptionMenu(self,
                                      self.option_var,
                                      #self.img_files[0],
                                      *self.img_files,
                                      command=self.frame_to_load
                                      )
        self.file_option.grid(row=0, column=1, padx=5, pady=5, sticky="w")




    def frame_to_load(self, choice):
        # if first image selected - activate load button
        if not self.current_img:
            self.frame1.activate_button(choice)
            return
        # if image already loaded but select different image
        # - load frame 1 and activate button
        file_name = self.get_selected_file()
        if file_name != self.current_img:
            # remove canvas frame and logo frame
            self.remove_widget_grid(self.canvas)
            self.remove_widget_grid(self.logo_frame)
            # load frame 1
            self.add_widget_grid(widget=self.frame1)
            # self.load_image()
            #self.load_image()
            self.frame1.activate_button(choice)




    def get_file_names(self, folder_path="./image_folder"):
        files = []
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                files.append(file)

        return files

    def remove_widget_grid(self, widget):
        widget.grid_remove()

    def add_widget_grid(self, widget, row=1, column=0, columnspan=2):
        widget.grid(row=row, column=column, columnspan=columnspan)


    def add_logo_frame(self, widget):
        widget.grid(row=2, column=0, columnspan=2#, sticky='n'
                    )

    def get_selected_file(self):
        # could add some more checks to selecting the file
        file_name = self.option_var.get()
        return file_name

    def load_image(self):
        """
        1. get file name
        2. unpack the Frame_await_image
        3. pack the canva frame
        4. add the image to the canva frame
        my_image = PhotoImage(file='tomato.png')
        canvas_image = canvas.create_image(250, 250, image=my_image).
        5. configure to full size
        """
        # 1. get file name
        file_name = self.get_selected_file()
        self.current_img = file_name
        # 2. unpack the Frame_await_image
        self.remove_widget_grid(self.frame1)
        # 3. pack the canvas frame
        self.add_widget_grid(self.canvas)
        # 4. add the image to the canva frame
        image_path = "./image_folder/" + file_name
        pil_image = Image.open(image_path)

        self.canvas.add_image(pil_image=pil_image)

        self.add_logo_frame(self.logo_frame)
        #self.add_logo_button.config(state=NORMAL)

    def add_to_canvas(self, text, font, position, colour, size):
        self.canvas.add_logo(text, font, position, colour, size)

    def save_image(self, overwrite=False):
        pil_image = self.canvas.get_PIL_image()
        file_name = self.get_selected_file()
        save = save_pil.SaveImage(file_name, pil_image)
        saved = save.save_image(overwrite)
        if not saved:
            overwrite = messagebox.askyesno(title="File already exists",
                                message="The file is already saved. Do you want to overwrite the file?")
            if overwrite:
                self.save_image(overwrite=overwrite)





class FrameOne(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # link to the root
        self.parent = parent

        # configure Frame setup - - -- - - - - -
        self.config(width=650, height=400,
                    #padx=50, pady=50,
                    bg='lightgrey')
        self.grid(row=1, column=0, columnspan=2,
                  #padx=50, pady=20
                  )

        # Prevent the frame from shrinking to fit its contents
        self.pack_propagate(False)

        # load image button in the frame
        self.load_image_button = Button(self,
                                        text="Load selected file",
                                        fg="black",
                                        # bg='lightgrey',
                                        # highlightthickness=1,
                                        # activebackground='blue',
                                        state=DISABLED,
                                        font=BOLD_FONT,
                                        command=self.parent.load_image)

        self.load_image_button.pack(pady=100)


    def activate_button(self, choice):
        if choice in self.parent.img_files:
            self.load_image_button.config(state=NORMAL)



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


class LogoFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        #self.config(padx=20)
        self.pack_propagate(False)

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

        self.logo = None

        # First row - Add logos or select existing logo,
        # - change font and colour
        self.logo_label = Label(self, text="Add an image logo:", fg='black',
                                font=NORM_FONT)
        self.logo_label.grid(row=0, column=0, pady=10, padx=10)

        self.logo_input = Entry(self, width=14, fg='black', bg="lightgrey")
        self.logo_input.grid(row=0, column=1, pady=10, padx=10, sticky='w')
        self.logo_input.bind("<Return>", lambda event: self.update_logo_list())


        self.update_logo_button = Button(self, text="Add logo", fg='black', state=DISABLED,
                                         command=self.update_logo_list)
        self.update_logo_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.logo_input.bind("<Key>", lambda e: self.update_logo_button.config(state=NORMAL))


        # second row ----------------------------
        self.seperator = ttk.Separator(self, orient="horizontal")
        self.seperator.grid(row=1, columnspan=5, sticky="ew", pady=10)




        # third row --------------------

        # LOGO Selection
        self.logos = []
        self.logo_var = StringVar(self)
        self.logo_var.set("Select Logo")
        self.logo_choice = OptionMenu(self,
                                        self.logo_var,
                                        value="Please add Logo above",
                                        *self.logos,
                                        command=self.activate_logo_button
                                      )
        self.logo_choice.grid(row=2, column=0, padx=10, pady=10)
        self.logo_choice.config(width=10)


        # logo PLACEMENT
        self.orientations = ["Top left", "Top right", "Bottom right", "Bottom left"]
        self.orientation_var = StringVar(self)
        self.orientation_var.set("Logo Placement")
        self.logo_orientation = OptionMenu(self,
                                           self.orientation_var,
                                           *self.orientations,
                                           command=self.activate_logo_button
                                           )
        self.logo_orientation.grid(row=2, column=1, padx=10, pady=10)
        self.logo_orientation.config(width=10)


        # logo COLOUR
        self.colors = ["blue", "grey", "red", "green", "yellow", "Orange"]
        self.color_var = StringVar(self)
        self.color_var.set("Select Colour")
        self.colour_choice = OptionMenu(self,
                                        self.color_var,
                                        *self.colors,
                                        command=self.activate_logo_button
                                        )
        self.colour_choice.grid(row=2, column=2, padx=10, pady=10)
        self.colour_choice.config(width=10)


        # logo FONT
        self.fonts = ["Arial", "Courier", "Georgia", "Verdana", "Comic Sans MS", "Times New Roman"]
        self.font_var = StringVar(self)
        self.font_var.set("Select Font")
        self.font_choice = OptionMenu(self,
                                        self.font_var,
                                        *self.fonts,
                                        command=self.activate_logo_button
                                      )
        self.font_choice.grid(row=2, column=3, padx=10, pady=10)
        self.font_choice.config(width=10)


        # logo SIZE
        self.sizes = ["10", "11", "12", "13", "14", "15", "16", "17", "18"]
        self.size_var = StringVar(self)
        self.size_var.set("Select Font")
        self.size_choice = OptionMenu(self,
                                        self.size_var,

                                        *self.sizes,
                                        command=self.activate_logo_button
                                      )
        self.size_choice.grid(row=2, column=4, padx=10, pady=10)
        self.size_choice.config(width=10)


        # fourth row --------------------------

        self.second_seperator = ttk.Separator(self, orient="horizontal")
        self.second_seperator.grid(row=3, columnspan=5, sticky="ew", pady=10)


        # Fifth row ---------------------------

        # add logo label and button
        self.add_logo_button = Button(self,
                                      text="Add Logo",
                                      fg='black',
                                      bg='green',
                                      # highlightbackground='green',
                                      font=BOLD_FONT,
                                      state=DISABLED,
                                      command=self.get_logo_details)
        self.add_logo_button.grid(row=4, column=0, padx=10, pady=10)


        # save button to save image with logo
        self.save_button = Button(self, text="Save Logo Image",
                                  fg='black',
                                  bg='blue',
                                  font=BOLD_FONT,
                                  state=DISABLED,
                                  command=self.parent.save_image
                                  )
        self.save_button.grid(row=4, column=4)


    def update_logo_list(self):
        logo_name = self.logo_input.get()
        if logo_name and logo_name not in self.logos:
            self.logos.append(logo_name)
            # Update OptionMenu
            self.logo_var.set(logo_name)  # Set to the latest logo added (optional)
            # Clear and recreate the options in the OptionMenu
            self.logo_choice['menu'].delete(0, 'end')  # Clear current options
            for logo in self.logos:
                self.logo_choice['menu'].add_command(label=logo, command=lambda value=logo: self.logo_var.set(value))
            self.logo_input.delete("0", END)

    def activate_logo_button(self, choice):
        if (self.logo_var.get() in self.logos
                and self.font_var.get() in self.fonts
                and self.orientation_var.get() in self.orientations
                and self.color_var.get() in self.colors
                and self.size_var.get() in self.sizes):

            self.add_logo_button.config(state=NORMAL, bg='green')


    def get_logo_details(self):
        # get the text, font, position, colour, size
        position = self.orientation_var.get()
        colour = self.color_var.get()
        font = self.font_var.get()
        text = self.logo_var.get()
        size = int(self.size_var.get())
        self.parent.add_to_canvas(text, font, position, colour, size)
        self.save_button.config(state=NORMAL)



if __name__ == "__main__":

    app = App()
    app.mainloop()


"""
HOW WILL I SAVE THE LOGO

- need to get the current image after adding the logo 

- need to also add the text to the (hidden) PIL image 
- do this when adding the text to the tkinter image 

- requires the .ttf fonts from MacOS 

Common fonts
/System/Library/Fonts
Supplemental font package: 
/System/Library/Fonts/Supplemental

"""

    # def load_image(self):
    #     """
    #     1. get file name
    #     2. unpack the Frame_await_image
    #     3. pack the canva frame
    #     4. add the image to the canva frame
    #     my_image = PhotoImage(file='tomato.png')
    #     canvas_image = canvas.create_image(250, 250, image=my_image).
    #     5. configure to full size
    #     """
    #     # 1. get file name
    #     file_name = self.get_selected_file()
    #     # 2. unpack the Frame_await_image
    #     self.remove_widget_grid(self.frame1)
    #     # 3. pack the canvas frame
    #     self.add_widget_grid(self.canvas)
    #     # 4. add the image to the canva frame
    #     image_path = "./image_folder/" + file_name
    #     pil_image = Image.open(image_path)
    #
    #     # Define maximum canvas size
    #     max_width, max_height = 500, 400
    #
    #     # Calculate aspect ratio and get new height and width for the image
    #     aspect_ratio = min(max_width / pil_image.width, max_height / pil_image.height)
    #     new_width = int(pil_image.width * aspect_ratio)
    #     new_height = int(pil_image.height * aspect_ratio)
    #     # Resize image
    #     resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
    #     tk_image = ImageTk.PhotoImage(resized_image)
    #
    #     # Display the image on the canvas
    #     self.canvas.create_image(max_width // 2, max_height // 2, image=tk_image)
    #
    #     # Keep a reference to avoid garbage collection
    #     self.canvas.image = tk_image
    #
    #     # Adjust canvas size to match max dimensions
    #     self.canvas.config(width=max_width, height=max_height)
    #
    #     # tk_image = ImageTk.PhotoImage(pil_image)
    #     # canvas_image = self.canvas.create_image(10, 10, image=tk_image)
    #     # self.canvas.image = tk_image
    #     # self.canvas.config(width=pil_image.width, height=pil_image.height)
    #
    #     # # # # - *******************