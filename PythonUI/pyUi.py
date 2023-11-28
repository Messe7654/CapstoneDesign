import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import colorchooser

def handle_tool_selection(tool_value):
    print(f"선택된 도구: {tool_value}")
    update_option_frame(tool_value)
menuColor="#676d73"
def update_option_frame(tool_value):
    # 이전의 위젯들을 옵션 프레임에서 제거
    for widget in option_frame.winfo_children():
        widget.destroy()

    if tool_value == "draw":
        # "draw" 버튼이 선택된 경우 선 굵기 및 색상 옵션을 표시
        label_thickness = tkinter.Label(option_frame, text="선 굵기:", bg=menuColor, fg="#C6BB96")
        label_thickness.grid(row=0,column=0)

        thickness_slider = tkinter.Scale(option_frame,bg=menuColor, from_=1, to=20, orient=tkinter.HORIZONTAL)
        thickness_slider.set(5)  # 기본 굵기
        thickness_slider.grid(row=0,column=1)

        color_button = tkinter.Button(option_frame,fg="white",bg=menuColor, text="색상 선택", command=choose_color)
        color_button.grid(row=1, columnspan=2)
        
        # draw 버튼이 선택되었을 때만 grid_propagate를 False로 설정
        option_frame.grid_propagate(False)

    elif tool_value == "text":
        label_textSize = tkinter.Label(option_frame,text="글자 크기",bg=menuColor, fg="#C6BB96")
        label_textSize.grid(row=0,column=0)

        textSize_slider = tkinter.Scale(option_frame,bg=menuColor, from_=1, to=20, orient=tkinter.HORIZONTAL)
        textSize_slider.set(8)
        textSize_slider.grid(row=0,column=1)

        label_textcolor = tkinter.Label(option_frame,text="글자 색상",bg=menuColor, fg="#C6BB96")
        label_textcolor.grid(row=1,column=0)
        text_color = tkinter.Button(option_frame,fg="white",bg=menuColor, command=choose_color)
        text_color.grid(row=1, column=1)
        option_frame.grid_propagate(False)
    elif tool_value=="circle" or tool_value=="square":
        label_thickness = tkinter.Label(option_frame, text="선 굵기:", bg=menuColor, fg="#C6BB96")
        label_thickness.grid(row=0,column=0)

        thickness_slider = tkinter.Scale(option_frame,bg=menuColor, from_=1, to=20, orient=tkinter.HORIZONTAL)
        thickness_slider.set(5)  # 기본 굵기
        thickness_slider.grid(row=0,column=1)

        label_textcolor = tkinter.Label(option_frame,text="글자 색상",bg=menuColor, fg="#C6BB96")
        label_textcolor.grid(row=1,column=0)
        text_color = tkinter.Button(option_frame,fg="white",bg=menuColor, command=choose_color)
        text_color.grid(row=1, column=1)

        label_fillcolor = tkinter.Label(option_frame,text="채우기 색상",bg=menuColor, fg="#C6BB96")
        label_fillcolor.grid(row=2,column=0)
        fill_color = tkinter.Button(option_frame,fg="white",bg=menuColor, command=choose_color)
        fill_color.grid(row=2, column=1)
        option_frame.grid_propagate(False)
    elif tool_value=="blur":
        label_blur = tkinter.Label(option_frame, text="강도:", bg=menuColor, fg="#C6BB96")
        label_blur.grid(row=0,column=0)

        blur_slider = tkinter.Scale(option_frame,bg=menuColor, from_=1, to=100, orient=tkinter.HORIZONTAL)
        blur_slider.set(100)  # 기본 굵기
        blur_slider.grid(row=0,column=1)
        option_frame.grid_propagate(False)
    elif tool_value=="bright":
        label_bright = tkinter.Label(option_frame, text="강도:", bg=menuColor, fg="#C6BB96")
        label_bright.grid(row=0,column=0)

        bright_slider = tkinter.Scale(option_frame,bg=menuColor, from_=1, to=100, orient=tkinter.HORIZONTAL)
        bright_slider.set(100)  # 기본 굵기
        bright_slider.grid(row=0,column=1)
        option_frame.grid_propagate(False)
    else:
        # 다른 버튼이 선택된 경우 옵션 프레임을 지움
        pass

def choose_color():
    color = colorchooser.askcolor(title="색상 선택")
    if color[1]:  # 색상이 선택된 경우
        print(f"선택된 색상: {color[1]}")
def upload_file():
    file_path = filedialog.askopenfilename(title="파일 선택", filetypes=[("이미지 파일", "*.png;*.jpg;*.jpeg;*.gif")])
    print(f"선택된 파일: {file_path}")
    
    if is_image_file(file_path):
        print("성공")
    else:
        print("선택한 파일은 유효한 이미지 파일이 아닙니다.")

def is_image_file(file_path):
    try:
        image = Image.open(file_path)
        image.verify()
        return True
    except Exception as e:
        print(f"에러: {e}")
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
    ("clockwise", "./img/icons8-rotate-96.png"),
    ("counter-clockwise", "./img/icons8-ccrotate-96.png"),
    ("horizon", "./img/icons8-flip-horizontal-96.png"),
    ("vertical", "./img/icons8-flip-vertical-96.png"),
    ("draw", "./img/icons8-draw-96.png"),
    ("text", "./img/icons8-text-96.png"),
    ("square", "./img/icons8-square-96.png"),
    ("circle", "./img/icons8-circle-96.png"),
    ("bright", "./img/icons8-sun-96.png"),
    ("blur", "./img/icons8-blur-96.png"),
    ("ai", "./img/icons8-adobe-illustrator-96.png")
]
button_width = int(menu_width * 0.2)

cut_img = Image.open(tools[0][1])
cut_rimg = cut_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
cut_tool = ImageTk.PhotoImage(cut_rimg)

cut_button = tkinter.Radiobutton(tool_frame, image=cut_tool,
                variable=tool, value=tools[0][0], command=lambda tool_name=tools[0][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
cut_button.image = cut_tool
cut_button.grid(row=0, column=0)

clock_img = Image.open(tools[1][1])
clock_rimg = clock_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
clock_tool = ImageTk.PhotoImage(clock_rimg)

clock_button = tkinter.Radiobutton(tool_frame, image=clock_tool,
                variable=tool, value=tools[1][0], command=lambda tool_name=tools[1][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
clock_button.image = clock_tool
clock_button.grid(row=0, column=1)

cntclock_img = Image.open(tools[2][1])
cntclock_rimg = cntclock_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
cntclock_tool = ImageTk.PhotoImage(cntclock_rimg)

cntclock_button = tkinter.Radiobutton(tool_frame, image=cntclock_tool,
                variable=tool, value=tools[2][0], command=lambda tool_name=tools[2][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
cntclock_button.image = cntclock_tool
cntclock_button.grid(row=0, column=2)

horizon_img = Image.open(tools[3][1])
horizon_rimg = horizon_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
horizon_tool = ImageTk.PhotoImage(horizon_rimg)

horizon_button = tkinter.Radiobutton(tool_frame, image=horizon_tool,
                variable=tool, value=tools[3][0], command=lambda tool_name=tools[3][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
horizon_button.image = horizon_tool
horizon_button.grid(row=0, column=3)

vertical_img = Image.open(tools[4][1])
vertical_rimg = vertical_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
vertical_tool = ImageTk.PhotoImage(vertical_rimg)

vertical_button = tkinter.Radiobutton(tool_frame, image=vertical_tool,
                variable=tool, value=tools[4][0], command=lambda tool_name=tools[4][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
vertical_button.image = vertical_tool
vertical_button.grid(row=1, column=0)

draw_img = Image.open(tools[5][1])
draw_rimg = draw_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
draw_tool = ImageTk.PhotoImage(draw_rimg)

draw_button = tkinter.Radiobutton(tool_frame, image=draw_tool,
                variable=tool, value=tools[5][0], command=lambda tool_name=tools[5][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
draw_button.image = draw_tool
draw_button.grid(row=1, column=1)

text_img = Image.open(tools[6][1])
text_rimg = text_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
text_tool = ImageTk.PhotoImage(text_rimg)

text_button = tkinter.Radiobutton(tool_frame, image=text_tool,
                variable=tool, value=tools[6][0], command=lambda tool_name=tools[6][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
text_button.image = text_tool
text_button.grid(row=1, column=2)

square_img = Image.open(tools[7][1])
square_rimg = square_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
square_tool = ImageTk.PhotoImage(square_rimg)

square_button = tkinter.Radiobutton(tool_frame, image=square_tool,
                variable=tool, value=tools[7][0], command=lambda tool_name=tools[7][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
square_button.image = square_tool
square_button.grid(row=1, column=3)

circle_img = Image.open(tools[8][1])
circle_rimg = circle_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
circle_tool = ImageTk.PhotoImage(circle_rimg)

circle_button = tkinter.Radiobutton(tool_frame, image=circle_tool,
                variable=tool, value=tools[8][0], command=lambda tool_name=tools[8][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
circle_button.image = circle_tool
circle_button.grid(row=2, column=0)

bright_img = Image.open(tools[9][1])
bright_rimg = bright_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
bright_tool = ImageTk.PhotoImage(bright_rimg)

bright_button = tkinter.Radiobutton(tool_frame, image=bright_tool,
                variable=tool, value=tools[9][0], command=lambda tool_name=tools[9][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
bright_button.image = bright_tool
bright_button.grid(row=2, column=1)

blur_img = Image.open(tools[10][1])
blur_rimg = blur_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
blur_tool = ImageTk.PhotoImage(blur_rimg)

blur_button = tkinter.Radiobutton(tool_frame, image=blur_tool,
                variable=tool, value=tools[10][0], command=lambda tool_name=tools[10][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
blur_button.image = blur_tool
blur_button.grid(row=2, column=2)

ai_img = Image.open(tools[11][1])
ai_rimg = ai_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
ai_tool = ImageTk.PhotoImage(ai_rimg)

ai_button = tkinter.Radiobutton(tool_frame, image=ai_tool,
                variable=tool, value=tools[11][0], command=lambda tool_name=tools[11][0]: handle_tool_selection(tool_name),
                compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                 padx=30, pady=10)
ai_button.image = ai_tool
ai_button.grid(row=2, column=3)






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
