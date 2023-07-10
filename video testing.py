from tkinter import *
import functools
import tkinter as tk
from tkVideoPlayer import TkinterVideo
import random
import time
import numpy as np
import pandas as pd
import openpyxl


root = Tk()

global time_start, time_end, test_output, user_profile, test_output, times_undo
global current_value, username
numvideos = 10
vid_list = random.sample(range(4,7),3)
current_value = tk.DoubleVar()
done_pressed = tk.IntVar()
done_pressed = 0
b4_changed = aft_changed = False
cur_pait = 0
no_vids = False
username = tk.StringVar()


user_profile = np.array([])
times_undo = 0
#User Output:
#[Name of User, paitient num, result, number of undos]

test_output = []

root.title("Data Recording")
root.geometry("1920x1080")

#Labels
Label(root, text= "Your name:",font={"Times New Roman", 18}).pack()

#Entry
user_name = Entry(root, width= 50, borderwidth= 5, textvariable= username).pack()

coin_flip = random.randint(0,1)

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
time_start = time.time()

test_output.append(username.get())


def load_next_set(order):
    global vid_name_before, vid_name_after, done_pressed, b4_changed, aft_changed, pait1_vid, pait2_vid, cur_pait, coin_flip, user_profile, no_vids, times_undo, username

    if(cur_pait >= len(vid_list)):
        print("Error found")
        no_vids = True
        #root.destroy()

    if(order == 'before'):
        if(not(no_vids)):
            vid_name_before = "P{}_Before.mp4".format(vid_list[cur_pait])
        else:
            vid_name_before = "P{}_Before.mp4".format(vid_list[cur_pait-1])
        b4_changed = True

    elif(order == 'after'):
        if(not(no_vids)):
            vid_name_after = "P{}_After.mp4".format(vid_list[cur_pait])
        else:
            vid_name_after = "P{}_After.mp4".format(vid_list[cur_pait-1])
        aft_changed = True
    
    if(b4_changed and aft_changed):
        time_end = time.time()
        test_output.append(time_end - time_start)

        coin_flip = random.randint(0,1)
        pait1_vid.stop()
        pait2_vid.stop()
        if(not(coin_flip)):
            pait1_vid.load(vid_name_before)
            pait2_vid.load(vid_name_after)
            test_output.append(current_value.get())
            print("New set loaded")
        else:
            pait1_vid.load(vid_name_after)
            pait2_vid.load(vid_name_before)
            test_output.append(-current_value.get())
            print("New set loaded")
        b4_changed = aft_changed = False
        done_pressed = 0
        test_output.append(times_undo)
        test_output.append(coin_flip)
        if(len(user_profile) < cur_pait*6):
            user_profile = np.append(user_profile, test_output)
        else:
            user_profile = np.array(np.split(user_profile, cur_pait-1))
            user_profile[cur_pait-1,] = test_output
        #user_profile = np.array(np.split(user_profile, cur_pait))
        if(no_vids):
            user_profile = np.array(np.split(user_profile, cur_pait))
            df = pd.DataFrame(user_profile)
            print(user_profile, df)
            test_result = pd.ExcelWriter("Perceptual_results.xlsx")
            excel_header = ["User's name", "Paitient number","Time spent(s)", "Result", "Times Undo", "Video Swapped(1 is true)"]
            df.to_excel(test_result, header= excel_header, index= False, startrow=1)
            test_result.save()
            root.destroy()
        test_output.clear()
        test_output.append(username.get())
        w2.set(0)
        


def check_done_pressed(event, videoplayer, order):
    global done_pressed
    if(done_pressed == 0):
        #loop(videoplayer)
        play_set()
    else:
        load_next_set(order)

def play_set():
    time_start = time.time()
    pait1_vid.play()
    pait2_vid.play()

    
pait1_vid.bind(
        "<<SecondChanged>>" or "<<Ended>>",
        functools.partial(
            check_done_pressed,
            videoplayer=pait1_vid,
            order = 'before'
        ),
    )


pait2_vid.bind(
        "<<SecondChanged>>" or "<<Ended>>",
        functools.partial(
            check_done_pressed,
            videoplayer=pait2_vid,
            order = 'after'
        ),
    )

def on_click_done():
    global done_pressed, cur_pait, vid_name_before, vid_name_after, vid_list
    test_output[0] = username.get()
    done_pressed = 1
    test_output.append(vid_list[cur_pait])
    cur_pait += 1
    
    
def undoCB():
    global vid_list, cur_pait, vid_name_before, vid_name_after, coin_flip, times_undo
    cur_pait = cur_pait - 1
    vid_name_before = "P{}_Before.mp4".format(vid_list[cur_pait])
    vid_name_after = "P{}_After.mp4".format(vid_list[cur_pait])
    pait1_vid.stop()
    pait2_vid.stop()

    if(not(coin_flip)):
        pait1_vid.load(vid_name_before)
        pait2_vid.load(vid_name_after)
        print("New set loaded")
    else:
        pait1_vid.load(vid_name_after)
        pait2_vid.load(vid_name_before)
        print("New set loaded")
    times_undo += 1
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
w2 = Scale(root,
           from_=-100, to=100,
           length= 600, 
           #tickinterval= 1, 
           command= slider_changed, 
           variable= current_value,  
           orient=HORIZONTAL,
           showvalue= 0)
w2.pack(fill= 'both')

Undo_button = Button(root, text= "Undo previous records", font={"Times New Roman", 18}, command= undoCB).pack(side= 'bottom',padx= 5, pady= 5)
Play_Button = Button(root, text= "Play new set", font={"Times New Roman", 18}, command= play_set).pack(side= 'bottom', padx= 5, pady= 5)
Done_Button  = Button(root, text= "Done", font={"Times New Roman", 18}, command= on_click_done).pack(side= 'bottom', padx= 5, pady= 5)

    

root.mainloop()
