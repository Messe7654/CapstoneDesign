import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import mymodule as mip

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        self.layer_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Layer", menu=self.layer_menu)
        self.layer_menu.add_command(label="New Layer", command=self.add_layer)
        self.layer_menu.add_command(label="Bring to Front", command=self.bring_to_front)
        self.layer_menu.add_command(label="Send to Back", command=self.send_to_back)
        self.layer_menu.add_separator()
        self.layer_menu.add_command(label="Set Transparency", command=self.set_transparency)

        default_layer = mip.layer.Layer()

        self.layers = [default_layer]
        self.active_layer = default_layer
        
        self.canvas_image = mip.image.Image()
        self.photo_image = None
        
    def set_transparency(self, value):
        pass

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            img = mip.image.Image()
            img.load(file_path)
            self.active_layer.addImage(img)
            self.update_canvas()            

    def save_image(self):
        if self.image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.image)

    def add_layer(self):
        if self.image is not None:
            layer = {"image": self.image.copy(), "transparency": 1.0}
            self.layers.append(layer)
            self.active_layer = layer
            self.update_canvas()

    def bring_to_front(self):
        if self.active_layer in self.layers:
            self.layers.remove(self.active_layer)
            self.layers.append(self.active_layer)
            self.update_canvas()

    def send_to_back(self):
        if self.active_layer in self.layers:
            self.layers.remove(self.active_layer)
            self.layers.insert(0, self.active_layer)
            self.update_canvas()

    def update_canvas(self):
        if self.canvas_image:
            mip.layer.display(self.canvas_image, self.layers)
            image_rgb = cv2.cvtColor(self.canvas_image.data, cv2.COLOR_BGRA2RGB)
            image_pil = Image.fromarray(image_rgb)
            self.photo_image = ImageTk.PhotoImage(image=image_pil)
            
            self.canvas.config(width=self.photo_image.width(), height=self.photo_image.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            self.canvas.image_names = self.photo_image
            
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
