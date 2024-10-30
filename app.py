
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
import fonts
import save_pil
from canvas_frame import CanvasFrame
from logo_frame import LogoFrame
from png_logo_frame import PNGLogoFrame
import shutil

NORM_FONT = ('Arial', 12)
BOLD_FONT = ('Arial', 12, 'bold')


class App(Tk):
    def __init__(self):
        super().__init__()

        # Root set up -------------------------------
        self.title("Add logo to image app")
        self.minsize(width=1000, height=800)
        self.config(padx=10, pady=10)

        # Configure grid rows and columns to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # for deciding if to switch between frame1 and canvas frame
        self.current_img = None
        self.image_folder = "./image_folder"

        self.frame_dimensions = 800, 580


        # App Menu
        self.menu = Menu(self)  # creates Menu object - associated with application
        self.config(menu=self.menu)  # configures and displays the menu at top of the
        self.file_menu = Menu(self.menu)  # creates submenu, a menu object - associated
        self.menu.add_cascade(label="File", menu=self.file_menu)  # adds cascading menu
        self.file_menu.add_command(label="Add Image", command=lambda: self.browse_files(self.image_folder))  # adds a menu item to
        self.file_menu.add_separator()  # adds horizontal seperator between menu
        self.file_menu.add_command(label="Exit", command=self.quit)  # adds an exit



        # FRAMES -------------------------------------
        # Frame one - initial frame to load image
        self.frame1 = FrameOne(self, self.frame_dimensions)

        # Canvas Frame - to place image
        self.canvas = CanvasFrame(self)


        self.tab_control = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Text Logo")
        self.tab_control.add(self.tab2, text="PNG logo")
        self.tab_control.grid(row=2, column=0, columnspan=2)

        # logo functionality frame
        self.logo_frame = LogoFrame(self, self.tab1)
        self.png_logo_frame = PNGLogoFrame(self, self.tab2)
        # self.logo_frame = LogoFrame(self)


        style = ttk.Style()
        style.configure("TNotebook", tabposition='nw')


        self.top_frame = Frame(self, padx=20, pady=10)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.top_frame.pack_propagate(False)

        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)
        self.top_frame.grid_columnconfigure(3, weight=1)

        self.load_file_button = Button(self.top_frame, text="Load Images", fg="black",
                                       font=BOLD_FONT,
                                       command=lambda: self.browse_files(self.image_folder))
        self.load_file_button.grid(row=0, column=0)


        # Label to select file -----------------------
        self.select_file_label = Label(self.top_frame, text="Select File to Edit:", fg='black', font=NORM_FONT)
        self.select_file_label.grid(row=0, column=1, sticky='e')

        # Option menu to select file ------------------
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


    def show_help(self):
        messagebox.showinfo(title="Information",
                            message="1. Add Image Files to the image_folder, or press 'Load Images' button."
                                    "\n\n2. Select file and display with Load Selected File button"
                                    "\n\n3. Add Logo Text in entry box, then select all drop down options"
                                    " for Logo placement and style before adding logo and saving image.")


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
            #self.remove_widget_grid(self.logo_frame)
            # load frame 1
            self.add_widget_grid(widget=self.frame1)
            # self.load_image()
            #self.load_image()
            self.frame1.activate_button(choice)



    def get_file_names(self, folder):
        """
        could make this used for both image folder and png folder
        """
        files = []
        # get image files if directory exists
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                files.append(file)
        # create directory if does not exist
        else:
            os.mkdir(folder)
        return files



    def browse_files(self, folder):
        filename = filedialog.askopenfile(initialdir="./",
                                          title="Select a file")

        if folder == self.image_folder:
            supported_extensions =["JPEG", "JPG", "PNG", "GIF", "BMP", "TIFF", "ICO", "WEBP", "PPM", "PDF"]
            supported_extensions = [ext.lower() for ext in supported_extensions]
            if filename.name.split(".")[1].lower() in supported_extensions:
                source_path = filename.name
                destination = f"{self.image_folder}/{source_path.split('/')[-1]}"
                shutil.copy(source_path, destination)

            self.img_files = self.get_file_names(self.image_folder)
            self.update_file_option_menu()
        else:
            if filename.name.split(".")[1].lower() == 'png':
                source_path = filename.name
                destination = f"{folder}/{source_path.split('/')[-1]}"
                shutil.copy(source_path, destination)



    def update_file_option_menu(self):
        menu = self.file_option["menu"]
        menu.delete(0, "end")
        for file in self.img_files:
            menu.add_command(label=file, command=lambda value=file: (self.option_var.set(value), self.frame_to_load(value)))


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
    def __init__(self, parent, dimensions):
        super().__init__(parent)
        self.width = dimensions[0]
        self.height = dimensions[1]

        # link to the root
        self.parent = parent

        # configure Frame setup - - -- - - - - -
        self.config(width=self.width, height=self.height-50,
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
                                        command=self.parent.load_image,
                                        # command=self.parent.browse_files
                                        )

        self.load_image_button.place(relx=0.5, rely=0.5, anchor='center')


    def activate_button(self, choice):
        if choice in self.parent.img_files:
            self.load_image_button.config(state=NORMAL)



if __name__ == "__main__":

    app = App()
    app.mainloop()

