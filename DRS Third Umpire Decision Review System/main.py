import tkinter
from tkinter.constants import ANCHOR, W 
import cv2                  #pip install opencv-python
import PIL.Image, PIL.ImageTk               #pip install pillow  
from functools import partial
import threading
import imutils
import time

# Width and height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368
flag = True
stream = cv2.VideoCapture("clip.mp4")
def play(speed):
    global flag
    print(f"video played and speed is {speed}")
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)
    grabbed, frame = stream.read()
    if not grabbed:
        # canvas.create_text(134, 26, fill="black", font="Times 20 italic bold", text="clip ended")
        return
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    if flag:
        canvas.create_text(134, 26, fill="black", font="Times 20 italic bold", text="Decision Pending")
    flag = not flag
def pending(decision):
    # 1. display decision pending image  
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    # 2. wait for a second
    time.sleep(1)
    # 3. display sponsor image 
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    # 4. wait for 1.5 second
    time.sleep(1.5)
    # 5. display decision out or not out
    frame = cv2.cvtColor(cv2.imread(f"{decision}.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    # 6. wait for 1.5 second
    time.sleep(1.5)



def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()

def notout():
    thread = threading.Thread(target=pending, args=("not_out",))
    thread.daemon = 1
    thread.start()
    print(f"player not out")

# Tkinter gui starts here
window = tkinter.Tk()
window.title("DRS Third Umpire Decision Review System Kit")
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
Img_on_Canvas =  canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

btn = tkinter.Button(window, text="<< Previous (Fast) <<", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (Slow) <<", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text=">> Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text=">> Next (Fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=notout)
btn.pack()

window.mainloop()

