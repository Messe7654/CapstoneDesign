# object.py
from enum import Enum
import cv2
import numpy
import urllib.request
class Object:
    """
    The class that manages the image
    
    Attributes:
        width (integer)
            An attribute to store the width of the object in pixels.
        height (integer)
            An attribute to store the height of the object in pixels.
        metadata (dictionary)
            A dictionary or object to store additional information
            about the object, such as author, creation date, and object description.
        pixel_data (cv2)
            A data structure (e.g., a 2D array or a buffer)
            to store pixel information for the object.
    """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.metadata = dict()
        self.pixel_data = None
    
    def __isURL(self, filename):
        """
        check that filename start with a protocol identifier
        Args:
            filename (string): Path to check

        Returns:
            boolean: True for URL, False for local file
        """
        url_protocols = ["http://", "https://", "ftp://", "file://"]
        for protocol in url_protocols:
            if filename.startswith(protocol):
                return True
        return False
        
    def __loadbyURL(self, url):
        """
        Loads an image from a Internet URL
        Args:
            url (string): URL of file to be loaded
        """
        req = urllib.request.urlopen(url)
        arr = numpy.asarray(bytearray(req.read()), dtype=numpy.uint8)
        img = cv2.imdecode(arr, -1)
        self.pixel_data = img
        self.width = self.pixel_data.shape[0]
        self.height = self.pixel_data.shape[1]
        
    def __loadbyFilename(self, filename):
        """
        Loads an image from a file path
        Args:
            filename (string): Path of file to be loaded
        """
        img = cv2.imread(filename)
        self.pixel_data = img
        self.width = self.pixel_data.shape[0]
        self.height = self.pixel_data.shape[1]
    
    def load(self, filename):
        """
        Loads an image form a path / URL
        Args:
            filename (string):
                Name of file to be loaded.
        """
        if self.__isURL(filename) == True:
            self.__loadbyURL(filename)
        else:
            self.__loadbyFilename(filename)        

    # def resize(self, new_width, new_height):
    #     """
    #     Resize the object to the specified dimensions
    #     while maintaining or adjusting the aspect ratio.
    #     Args:
    #         new_width (_type_): 
    #             Width of object to be transformed.
    #         new_height (_type_):
    #             Height of object to be transformed.
    #     """
        
    # def rotate(self, degree):
        
    # def crop(self, x, y, width, height):
        
    # def applyFilter(filter_type):
        
    # def getColor(x, y):
if __name__ == "__main__":
    test_obj = Object()
    test_obj.load("https://mimgnews.pstatic.net/image/144/2023/09/28/0000915729_001_20230928132501311.jpg?type=w540")
    
    