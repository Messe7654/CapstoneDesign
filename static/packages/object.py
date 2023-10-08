# object.py
from enum import Enum
import cv2
import numpy
import urllib.request
import imutils

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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        self.pixel_data = img
        self.height = self.pixel_data.shape[0]
        self.width = self.pixel_data.shape[1]
        
    def __loadbyFilename(self, filename):
        """
        Loads an image from a file path
        Args:
            filename (string): Path of file to be loaded
        """
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED) # BGRA로 입력 받음
        self.pixel_data = img
        self.height = self.pixel_data.shape[0]
        self.width = self.pixel_data.shape[1]
    
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

    def resize(self, new_width, new_height):
        """
        Resize the object to the specified dimensions
        while maintaining or adjusting the aspect ratio.
        Args:
            new_width (_type_): 
                Width of object to be transformed.
            new_height (_type_):
                Height of object to be transformed.
        """
        self.width, self.height = new_width, new_height
        self.pixel_data = cv2.resize(self.pixel_data, dsize=(new_width, new_height))
    
    # TODO(Sanghun) : rotate가 2번 이상 들어올 경우 주변에 검은 공간이 늘어나는 점 수정
    # Method 1 : origin image에 대해서 계속 수정
    # Method 2 : rotate가 끝나고 alpha channel 0인 공간에 대해서 crop해주기
    def rotate(self, degree):
        """
        Rotate the object by the specified number of degrees.
        Args:
            degree (integer):
                the value to specify how to rotate the object
        """
        rotated = imutils.rotate_bound(self.pixel_data, degree)
        self.pixel_data = rotated
        self.height, self.width = self.pixel_data.shape[0], self.pixel_data.shape[1]
        
        
    def crop(self, x, y, width, height):
        """
        Crop the image into the specific area.
        Args:
            x (_type_): Horizontal starting point to cropped image
            y (_type_): Vertical starting point to cropped image
            width (_type_): A new width to crop
            height (_type_): A new height to crop
        """
        if (x + width <= self.width) and (y + height <= self.height):
            self.pixel_data = self.pixel_data[y : y + height, x : x + width]
        else:
            self.pixel_data = self.pixel_data[y : self.height, x : self.width]
        self.height, self.width = self.pixel_data.shape[0], self.pixel_data.shape[1]
        
    # def applyFilter(filter_type):
        
    # def getColor(x, y):
if __name__ == "__main__":
    test_obj = Object()
    test_obj.load("https://images.unsplash.com/photo-1561336313-0bd5e0b27ec8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80")
    test_obj.resize(test_obj.width // 3, test_obj.height // 3)
    
    test_obj.rotate(30)
    
    cv2.imshow("", test_obj.pixel_data)
    cv2.waitKey()
    
    