"""
save class
- creates a folder to store saved images if none, and saves PIL image with added logo
"""
import os


class SaveImage:

    def __init__(self, file_name, image, directory='./edited_images', extension=".jpg"):
        self.file_name = file_name  # file name
        self.image = image  # image from tkinter app
        self.format = extension  # file extension
        self.edited_image_folder = self.get_edited_folder(directory)  # folder to place file

    def get_edited_folder(self, directory):
        """
        creates saved image folder if none
        """
        if not os.path.isdir(directory):
            os.mkdir(directory)
        return directory

    def save_image(self, overwrite=False):
        """
        saves image to the saved image folder if not previously saved.
        if passed override True, then saves over current file
        """
        if not overwrite:
            if f"{self.file_name}_logo{self.format}" not in os.listdir(self.edited_image_folder):
                self.image.save(f"{self.edited_image_folder}/{self.file_name}_logo{self.format}")
                return True
            else:
                return False
        self.image.save(f"{self.edited_image_folder}/{self.file_name}_logo{self.format}")
        return True

