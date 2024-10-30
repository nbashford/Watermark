import os


class SaveImage:

    def __init__(self, file_name, image, directory='./edited_images', extenstion=".jpg"):
        self.file_name = file_name  # file name
        self.image = image  # image from tkinter app
        self.format = extenstion
        self.edited_image_folder = self.get_edited_folder(directory)  # folder to place file

        # if self.file_not_present(self.file_name):
        #     self.save_image()
        #
    def get_edited_folder(self, directory):
        if os.path.isdir(directory):
            return directory
        else:
            os.mkdir(directory)
            return directory

    def save_image(self, overwrite=False):

        if not overwrite:
            if f"{self.file_name}_logo{self.format}" not in os.listdir(self.edited_image_folder):
                self.image.save(f"{self.edited_image_folder}/{self.file_name}_logo{self.format}")
                return True
            else:
                return False
        else:
            self.image.save(f"{self.edited_image_folder}/{self.file_name}_logo{self.format}")
            return True



