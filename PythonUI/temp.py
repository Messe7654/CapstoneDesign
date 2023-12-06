import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import colorchooser
import mymodule as mip
import AI as mai
import cv2
from collections import deque
import math

class ImagerEditor:
    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.root.title("Image Editor")
        self.root.resizable(True, True)
        
        window_width = int(root.winfo_screenwidth() * 0.8)
        window_height = int((root.winfo_screenheight() * 0.8))
        root.geometry(f"{window_width}x{window_height}")
        
        menu_width = int(window_width * 0.08)
        menu_height = int(window_height * 0.9)
        self.menu_color = "#D9D9D9"
        
        self.tool_frame = tkinter.Frame(root, bg="#D9D9D9", width=menu_width, height=menu_height)
        self.tool_frame.grid(row=0, column=0, sticky="se", padx=0, pady=0)
        
        canvas_width = int(window_width * 0.77)
        canvas_height = int(window_height * 0.9)
        self.canvas = tkinter.Canvas(root, relief="solid", bg="#FFFFFF", width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=1, sticky="se", padx=0, pady=0)

        layer_frame_width = int(window_width * 0.15)
        layer_frame_height = int(window_height * 0.9)
        self.layer_frame = tkinter.Frame(root, bg="#D9D9D9",
                                         width=layer_frame_width,
                                         height=layer_frame_height)
        self.layer_frame.grid(row=0, column=2, sticky="se", padx=0, pady=0)

        bottom_height = int(window_height * 0.1)
        self.bottom_frame = tkinter.Frame(root, bg="#929292", width=window_width, height=bottom_height)
        self.bottom_frame.grid(row=1, column=0, columnspan=3, sticky="nw", padx=0, pady=0)  

        self.add_widgets()
        
        thumbnail_width = int(layer_frame_width * 0.8)
        thumbnail_height = int(thumbnail_width * 9 / 16)
        
        self.thumbnail_list = deque()
        
        default_layer = mip.layer.Layer()

        self.layers = [default_layer]
        self.active_layer = default_layer
        
        add_photo = tkinter.PhotoImage(file="./PythonUI/img/icons8-add-100.png")
        self.add_layer_button = tkinter.Button(self.layer_frame, image=add_photo, pady=10)
        self.add_layer_button.image = add_photo
        self.layer_frame.pack_propagate(False)
        self.add_layer_button.pack(pady=10)
        
        self.canvas_image = mip.image.Image()
        self.photo_image = None
        
        self.model = mai.ai_model.make_model(num_filters=64, num_of_residual_blocks=16)
        checkpoint_path = "./AI/training_1/cp.ckpt"
        self.model.load_weights(checkpoint_path)
        
        self.selected_tool = None
        self.line1 = None
        self.line2 = None
        self.canvas_text = None
        
        self.canvas.bind("<Button-1>", self.getEvent_Button_1)
        self.canvas.bind("<B1-Motion>", self.getEvent_B1_Motion)
        self.canvas.bind("<ButtonRelease-1>", self.getEvent_ButtonRelease_1)    
    
    def add_widgets(self):
        window_width = int(root.winfo_screenwidth() * 0.8)
        window_height = int((root.winfo_screenheight() * 0.8))
        menu_width = int(window_width * 0.08)
        menu_height = int(window_height * 0.9)
        bottom_height = int(window_height * 0.1)
        
        self.tool = tkinter.StringVar()
        self.tool_list = [
            ("cut", "./PythonUI/img/icons8-crop-96.png"),
            ("clockwise", "./PythonUI/img/icons8-rotate-96.png"),
            ("counter-clockwise", "./PythonUI/img/icons8-ccrotate-96.png"),
            ("horizon", "./PythonUI/img/icons8-flip-horizontal-96.png"),
            ("vertical", "./PythonUI/img/icons8-flip-vertical-96.png"),
            ("draw", "./PythonUI/img/icons8-draw-96.png"),
            ("text", "./PythonUI/img/icons8-text-96.png"),
            ("square", "./PythonUI/img/icons8-square-96.png"),
            ("circle", "./PythonUI/img/icons8-circle-96.png"),
            ("bright", "./PythonUI/img/icons8-sun-96.png"),
            ("blur", "./PythonUI/img/icons8-blur-96.png"),
            ("ai", "./PythonUI/img/icons8-adobe-illustrator-96.png")
        ]
        
        button_width = int(menu_width * 0.55)
        button_pad = int(menu_width * 0.27)

        cut_img = Image.open(self.tool_list[0][1])
        cut_rimg = cut_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        cut_tool = ImageTk.PhotoImage(cut_rimg)

        self.cut_button = tkinter.Radiobutton(self.tool_frame, image=cut_tool,
                        variable=self.tool, value=self.tool_list[0][0], command=lambda tool_name=self.tool_list[0][0]: self.handle_tool_selection(tool_name),
                        compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                        padx=30, pady=10, bg=self.menu_color, bd=0, selectcolor="#ACACAC")
        self.cut_button.image = cut_tool
        self.cut_button.grid(row=0, padx=button_pad)

        clock_img = Image.open(self.tool_list[1][1])
        clock_rimg = clock_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        clock_tool = ImageTk.PhotoImage(clock_rimg)

        self.clock_button = tkinter.Radiobutton(self.tool_frame, image=clock_tool,
                        variable=self.tool, value=self.tool_list[1][0], command=lambda tool_name=self.tool_list[1][0]: self.handle_tool_selection(tool_name),
                        compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                        padx=30, pady=10, bg=self.menu_color, bd=0, selectcolor="#ACACAC")
        self.clock_button.image = clock_tool
        # self.clock_button.grid(row=0, column=1)
        self.clock_button.grid(row=1)

        # cntclock_img = Image.open(self.tool_list[2][1])
        # cntclock_rimg = cntclock_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        # cntclock_tool = ImageTk.PhotoImage(cntclock_rimg)

        # self.cntclock_button = tkinter.Radiobutton(self.tool_frame, image=cntclock_tool,
        #                 variable=self.tool, value=self.tool_list[2][0], command=lambda tool_name=self.tool_list[2][0]: self.handle_tool_selection(tool_name),
        #                 compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
        #                 padx=30, pady=10)
        # self.cntclock_button.image = cntclock_tool
        # self.cntclock_button.grid(row=0, column=2)

        horizon_img = Image.open(self.tool_list[3][1])
        horizon_rimg = horizon_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        horizon_tool = ImageTk.PhotoImage(horizon_rimg)

        self.horizon_button = tkinter.Radiobutton(self.tool_frame, image=horizon_tool,
                        variable=self.tool, value=self.tool_list[3][0], command=lambda tool_name=self.tool_list[3][0]: self.handle_tool_selection(tool_name),
                        compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                        padx=30, pady=10, bg=self.menu_color, bd=0, selectcolor="#ACACAC")
        self.horizon_button.image = horizon_tool
        # self.horizon_button.grid(row=0, column=3)
        self.horizon_button.grid(row=2)

        vertical_img = Image.open(self.tool_list[4][1])
        vertical_rimg = vertical_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        vertical_tool = ImageTk.PhotoImage(vertical_rimg)

        self.vertical_button = tkinter.Radiobutton(self.tool_frame, image=vertical_tool,
                        variable=self.tool, value=self.tool_list[4][0], command=lambda tool_name=self.tool_list[4][0]: self.handle_tool_selection(tool_name),
                        compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                        padx=30, pady=10, bg=self.menu_color, bd=0, selectcolor="#ACACAC")
        self.vertical_button.image = vertical_tool
        # self.vertical_button.grid(row=1, column=0)
        self.vertical_button.grid(row=3)

        draw_img = Image.open(self.tool_list[5][1])
        draw_rimg = draw_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        draw_tool = ImageTk.PhotoImage(draw_rimg)

        self.draw_button = tkinter.Radiobutton(self.tool_frame, image=draw_tool,
                        variable=self.tool, value=self.tool_list[5][0], command=lambda tool_name=self.tool_list[5][0]: self.handle_tool_selection(tool_name),
                        compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                        padx=30, pady=10, bg=self.menu_color, bd=0, selectcolor="#ACACAC")
        self.draw_button.image = draw_tool
        # self.draw_button.grid(row=1, column=1)
        self.draw_button.grid(row=4)

        text_img = Image.open(self.tool_list[6][1])
        text_rimg = text_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        text_tool = ImageTk.PhotoImage(text_rimg)

        self.text_button = tkinter.Radiobutton(self.tool_frame, image=text_tool,
                        variable=self.tool, value=self.tool_list[6][0], command=lambda tool_name=self.tool_list[6][0]: self.handle_tool_selection(tool_name),
                        compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                        padx=30, pady=10, bg=self.menu_color, bd=0, selectcolor="#ACACAC")
        self.text_button.image = text_tool
        # self.text_button.grid(row=1, column=2)
        self.text_button.grid(row=5)

        # square_img = Image.open(self.tool_list[7][1])
        # square_rimg = square_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        # square_tool = ImageTk.PhotoImage(square_rimg)

        # self.square_button = tkinter.Radiobutton(self.tool_frame, image=square_tool,
        #                 variable=self.tool, value=self.tool_list[7][0], command=lambda tool_name=self.tool_list[7][0]: self.handle_tool_selection(tool_name),
        #                 compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
        #                 padx=30, pady=10)
        # self.square_button.image = square_tool
        # self.square_button.grid(row=1, column=3)

        # circle_img = Image.open(self.tool_list[8][1])
        # circle_rimg = circle_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        # circle_tool = ImageTk.PhotoImage(circle_rimg)

        # self.circle_button = tkinter.Radiobutton(self.tool_frame, image=circle_tool,
        #                 variable=self.tool, value=self.tool_list[8][0], command=lambda tool_name=self.tool_list[8][0]: self.handle_tool_selection(tool_name),
        #                 compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
        #                 padx=30, pady=10)
        # self.circle_button.image = circle_tool
        # self.circle_button.grid(row=2, column=0)

        # bright_img = Image.open(self.tool_list[9][1])
        # bright_rimg = bright_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        # bright_tool = ImageTk.PhotoImage(bright_rimg)

        # self.bright_button = tkinter.Radiobutton(self.tool_frame, image=bright_tool,
        #                 variable=self.tool, value=self.tool_list[9][0], command=lambda tool_name=self.tool_list[9][0]: self.handle_tool_selection(tool_name),
        #                 compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
        #                 padx=30, pady=10)
        # self.bright_button.image = bright_tool
        # self.bright_button.grid(row=2, column=1)

        # blur_img = Image.open(self.tool_list[10][1])
        # blur_rimg = blur_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        # blur_tool = ImageTk.PhotoImage(blur_rimg)

        # self.blur_button = tkinter.Radiobutton(self.tool_frame, image=blur_tool,
        #                 variable=self.tool, value=self.tool_list[10][0], command=lambda tool_name=self.tool_list[10][0]: self.handle_tool_selection(tool_name),
        #                 compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
        #                 padx=30, pady=10)
        # self.blur_button.image = blur_tool
        # self.blur_button.grid(row=2, column=2)

        ai_img = Image.open(self.tool_list[11][1])
        ai_rimg = ai_img.resize((int(button_width * 0.9), int(button_width * 0.9)))
        ai_tool = ImageTk.PhotoImage(ai_rimg)

        self.ai_button = tkinter.Radiobutton(self.tool_frame, image=ai_tool,
                        variable=self.tool, value=self.tool_list[11][0], command=lambda tool_name=self.tool_list[11][0]: self.handle_tool_selection(tool_name),
                        compound=tkinter.LEFT, width=button_width, height=button_width, indicatoron=0,
                        padx=30, pady=10, bg=self.menu_color, bd=0, selectcolor="#ACACAC")
        self.ai_button.image = ai_tool
        # self.ai_button.grid(row=2, column=3)
        self.ai_button.grid(row=6)

        self.tool_frame.grid_propagate(False)

        option_height = int(menu_height * 0.75) 
        self.option_frame = tkinter.Frame(root, bg="#D9D9D9", width=menu_width, height=option_height)
        self.option_frame.grid(row=1, column=0, padx=0, pady=0)
        
        self.upload_button = tkinter.Button(self.bottom_frame,
                                            text="Upload File",
                                            font=("Arial", 16),
                                            command=self.upload_file,
                                            bd=0,
                                            bg="#D9D9D9",
                                            height=2,
                                            width=10)
        self.upload_button.grid(row=0, column=0, pady=10)
        undo_image = Image.open("./PythonUI/img/icons8-undo-96.png")
        redo_image = Image.open("./PythonUI/img/icons8-redo-96.png")
        
        undo_image = undo_image.resize((int(bottom_height * 0.7), int(bottom_height * 0.8)))
        redo_image = redo_image.resize((int(bottom_height * 0.7), int(bottom_height * 0.8)))

        undo_photo = ImageTk.PhotoImage(undo_image)
        redo_photo = ImageTk.PhotoImage(redo_image)

        self.undo_button = tkinter.Button(self.bottom_frame, image=undo_photo, bg="#929292", bd=0)
        self.redo_button = tkinter.Button(self.bottom_frame, image=redo_photo, bg="#929292", bd=0)
        self.download_button = tkinter.Button(self.bottom_frame,
                                              text="Download File",
                                              font=("Arial", 16),
                                              bd=0,
                                              bg="#D9D9D9",
                                              height=2,
                                              width=12)  

        self.undo_button.image = undo_photo
        self.redo_button.image = redo_photo
        self.undo_button.grid(row=0, column=0,padx=(int(window_width*0.45),0))  
        self.redo_button.grid(row=0, column=1,padx=(int(window_width*0.05),0))  
        self.upload_button.grid(row=0, column=2,padx=(int(window_width*0.1),0)) 
        self.download_button.grid(row=0, column=3,padx=(int(window_width*0.02),0))  

        self.bottom_frame.grid_propagate(False)
    
    def handle_tool_selection(self, tool_name):
        self.selected_tool = tool_name
        self.update_option_frame()
        
    def update_option_frame(self):
        for widget in self.option_frame.winfo_children():
            widget.destroy()
        
        if self.selected_tool == "draw":
            # "draw" 버튼이 선택된 경우 선 굵기 및 색상 옵션을 표시
            label_thickness = tkinter.Label(self.option_frame, text="선 굵기:", bg=self.menu_color, fg="#C6BB96")
            label_thickness.grid(row=0,column=0)

            thickness_slider = tkinter.Scale(self.option_frame,bg=self.menu_color, from_=1, to=20, orient=tkinter.HORIZONTAL)
            thickness_slider.set(5)  # 기본 굵기
            thickness_slider.grid(row=0,column=1)

            color_button = tkinter.Button(self.option_frame,fg="white",bg=self.menu_color, text="색상 선택", command=self.choose_color)
            color_button.grid(row=1, columnspan=2)
            
            # draw 버튼이 선택되었을 때만 grid_propagate를 False로 설정
            self.option_frame.grid_propagate(False)

        elif self.selected_tool == "text":
            label_textSize = tkinter.Label(self.option_frame,text="글자 크기",bg=self.menu_color, fg="#C6BB96")
            label_textSize.grid(row=0,column=0)

            textSize_slider = tkinter.Scale(self.option_frame,bg=self.menu_color, from_=1, to=20, orient=tkinter.HORIZONTAL)
            textSize_slider.set(8)
            textSize_slider.grid(row=0,column=1)

            label_textcolor = tkinter.Label(self.option_frame,text="글자 색상",bg=self.menu_color, fg="#C6BB96")
            label_textcolor.grid(row=1,column=0)
            text_color = tkinter.Button(self.option_frame,fg="white",bg=self.menu_color, command=self.choose_color)
            text_color.grid(row=1, column=1)
            self.option_frame.grid_propagate(False)
            
        elif self.selected_tool=="circle" or self.selected_tool=="square":
            label_thickness = tkinter.Label(self.option_frame, text="선 굵기:", bg=self.menu_color, fg="#C6BB96")
            label_thickness.grid(row=0,column=0)

            thickness_slider = tkinter.Scale(self.option_frame,bg=self.menu_color, from_=1, to=20, orient=tkinter.HORIZONTAL)
            thickness_slider.set(5)  # 기본 굵기
            thickness_slider.grid(row=0,column=1)

            label_textcolor = tkinter.Label(self.option_frame,text="글자 색상",bg=self.menu_color, fg="#C6BB96")
            label_textcolor.grid(row=1,column=0)
            text_color = tkinter.Button(self.option_frame,fg="white",bg=self.menu_color, command=self.choose_color)
            text_color.grid(row=1, column=1)

            label_fillcolor = tkinter.Label(self.option_frame,text="채우기 색상",bg=self.menu_color, fg="#C6BB96")
            label_fillcolor.grid(row=2,column=0)
            fill_color = tkinter.Button(self.option_frame,fg="white",bg=self.menu_color, command=self.choose_color)
            fill_color.grid(row=2, column=1)
            self.option_frame.grid_propagate(False)
            
        elif self.selected_tool=="blur":
            label_blur = tkinter.Label(self.option_frame, text="강도:", bg=self.menu_color, fg="#C6BB96")
            label_blur.grid(row=0,column=0)

            blur_slider = tkinter.Scale(self.option_frame,bg=self.menu_color, from_=1, to=100, orient=tkinter.HORIZONTAL)
            blur_slider.set(100)  # 기본 굵기
            blur_slider.grid(row=0,column=1)
            self.option_frame.grid_propagate(False)
            
        elif self.selected_tool=="bright":
            label_bright = tkinter.Label(self.option_frame, text="강도:", bg=self.menu_color, fg="#C6BB96")
            label_bright.grid(row=0,column=0)

            bright_slider = tkinter.Scale(self.option_frame,bg=self.menu_color, from_=1, to=100, orient=tkinter.HORIZONTAL)
            bright_slider.set(100)  # 기본 굵기
            bright_slider.grid(row=0,column=1)
            self.option_frame.grid_propagate(False)
        
        elif self.selected_tool == "horizon":
            self.flip_horizon()
            
        elif self.selected_tool == "vertical":
            self.flip_vertical()
        
        elif self.selected_tool == "ai":
            upscaled = self.model.predict_step(self.active_layer.view.getImagePIL())
            self.active_layer.setImage(upscaled)
            self.update_canvas()
        else:
            # 다른 버튼이 선택된 경우 옵션 프레임을 지움
            pass
        
    def choose_color(self):
        self.color = colorchooser.askcolor(title="색상 선택")
        if self.color[1]:  # 색상이 선택된 경우
            print(f"선택된 색상: {self.color[1]}")
            
    def upload_file(self):
        file_path = filedialog.askopenfilename(title="파일 선택", filetypes=[("이미지 파일", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            img = mip.image.Image()
            img.load(file_path)
            self.active_layer.addImage(img)
            self.update_canvas()
            
    def flip_horizon(self):
        self.active_layer.flip(mip.layer.Layer.FLIP_HORIZONTAL)
        self.update_canvas()
        
    def flip_vertical(self):
        self.active_layer.flip(mip.layer.Layer.FLIP_VERTICAL)
        self.update_canvas()
        
    def update_canvas(self):
        if self.canvas_image:
            mip.layer.display(self.canvas_image, self.layers)
            self.photo_image = self.canvas_image.getThumbnail()
            
            # self.canvas.config(width=self.photo_image.width(), height=self.photo_image.height())
            self.canvas.create_image(1, 1, anchor=tkinter.NW, image=self.photo_image)
            self.canvas.image_names = self.photo_image
            
    def getEvent_B1_Motion(self, event):
        if self.selected_tool is None:
            pass
        if self.selected_tool == "clockwise":
            if self.line2:
                self.canvas.delete(self.line2)
                self.line2 = None
                
            if self.canvas_text:
                self.canvas.delete(self.canvas_text)
                self.canvas_text = None
                
            x, y = event.x, event.y
            
            w, h = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()
            centerx, centery = w//2, h//2
            
            line_length = 300
            
            v1 = [0, 1]
            v2 = [x - centerx, y - centery]
            position_length = self.vector_magnitude(v2)
            degree = self.angle_between_vectors(v1, v2)
            
            endx = centerx + v2[0] * line_length // position_length
            endy = centery + v2[1] * line_length // position_length
            
            self.line1 = self.canvas.create_line(centerx, centery, centerx, centery-line_length,
                                                 width=4, fill="#EEEEEE")
            self.line2 = self.canvas.create_line(centerx, centery, endx, endy,
                                                 width=4, fill="#EEEEEE")
            self.canvas_text = self.canvas.create_text(centerx + 40, centery - line_length,
                                                       font=('Arial', 20),
                                                       text=str(int(degree)),
                                                       fill="#EEEEEE")
            
    
    def getEvent_Button_1(self, event):
        if self.selected_tool is None:
            pass
        if self.selected_tool == "clockwise":
            if self.line2:
                self.canvas.delete(self.line2)
                self.line2 = None
            
            if self.canvas_text:
                self.canvas.delete(self.canvas_text)
                self.canvas_text = None
            
            x, y = event.x, event.y
            
            w, h = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()
            centerx, centery = w//2, h//2
            
            line_length = 300
            
            v1 = [0, 1]
            v2 = [x - centerx, y - centery]
            position_length = self.vector_magnitude(v2)
            degree = self.angle_between_vectors(v1, v2)
            
            endx = centerx + v2[0] * line_length // position_length
            endy = centery + v2[1] * line_length // position_length
            
            self.line1 = self.canvas.create_line(centerx, centery, centerx, centery-line_length,
                                                 width=4, fill="#EEEEEE")
            self.line2 = self.canvas.create_line(centerx, centery, endx, endy,
                                                 width=4, fill="#EEEEEE")
            self.canvas_text = self.canvas.create_text(centerx + 40, centery - line_length,
                                                       font=('Arial', 20),
                                                       text=str(int(degree)),
                                                       fill="#EEEEEE")
            
    def getEvent_ButtonRelease_1(self, event):
        if self.selected_tool is None:
            pass
        if self.selected_tool == "clockwise":
            x, y = event.x, event.y

            w, h = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()
            centerx, centery = w//2, h//2
            
            v1 = [0, 1]            
            v2 = [x - centerx, y - centery]
            degree = self.angle_between_vectors(v1, v2)
            
            self.active_layer.rotate(degree)
            
            self.canvas.delete(self.line1)
            self.canvas.delete(self.line2)
            self.canvas.delete(self.canvas_text)
            
            self.line1 = None
            self.line2 = None
            self.canvas_text = None
            
            self.update_canvas()
            
    def dot_product(self, v1, v2):
        return sum(x * y for x, y in zip(v1, v2))
    
    def cross_product_magnitude(self, v1, v2):
        return (v1[0] * v2[1] - v1[1] * v2[0])

    def vector_magnitude(self, v):
        return math.sqrt(sum(x**2 for x in v))

    def angle_between_vectors(self, v1, v2):
        dot = self.dot_product(v1, v2)
        cross_mag = self.cross_product_magnitude(v1, v2)
        mag_v1 = self.vector_magnitude(v1)
        mag_v2 = self.vector_magnitude(v2)

        # Avoid division by zero
        if mag_v1 == 0 or mag_v2 == 0:
            return None

        cos_theta = dot / (mag_v1 * mag_v2)

        # The arccosine function returns the angle in radians, so we convert it to degrees
        angle_in_radians = math.acos(cos_theta)
        angle_in_degrees = math.degrees(angle_in_radians)

        if cross_mag < 0:
            angle_in_degrees = 360 - angle_in_degrees
        return (angle_in_degrees + 180) % 360
    
if __name__ == "__main__":
    root = tkinter.Tk()
    app = ImagerEditor(root)
    root.mainloop()