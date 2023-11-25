import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk

def handle_tool_selection(tool_value): #버튼클릭시 임시 실행 함수
    print(f"Selected Tool: {tool_value}")

def upload_file():
    file_path = filedialog.askopenfilename(title="Choose a file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    print(f"Selected file: {file_path}")
    
    if is_image_file(file_path):
        print("success")
    else:
        print("Selected file is not a valid image file.")

def is_image_file(file_path):
    try:
        image = Image.open(file_path)
        image.verify()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

window = tkinter.Tk()
window.title("포토그래퍼")
window.resizable(False, False)

window_width = int(window.winfo_screenwidth() * 0.8)
window_height = int((window.winfo_screenheight() * 0.8))
window.geometry(f"{window_width}x{window_height}")

menu_width = int(window_width * 0.15)
menu_height = int(window_height * 0.9)

tool_height = int(menu_height * 0.25)  
tool_frame = tkinter.Frame(window, bg="#676d73", width=menu_width, height=tool_height)
tool_frame.grid(row=0, column=0, sticky="se", padx=0, pady=0)

tool = tkinter.StringVar()
tools = [
    ("cut", "./img/icons8-crop-96.png"),
    ("clockwise", "blur.png"),
    ("counter-clockwise", "blur.png"),
    ("horizon", "blur.png"),
    ("vertical", "blur.png"),
    ("draw", "./img/icons8-draw-96.png"),
    ("text", "./img/icons8-text-96.png"),
    ("square", "./img/icons8-square-96.png"),
    ("circle", "./img/icons8-circle-96.png"),
    ("bright", "./img/icons8-sun-96.png"),
    ("blur", "./img/icons8-blur-96.png"),
    ("ai", "./img/icons8-adobe-illustrator-96.png")
]
button_width = int(menu_width * 0.2)
row, col = 0, 0
for tool_name, image_path in tools:
    original_image = Image.open(image_path)
    resized_image = original_image.resize((int(button_width * 0.9), int(button_width * 0.9)))
    tool_image = ImageTk.PhotoImage(resized_image)

    tool_button = tkinter.Radiobutton(tool_frame, image=tool_image,
                                      variable=tool, value=tool_name, command=lambda tool_name=tool_name: handle_tool_selection(tool_name),
                                      compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                                      padx=30, pady=10)
    tool_button.image = tool_image
    tool_button.grid(row=row, column=col)

    col += 1
    if col > 3: 
        col = 0
        row += 1

tool_frame.grid_propagate(False)

option_height = int(menu_height * 0.75) 
option_frame = tkinter.Frame(window, bg="#676d73", width=menu_width, height=option_height)
option_frame.grid(row=1, column=0, padx=0, pady=0)


canvas_width = int((window_width / 100) * 85)
canvas_height = int((window_height / 100) * 90)
canvas = tkinter.Canvas(window, relief="solid", bg="#dadcdc", width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=1, rowspan=2, sticky="se", padx=0, pady=0)

bottom_height = int(window_height * 0.1)
bottom_frame = tkinter.Frame(window, bg="#161615", width=window_width, height=bottom_height)
bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nw", padx=0, pady=0)  

upload_button = tkinter.Button(bottom_frame, text="Upload File", command=upload_file, height=int(bottom_height * 0.))
upload_button.grid(row=0, column=0)
undo_image = Image.open("./img/icons8-undo-96.png")
redo_image = Image.open("./img/icons8-redo-96.png")

undo_image = undo_image.resize((int(bottom_height * 0.7), int(bottom_height * 0.8)))
redo_image = redo_image.resize((int(bottom_height * 0.7), int(bottom_height * 0.8)))

undo_photo = ImageTk.PhotoImage(undo_image)
redo_photo = ImageTk.PhotoImage(redo_image)

undo_button = tkinter.Button(bottom_frame, image=undo_photo)
redo_button = tkinter.Button(bottom_frame, image=redo_photo)
download_button = tkinter.Button(bottom_frame, text="다운로드", height=int(window_height * 0.001))  

undo_button.image = undo_photo
redo_button.image = redo_photo
undo_button.grid(row=0, column=0,padx=(int(window_width*0.45),0))  
redo_button.grid(row=0, column=1,padx=(int(window_width*0.05),0))  
upload_button.grid(row=0, column=2,padx=(int(window_width*0.25),0)) 
download_button.grid(row=0, column=3,padx=(int(window_width*0.01),0))  

bottom_frame.grid_propagate(False)
window.mainloop()
