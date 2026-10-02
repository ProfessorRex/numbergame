# import everything from tkinter module 
import tkinter as tk
import tkinter.font as font
import numgame as ng
from myimages import *
import base64
import os

#from win32gui import GetForegroundWindow, ShowWindow
#import win32.lib.win32con as win32con

#the_program_to_hide = GetForegroundWindow()
#ShowWindow(the_program_to_hide , win32con.SW_HIDE)

# declare text_box
num_text = ""

def num_press(num, event=None): 
    '''
    appends the number pressed to the text box
    '''
    global num_text

    num_text += str(num) 

    # update the expression by using set method
    input_num.set(num_text)
    
def enter_press():
    ''' submits the answer '''
    # If the game has not yet started, start it
    print(ng.game_state)
    if ng.game_state == "Not Running":
        if "0118999" in num_text:
            ng.debug = True
            ng.start_game(int(num_text[7:]))
        else:
            ng.start_game()
        update_text_boxes()
    elif ng.game_state == "Awaiting Answer":
        ng.check_answer(num_text)
        update_text_boxes()
    elif ng.game_state == 'Waiting to generate new question':
        ng.next_question()
        update_text_boxes()
        
def update_text_boxes():
    global question_text
    global lives_text
    global score_text
    global level_text
    question_text.configure(state='normal')
    question_text.delete('1.0', 'end')
    question_text.insert(tk.END, ng.display_text)
    if ng.display_text.count('\n') > 11:
        question_text.configure(height=ng.display_text.count('\n'))
    else:
        question_text.configure(height=11)
    question_text.configure(state='disabled')
    lives_text.configure(state='normal')
    lives_text.delete('1.0', 'end')
    lives_text.insert(tk.END, ("Lives: " + str(ng.lives)))
    lives_text.configure(state='disabled')
    score_text.configure(state='normal')
    score_text.delete('1.0', 'end')
    score_text.insert(tk.END, ("Score: " + str(ng.game_points)))
    score_text.configure(state='disabled')
    
    answ_no_text.configure(state='normal')
    answ_no_text.delete('1.0', 'end')
    answ_no_text.insert(tk.END, ("Q#: " + str(ng.question_number)))
    answ_no_text.configure(state='disabled')
    
    min_text.configure(state='normal')
    min_text.delete('1.0', 'end')
    min_text.insert(tk.END, ("Min #: " + str(ng.current_question[3][0])))
    min_text.configure(state='disabled') 
    
    max_text.configure(state='normal')
    max_text.delete('1.0', 'end')
    max_text.insert(tk.END, ("Max #: " + str(ng.current_question[3][1])))
    max_text.configure(state='disabled')     
    
    level_text.configure(state='normal')
    level_text.delete('1.0', 'end')
    level_text.insert(tk.END, ("Level: " + str(ng.level)))
    level_text.configure(state='disabled')
    global input_num
    input_num.set(ng.input_text)
    global num_text
    num_text = ""    

# Function to clear the contents 
# of text entry box 
def clear(): 
    global num_text
    num_text = "" 
    input_num.set("") 

def bckspc():
    global num_text
    num_text = num_text[:-1]
    input_num.set(num_text)

def resize(gui):
    height = gui.winfo_height()
    width = gui.winfo_width()
    #print('height %s' % height)
    #print('width %s' % width)
    if height < 400 or width < 300:
        fontsize = 8
    elif height < 500 or width < 400:
        fontsize = 10
    elif height < 700 or width < 600:
        fontsize = 13
    elif width < 1000 or height < 900:
        fontsize = 15
    elif width < 1100 or height < 1100:
        fontsize = 17
    else:
        fontsize = 20
    gui.buttonFont['size'] = int(fontsize * 5/3)
    gui.label_font['size'] = fontsize
    gui.statsFont['size'] = int(fontsize * 7/6)

def animate_keypress(key):
    b = buttons[key]
    #Simulate pushing the button
    b.config(relief=tk.SUNKEN)

    #Let it pop back up after 200 milliseconds
    b.after(200, lambda: b.config(relief=tk.RAISED))    


# Driver code 
if __name__ == "__main__":
    # create a GUI window 
    gui = tk.Tk()
    
    
    gui.label_font = font.Font(family='Arial', weight="bold")   
    
    gui.bind('<Configure>', lambda x: resize(gui))

    #BIND KEY PRESSES
    gui.bind("<Return>", lambda x: enter_press())
    gui.bind("1", lambda x: num_press(1))
    gui.bind("2", lambda x: num_press(2)) 
    gui.bind("3", lambda x: num_press(3))
    gui.bind("4", lambda x: num_press(4))
    gui.bind("5", lambda x: num_press(5))
    gui.bind("6", lambda x: num_press(6))
    gui.bind("7", lambda x: num_press(7))
    gui.bind("8", lambda x: num_press(8))
    gui.bind("9", lambda x: num_press(9))
    gui.bind("0", lambda x: num_press(0))
    gui.bind("<KeyPress-Delete>", lambda x: clear())
    gui.bind(".", lambda x: clear())
    gui.bind("<BackSpace>", lambda x: bckspc())
    gui.bind("+", lambda x: bckspc())
    gui.bind("1", lambda x: animate_keypress(1), add="+")
    gui.bind("2", lambda x: animate_keypress(2), add="+")
    gui.bind("3", lambda x: animate_keypress(3), add="+")
    gui.bind("4", lambda x: animate_keypress(4), add="+")
    gui.bind("5", lambda x: animate_keypress(5), add="+")
    gui.bind("6", lambda x: animate_keypress(6), add="+")
    gui.bind("7", lambda x: animate_keypress(7), add="+")
    gui.bind("8", lambda x: animate_keypress(8), add="+")
    gui.bind("9", lambda x: animate_keypress(9), add="+")
    gui.bind("0", lambda x: animate_keypress(0), add="+")
    gui.bind("<Return>", lambda x: animate_keypress(10), add="+")
    gui.bind("<KeyPress-Delete>", lambda x: animate_keypress(11), add="+")
    gui.bind(".", lambda x: animate_keypress(11), add="+")
    gui.bind("<BackSpace>", lambda x: animate_keypress(11), add="+")
    gui.bind("+", lambda x: animate_keypress(11), add="+")



    # set the background colour of GUI window 
    gui.configure(background="#ffb2e3")
    stats_bg="#79dfee"
    button_bg="#79dfee"
    button_fg="#db098e"
    text_bg="#b6f6ff"
    text_fg="#b1257e"

    # set the title of GUI window 
    gui.title("Number Game") 

    # set the configuration of GUI window 
    #gui.geometry("385x444") 
    gui.geometry("450x525")

    # define font
    gui.buttonFont = font.Font(weight='bold', size=20)
    gui.statsFont = font.Font(weight="bold")

    # StringVar() is the variable class 
    # we create an instance of this class 
    input_num = tk.StringVar() 

    # create the text entry box for 
    # showing the expression .
    input_field = tk.Entry(gui, textvariable=input_num, fg=text_fg)
    input_field.configure({"readonlybackground": text_bg})
    input_field['font'] = gui.buttonFont
    input_field.grid(row=3, column=0, padx=0, pady=0, columnspan=3, sticky="ns") 
    input_num.set('')
    input_field.configure(state='readonly')
    
    # Generate Text box for question
    question_text = tk.Text(gui, height = 11, bg=text_bg, fg=text_fg)
    question_text['font'] = gui.label_font
    question_text.insert(tk.END, ng.display_text)
    question_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew") 
    question_text.configure(state='disabled')
    #Generate text box for lives
    lives_text = tk.Text(gui, width=11, height=1, bg=stats_bg, fg=button_fg)
    lives_text.insert(tk.END, ("Lives: " + str(ng.lives)))
    lives_text['font'] = gui.statsFont
    lives_text.grid(row=0, column=0, columnspan=1, sticky="ns", padx=5, pady=5)   
    lives_text.configure(state='disabled')
    # Text box for score
    score_text = tk.Text(gui, width=13, height=1, bg=stats_bg, fg=button_fg)
    score_text.insert(tk.END, ("Score: " + str(ng.game_points)))
    score_text['font'] = gui.statsFont
    score_text.grid(row=0, column=1, columnspan=1, sticky="ns", padx=5, pady=5)   
    score_text.configure(state='disabled')
    #text box for level
    level_text = tk.Text(gui, width=13, height=1, bg=stats_bg, fg=button_fg)
    level_text.insert(tk.END, ("Level: " + str(ng.level)))
    level_text.grid(row=0, column=2, columnspan=1, sticky="ns", padx=5, pady=5)   
    level_text['font'] = gui.statsFont
    level_text.configure(state='disabled')
    #text box for questions_answered
    answ_no_text = tk.Text(gui, width=11, height=1, bg=stats_bg, pady=0, fg=button_fg)
    answ_no_text.insert(tk.END, ("Q#: " + str(ng.question_number)))
    answ_no_text.grid(row=1, column=0, columnspan=1, sticky="n", padx=5, pady=5, ipady=3)   
    answ_no_text['font'] = gui.statsFont
    answ_no_text.configure(state='disabled')
    #text box for min number
    min_text = tk.Text(gui, width=13, height=1, fg="green", bg=stats_bg)
    min_text.insert(tk.END, ("Min #: 0"))
    min_text.grid(row=1, column=1, columnspan=1, sticky="n", padx=5, pady=5, ipady=3)   
    min_text['font'] = gui.statsFont
    min_text.configure(state='disabled')
    #text box for max number
    max_text = tk.Text(gui, width=13, height=1, fg="red", bg=stats_bg)
    max_text.insert(tk.END, ("Max #: 0"))
    max_text.grid(row=1, column=2, columnspan=1, sticky="n", padx=5, pady=5, ipady=3)   
    max_text['font'] = gui.statsFont
    max_text.configure(state='disabled')      
    # create a Buttons and place at a particular 
    # location inside the root window . 
    # when user press the button, the command or 
    # function affiliated to that button is executed .
    buttons = list(range(0, 15))
    buttons[1] = tk.Button(gui, text='1', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(1), height=1, width=7) 
    buttons[1]['font'] = gui.buttonFont
    buttons[1].grid(row=4, column=0, sticky="nsew", pady=(5,0), padx=(5,0)) 
    buttons[1]['font'] = gui.buttonFont
    buttons[2] = tk.Button(gui, text='2', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(2), height=1, width=7) 
    buttons[2].grid(row=4, column=1, sticky="nsew", pady=(5,0)) 
    buttons[2]['font'] = gui.buttonFont
    buttons[3] = tk.Button(gui, text='3', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(3), height=1, width=7) 
    buttons[3].grid(row=4, column=2, sticky="nsew", pady=(5,0), padx=(0,5))
    buttons[3]['font'] = gui.buttonFont
    buttons[3]['font'] = gui.buttonFont
    buttons[4] = tk.Button(gui, text='4', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(4), height=1, width=7) 
    buttons[4].grid(row=5, column=0, sticky="nsew", padx=(5,0)) 
    buttons[4]['font'] = gui.buttonFont
    buttons[5] = tk.Button(gui, text='5', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(5), height=1, width=7) 
    buttons[5].grid(row=5, column=1, sticky="nsew") 
    buttons[5]['font'] = gui.buttonFont
    buttons[6] = tk.Button(gui, text='6', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(6), height=1, width=7) 
    buttons[6].grid(row=5, column=2, sticky="nsew", padx=(0,5))
    buttons[6]['font'] = gui.buttonFont
    buttons[7] = tk.Button(gui, text='7', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(7), height=1, width=7) 
    buttons[7].grid(row=6, column=0, sticky="nsew", padx=(5,0)) 
    buttons[7]['font'] = gui.buttonFont
    buttons[8] = tk.Button(gui, text='8', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(8), height=1, width=7) 
    buttons[8].grid(row=6, column=1, sticky="nsew") 
    buttons[8]['font'] = gui.buttonFont
    buttons[9] = tk.Button(gui, text='9', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(9), height=1, width=7) 
    buttons[9].grid(row=6, column=2, sticky="nsew", padx=(0,5))
    buttons[9]['font'] = gui.buttonFont
    buttons[0] = tk.Button(gui, text='0', fg=button_fg, bg=button_bg, activebackground=button_bg,
                     command=lambda: num_press(0), height=1, width=7) 
    buttons[0].grid(row=7, column=0, sticky="nsew", padx=(5,0), pady=(0,5)) 
    buttons[0]['font'] = gui.buttonFont
    buttons[10]= tk.Button(gui, text='ENTER', fg=button_fg, bg=button_bg, activebackground=button_bg,
                   command=enter_press, height=1, width=7) 
    buttons[10].grid(row=7, column=2, sticky="nsew", padx=(0,5), pady=(0,5)) 
    buttons[10]['font'] = gui.buttonFont
    buttons[11] = tk.Button(gui, text='CLEAR', fg=button_fg, bg=button_bg, activebackground=button_bg,
                   command=clear, height=1, width=7)
    buttons[11].grid(row=7, column=1, sticky="nsew", pady=(0,5)) 
    buttons[11]['font'] = gui.buttonFont
    gui.rowconfigure(1, weight = 1)
    gui.rowconfigure(2, weight = 1)
    gui.rowconfigure(3, weight = 1)
    gui.rowconfigure(4, weight = 1)
    gui.rowconfigure(5, weight = 1)
    gui.rowconfigure(6, weight = 1)
    gui.rowconfigure(7, weight = 1)
    gui.columnconfigure(0, weight =1)
    gui.columnconfigure(1, weight=1)
    gui.columnconfigure(2, weight=1)
    # start the GUI 
    
    icondata= base64.b64decode(icon)
    ## The temp file is icon.ico
    tempFile= "0111icon.ico"
    iconfile= open(tempFile,"wb")
    ## Extract the icon
    iconfile.write(icondata)
    iconfile.close()
    gui.wm_iconbitmap(tempFile)
    ## Delete the tempfile
    os.remove(tempFile)
    
    #gui.iconbitmap('NRG4.ico')
    gui.mainloop()  