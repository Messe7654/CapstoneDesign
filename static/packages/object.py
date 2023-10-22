from collections import deque
from enum import Enum
import cv2
import numpy
import urllib.request
import imutils
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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
        self.offset = [0, 0] # [x, y] offsets
    
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
        
        # action
          

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

        # action
        
    def rotate(self, degree):
        """
        Rotate the object by the specified number of degrees.
        Args:
            degree (integer):
                the value to specify how to rotate the object
        """
        rotated = imutils.rotate_bound(self.pixel_data, degree)
        
        # crop the empty space
        alpha = rotated[:, :, 3]
        _, threshold = cv2.threshold(alpha, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        x, y, width, height = cv2.boundingRect(contours[0])
        
        self.pixel_data = rotated[y : y + height, x : x + width]
        self.height, self.width = self.pixel_data.shape[0], self.pixel_data.shape[1]
        
        # action
        
        
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
        
        # action
        
    def move(self, x_diff, y_diff):
        self.offset[0] = self.offset[0] + x_diff
        self.offset[1] = self.offset[1] + y_diff
        
        # action
        
    # def applyFilter(filter_type):
        
    # def getColor(x, y):
    

class Layer:
    layers = list()
    
    BLEND_MODE_NORMAL = 0
    BLEND_MODE_MULTIPLY = 1
    BLEND_MODE_OVERLAY = 2
    
    FLIP_VERTICAL = 1
    FLIP_HORIZONTAL = 2
    
    selected = None
    
    __DEFAULT_WIDTH = 1280
    __DEFAULT_HEIGHT = 1080
    
    board = None
    
    def __init__(self):
        self.name = ""
        self.visible = True
        self.opacity = 1
        self.blending_mode = Layer.BLEND_MODE_NORMAL
        self.position = 0
        self.width = Layer.__DEFAULT_WIDTH
        self.height = Layer.__DEFAULT_HEIGHT
        self.mask = None
        self.lock = False
        self.link_to = None
        
        pixel_data = numpy.zeros((self.__DEFAULT_HEIGHT, self.__DEFAULT_WIDTH, 4), dtype=numpy.uint8)
        
        self.contents = {"pixel_data" : pixel_data, "texts" : list()}
        self.object_list = list()
        
    def select(self):
        Layer.selected = self
        # action
        
    def SetDefaultWidth(self, new_width):
        Layer.__DEFAULT_WIDTH = new_width
        # action
        
    def SetDefaultHeight(self, new_height):
        Layer.__DEFAULT_HEIGHT = new_height
        # action
        
    def SetBlendingMode(self, new_blending_mode):
        self.blending_mode = new_blending_mode
        # action
        
    def ToggleVisibility(self):
        self.visible = not self.visible
        # action
        
    def Lock(self):
        self.lock = True
        # action
        
    def Unlock(self):
        self.lock = False
        # action
        
    def LinkTo(self, layer):
        self.link_to = layer
        # action
        
    def UnlinkTo(self):
        self.link_to = None
        # action
        
    def AdjustOpacity(self, new_opacity):
        self.opacity = new_opacity
        
    def ApplyMask(self, masking_layer):
        self.mask = masking_layer
        
    def Flip(self, mode):
        flip_code = 0
        if mode == 1:
            flip_code = 1
        elif mode == 2:
            flip_code = 0
        else:
            flip_code = -1
        self.contents["pixel_data"] = cv2.flip(self.contents["pixel_data"], flip_code)
    
        # action
        
    def AdjustPosition(self, adjust):
        now_idx = Layer.layers.index(self)
        Layer.layers.pop(now_idx)
        length = len(Layer.layers)
        next_idx = now_idx + adjust
        if next_idx < 0:
            next_idx = 0
        elif next_idx > length:
            next_idx = length
        Layer.layers.insert(next_idx, self)
        
        # action
        
    def RunObjects(self):
        for obj in self.object_list:
            x, y = obj.offset
            width, height = obj.width, obj.height
            alpha_channel = obj.pixel_data[:,:,3]
            self.contents["pixel_data"][y : y + height, x : x + width][alpha_channel > 0] = obj.pixel_data[:,:][alpha_channel > 0]
        
    def draw(self):
        Layer.board = numpy.zeros((Layer.__DEFAULT_HEIGHT, Layer.__DEFAULT_WIDTH, 4), dtype=numpy.uint8)
        for layer in Layer.layers:
            layer.RunObjects()
            if layer.contents["pixel_data"] is None:
                continue
            alpha_channel = layer.contents["pixel_data"][:,:,3]
            Layer.board[alpha_channel > 0] = cv2.addWeighted(layer.contents["pixel_data"][alpha_channel > 0], layer.opacity, 
                                                             Layer.board[alpha_channel > 0], 1 - layer.opacity, 0)
            
        
    def getColor(self, x, y):
        return self.contents["pixel_data"][y][x]
    
    def merge(self, layer):
        for obj in self.object_list:
            layer.object_list.append(obj)
        
class creater:
    __instance = None
    
    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance
    
    def create_layer(self) -> Layer:
        new_layer = Layer()
        Layer.layers.append(new_layer)
        return new_layer
    
    def create_object(self, src="") -> Object:
        new_object = Object()
        if src != "":
            new_object.load(src)
        Layer.selected.object_list.append(new_object)
        return new_object      
    
    def create_text(self, string, position=(0, 0), color=(255, 255, 255), scale=1, thick=1) -> Object:
        size, base = cv2.getTextSize(string, cv2.FONT_HERSHEY_SIMPLEX, scale, thick)
        new_object = Object()
        new_object.offset = position
        new_object.width, new_object.height = size
        new_object.pixel_data = numpy.zeros((new_object.height, new_object.width, 4), dtype=numpy.uint8)
        cv2.putText(new_object.pixel_data, string, (0, 2 * base)
                    , cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), thick)
        blue_channel = new_object.pixel_data[:,:,0]
        new_object.pixel_data[:,:,3][blue_channel > 0] = 255
        new_object.pixel_data[:,:,:-1][blue_channel > 0] = color
        
        Layer.selected.object_list.append(new_object)
        return new_object
    
if __name__ == "__main__":
    mycreat = creater()
    
    layer1 = mycreat.create_layer()
    layer2 = mycreat.create_layer()
    
    layer1.select()
    mycreat.create_object("https://image.jtbcplus.kr/data/contents/jam_photo/202307/20/ce688e7c-1505-4e23-b41e-c117b1016191.jpg")
    layer2.select()
    mycreat.create_object("https://i.ytimg.com/vi/d7sq--R2hMM/maxresdefault.jpg")
    
    layer1.draw()
    
    cv2.imshow("", Layer.board)
    cv2.waitKey()
    
    layer2.select()
    mycreat.create_text("Hello, world!", (500, 20), (0, 0, 0), scale=3, thick=6)
    layer1.draw()
    cv2.imshow("", Layer.board)
    cv2.waitKey()