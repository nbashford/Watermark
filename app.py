"""
Main Tkinter application class
- organises all frames
- allows files to be uploaded
- provides communication between frames
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
from PIL import Image
import save_pil
from canvas_frame import CanvasFrame
from logo_frame import LogoFrame
from png_logo_frame import ImgLogoFrame
import shutil

# tkinter font constants
NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')


class App(Tk):
    def __init__(self):
        super().__init__()

        # **** Root set up *************************
        self.title("Add logo to image app")
        self.minsize(width=1000, height=800)
        self.config(padx=10, pady=10)

        # Configure grid rows and columns to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # attributes: current image, name of image folder and frame dimensions
        self.current_img = None
        self.image_folder = "./image_folder"
        self.frame_dimensions = 800, 580

        # **** WIDGETS *********************************************

        # ----- App Menu
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        # add image
        self.file_menu.add_command(label="Add Image",
                                   command=lambda: self.browse_files(self.image_folder))
        self.file_menu.add_separator()
        # exit application
        self.file_menu.add_command(label="Exit", command=self.quit)  # adds an exit

        # ------- FRAMES ---------------

        # 1. TOP FRAME - add files, select file, help button
        self.top_frame = Frame(self, padx=20, pady=10)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.top_frame.pack_propagate(False)
        # Configure grid for top frame
        for i in range(4):
            self.top_frame.grid_columnconfigure(i, weight=1)

        # Load file button
        self.load_file_button = Button(self.top_frame, text="Load Images", fg="black",
                                       font=BOLD_FONT,
                                       command=lambda: self.browse_files(self.image_folder))
        self.load_file_button.grid(row=0, column=0)

        # Select file label
        self.select_file_label = Label(self.top_frame, text="Select File to Edit:", fg='black', font=NORM_FONT)
        self.select_file_label.grid(row=0, column=1, sticky='e')

        # select file Option menu
        self.img_files = self.get_file_names(self.image_folder)
        self.option_var = StringVar(self)
        self.option_var.set("None Selected")
        self.file_option = OptionMenu(self.top_frame,
                                      self.option_var,
                                      value="None Selected",
                                      command=self.frame_to_load
                                      )
        self.file_option.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        if len(self.img_files) > 0:
            self.update_file_option_menu()

        # Help Button
        self.help_button = Button(self.top_frame, text="Help", fg='black', font=NORM_FONT,
                                  command=self.show_help)
        self.help_button.grid(row=0, column=3)

        # 2. BLANK FRAME - indicating user needs to load img
        self.blank_frame = Frame(self, width=self.frame_dimensions[0],
                                 height=self.frame_dimensions[1]-50,
                                 bg='lightgrey')
        self.blank_frame.grid(row=1, column=0, columnspan=2)
        self.blank_frame.pack_propagate(False)

        # Button to display image
        self.load_image_button = Button(self.blank_frame,
                                        text="Load selected file",
                                        fg="black",
                                        state=DISABLED,
                                        font=BOLD_FONT,
                                        command=self.load_image)
        self.load_image_button.place(relx=0.5, rely=0.5, anchor='center')

        # 3. Canvas Frame - to display loaded image
        self.canvas = CanvasFrame(self)

        # 4. TAB ADD LOGO FRAME - can add text or img logo to main image
        style = ttk.Style()
        style.configure("TNotebook", tabposition='nw')
        self.tab_control = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Text Logo")
        self.tab_control.add(self.tab2, text="PNG logo")
        self.tab_control.grid(row=2, column=0, columnspan=2)
        # Frame containing Text Logo functionality
        self.logo_frame = LogoFrame(self, self.tab1)
        # Frame containing Image Logo functionality
        self.png_logo_frame = ImgLogoFrame(self, self.tab2)

    def show_help(self, **kwargs):
        if kwargs:
            messagebox.showinfo(title=f"{kwargs.get('title')}",
                                message=f"{kwargs.get('message')}")
        else:
            messagebox.showinfo(title="Information",
                                message="1. Add Image Files to the image_folder, "
                                        "or press 'Load Images' button."
                                        "\n\n2. Select file and display with Load "
                                        "Selected File button"
                                        "\n\n3. Add Logo Text in entry box, "
                                        "then select all drop down options"
                                        " for Logo placement and style before "
                                        "adding logo and saving image.")

    def frame_to_load(self, choice):
        """
        changes whether 'Blank Frame' is displayed or 'Canvas Frame' is displayed.
        """
        # if initial image selected - activate load button
        if not self.current_img:
            self.activate_button(choice)
            return
        # if selected different image - remove canvas and load frame 1
        file_name = self.get_selected_file()
        if file_name != self.current_img:
            self.remove_widget_grid(self.canvas)  # remove canvas frame
            self.add_widget_grid(widget=self.blank_frame)  # load frame 1
            self.activate_button(choice)  # can now load the new image


    def update_file_option_menu(self):
        """
        updates the select file option menu
        """
        menu = self.file_option["menu"]
        menu.delete(0, "end")
        for file in self.img_files:
            menu.add_command(label=file,
                             command=lambda value=file: (self.option_var.set(value),
                                                         self.frame_to_load(value)))

    def remove_widget_grid(self, widget):
        """
        passed widget is removed from grid
        """
        widget.grid_remove()

    def add_widget_grid(self, widget, row=1, column=0, columnspan=2):
        """
        passed widget is added to grid
        """
        widget.grid(row=row, column=column, columnspan=columnspan)

    def get_selected_file(self):
        """
        :return: file selected in option menu
        """
        file_name = self.option_var.get()
        return file_name

    def activate_button(self, choice):
        """
        if select file option is in the image folder - enable load img button
        """
        if choice in self.img_files:
            self.load_image_button.config(state=NORMAL)

    def load_image(self):
        """
        Removes blank placeholder frame from view and adds the canvas frame.
        selected image is opened using PIL, and rotated if portrait.
        Image and orientation passed to Canvas frame class to display img.
        """
        file_name = self.get_selected_file()  # get file name
        self.current_img = file_name  # set as pointer to current img name
        self.remove_widget_grid(self.blank_frame)  # remove blank frame
        self.add_widget_grid(self.canvas)  # place canvas frame on root
        image_path = "./image_folder/" + file_name
        pil_image = Image.open(image_path)  # load image

        portrait = False
        # rotate image based on exif orientation data
        try:
            exif = pil_image.getexif()
            orientation = 274  # EXIF tag for orientation
            if exif and orientation in exif:
                exif_orientation = exif[orientation]
                if exif_orientation == 3:
                    pil_image = pil_image.rotate(180, expand=True)
                    portrait=True
                elif exif_orientation == 6:
                    pil_image = pil_image.rotate(270, expand=True)
                    portrait=True
                elif exif_orientation == 8:
                    pil_image = pil_image.rotate(90, expand=True)
                    portrait=True
        except (AttributeError, KeyError, IndexError):
            pass

        # display on canvas frame
        self.canvas.add_image(pil_image=pil_image, portrait=portrait)

    def add_to_canvas(self, **kwargs):
        """
        helper to pass data from either LogoFrame ImgLogoFrame class to Canvas frame
        """
        self.canvas.add_logo(**kwargs)

    def get_tk_pil_dimensions(self):
        """
        gets the current img dimensions displayed in canvas
        """
        return self.canvas.get_img_dimensions()

    def save_image(self, overwrite=False):
        """
        retrieves and passes the PIL image from canvas with file name
        to save_pil class to save.
        If file previously saved - option to override is displayed
        """
        pil_image = self.canvas.get_PIL_image()  # get PIL image - Canvas
        save = save_pil.SaveImage(self.get_selected_file(), pil_image)
        # save file - True if file not previously saved
        saved = save.save_image(overwrite)
        if not saved:
            overwrite = messagebox.askyesno(
                title="File already exists",
                message="The file is already saved. "
                        "Do you want to overwrite the file?")
            if overwrite:
                # call function again but with overwrite command
                self.save_image(overwrite=overwrite)

    def get_file_names(self, folder):
        """
        returns files from passed folder, creates if no such folder.
        """
        files = []
        if os.path.isdir(folder):  # if folder exist
            for file in os.listdir(folder):
                files.append(file)
        else:
            os.mkdir(folder)  # creates folder if none
        return files

    def browse_files(self, folder):
        """
        Opens OS select file.
        checks if selected file is an image file.
        Adds file to either 'image_folder' if called from 'Top frame'
        or to 'img_logo_folder' if called from ImgLogoFrame
        """
        supported_extensions = ["JPEG", "JPG", "PNG", "GIF", "BMP", "TIFF", "ICO", "WEBP", "PPM", "PDF"]
        filename = filedialog.askopenfile(initialdir="./",
                                          title="Select a file")
        if filename:
            # if correct file type
            if filename.name.split(".")[1].upper() in supported_extensions:
                source_path = filename.name
                destination = f"{folder}/{source_path.split('/')[-1]}"
                shutil.copy(source_path, destination)
                if folder == self.image_folder:  # main upload image folder
                    self.img_files = self.get_file_names(self.image_folder)
                    self.update_file_option_menu()
            else:
                messagebox.showinfo(title="Unsupported file type",
                                    message="Please upload an image file")


if __name__ == "__main__":

    app = App()
    app.mainloop()

