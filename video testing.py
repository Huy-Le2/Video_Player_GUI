from tkinter import *
import functools
import tkinter as tk
from tkVideoPlayer import TkinterVideo
import random
import time


root = Tk()

numvideos = 10
vid_list = random.sample(range(4,7),3)
current_value = tk.DoubleVar()
done_pressed = tk.IntVar()
done_pressed = 0
b4_changed = aft_changed = False
cur_pait = 0

root.title("Data Recording")
root.geometry("1920x1080")
root.resizable(False, False)

#Labels
Label(root, text= "Your name:",font={"Times New Roman", 18}).pack()

#Entry
user_name = Entry(root, width= 50, borderwidth= 5).pack()

vid_name_before = "P{}_Before.mp4".format(vid_list[cur_pait])
vid_name_after = "P{}_After.mp4".format(vid_list[cur_pait])

pait1_vid = TkinterVideo(scaled= True, master= root)
pait1_vid.set_size(size=(854,480), keep_aspect= True)
pait1_vid.load(vid_name_before)
pait1_vid.pack(side='left', fill= 'both', expand= True)
pait1_vid.play()

pait2_vid = TkinterVideo(scaled= True, master= root)
pait2_vid.set_size(size=(854,480), keep_aspect= True)
pait2_vid.load(vid_name_after)
pait2_vid.pack(side='right', fill= 'both', expand= True)
pait2_vid.play()

def load_next_set(order):
    global vid_name_before, vid_name_after, done_pressed, b4_changed, aft_changed, pait1_vid, pait2_vid, cur_pait

    print("New set for paitient {}".format(vid_list[cur_pait]), b4_changed, aft_changed)
    
    if(order == 'before'):
        vid_name_before = "P{}_Before.mp4".format(vid_list[cur_pait])
        b4_changed = True

    elif(order == 'after'):
        vid_name_after = "P{}_After.mp4".format(vid_list[cur_pait])
        aft_changed = True
    
    if(b4_changed and aft_changed):
        pait1_vid.stop()
        pait2_vid.stop()
        pait1_vid.load(vid_name_before)
        pait2_vid.load(vid_name_after)

        print("New set loaded")
        b4_changed = aft_changed = False
        done_pressed = 0
        print(done_pressed, aft_changed, b4_changed)
    

def loop(videoplayer):
    videoplayer.play()

def check_done_pressed(event, videoplayer, order):
    global done_pressed
    if(done_pressed == 0):
        loop(videoplayer)
    else:
        load_next_set(order)

def play_set():
    pait1_vid.play()
    pait2_vid.play()
    

    
pait1_vid.bind(
        "<<SecondChanged>>",
        functools.partial(
            check_done_pressed,
            videoplayer=pait1_vid,
            order = 'before'
        ),
    )

pait2_vid.bind(
        "<<SecondChanged>>",
        functools.partial(
            check_done_pressed,
            videoplayer=pait2_vid,
            order = 'after'
        ),
    )

def on_click_done():
    global done_pressed, cur_pait, vid_name_before, vid_name_after, vid_list
    done_pressed = 1
    cur_pait += 1
    print(vid_list[cur_pait], vid_name_before, vid_name_after)
    
def get_current_value():
    return '{: .2f}'.format(current_value.get()) 
    
def slider_changed(event):
    value_label.configure(text=get_current_value())

# current value label
current_value_label = tk.Label(
    root,
    text='Current Value:'
)

current_value_label.pack()

# value label
value_label = tk.Label(
    root,
    text=get_current_value()
)
value_label.pack()

#Scale slider
w2 = Scale(root, from_=-100, to=100, 
           length= 600, 
           tickinterval= 1, 
           command= slider_changed, 
           variable= current_value,  
           orient=HORIZONTAL)
w2.pack(fill= 'both')


Undo_button = Button(root, text= "Undo previous records", font={"Times New Roman", 18}, command= on_click_done).pack(side= 'bottom',padx= 5, pady= 5)
Play_Button = Button(root, text= "Play new set", font={"Times New Roman", 18}, command= play_set).pack(side= 'bottom', padx= 5, pady= 5)
Done_Button  = Button(root, text= "Done", font={"Times New Roman", 18}, command= on_click_done).pack(side= 'bottom', padx= 5, pady= 5)

root.mainloop()