# import everything from tkinter module 
import tkinter as tk
import tkinter.font as font
import numgame as ng

from win32gui import GetForegroundWindow, ShowWindow
import win32.lib.win32con as win32con

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
        if num_text == "0118999":
            ng.start_game(5)
        else:
            ng.start_game(1)
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
    question_text.configure(state='disabled')
    lives_text.configure(state='normal')
    lives_text.delete('1.0', 'end')
    lives_text.insert(tk.END, ("Lives: " + str(ng.lives)))
    lives_text.configure(state='disabled')
    score_text.configure(state='normal')
    score_text.delete('1.0', 'end')
    score_text.insert(tk.END, ("Score: " + str(ng.game_points)))
    score_text.configure(state='disabled')
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


# Driver code 
if __name__ == "__main__": 
    # create a GUI window 
    gui = tk.Tk() 

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

    # set the background colour of GUI window 
    gui.configure(background="light gray") 

    # set the title of GUI window 
    gui.title("Number Game") 

    # set the configuration of GUI window 
    gui.geometry("385x444") 

    # define font
    buttonFont = font.Font(weight='bold', size=20)    

    # StringVar() is the variable class 
    # we create an instance of this class 
    input_num = tk.StringVar() 

    # create the text entry box for 
    # showing the expression .
    input_field = tk.Entry(gui, textvariable=input_num)
    input_field['font'] = buttonFont
    input_field.grid(row=3, column=0, padx=0, pady=0, columnspan=3, ipadx=0) 
    input_num.set('')
    input_field.configure(state='readonly')
    
    # Generate Text box for question
    question_text = tk.Text(gui, width=40, height=10)
    question_text.insert(tk.END, ng.display_text)
    question_text.grid(row=2, column=0, columnspan=3) 
    question_text.configure(state='disabled')
    #Generate text box for lives
    lives_text = tk.Text(gui, width=11, height=0)
    lives_text.insert(tk.END, ("Lives: " + str(ng.lives)))
    lives_text.grid(row=1, column=0, columnspan=1)   
    lives_text.configure(state='disabled')
    # Text box for score
    score_text = tk.Text(gui, width=11, height=0)
    score_text.insert(tk.END, ("Score: " + str(ng.game_points)))
    score_text.grid(row=1, column=1, columnspan=1)
    score_text.configure(state='disabled')
    #text box for level
    level_text = tk.Text(gui, width=11, height=0)
    level_text.insert(tk.END, ("Level: " + str(ng.level)))
    level_text.grid(row=1, column=2, columnspan=1)
    level_text.configure(state='disabled')
    # create a Buttons and place at a particular 
    # location inside the root window . 
    # when user press the button, the command or 
    # function affiliated to that button is executed . 
    button1 = tk.Button(gui, text='1', fg='white', bg='black', 
                     command=lambda: num_press(1), height=1, width=7) 
    button1['font'] = buttonFont
    button1.grid(row=4, column=0, padx=0, pady=0) 

    button2 = tk.Button(gui, text=' 2 ', fg='white', bg='black', 
                     command=lambda: num_press(2), height=1, width=7) 
    button2.grid(row=4, column=1) 
    button2['font'] = buttonFont
    button3 = tk.Button(gui, text=' 3 ', fg='white', bg='black', 
                     command=lambda: num_press(3), height=1, width=7) 
    button3.grid(row=4, column=2) 
    button3['font'] = buttonFont
    button4 = tk.Button(gui, text=' 4 ', fg='white', bg='black', 
                     command=lambda: num_press(4), height=1, width=7) 
    button4.grid(row=5, column=0) 
    button4['font'] = buttonFont
    button5 = tk.Button(gui, text=' 5 ', fg='white', bg='black', 
                     command=lambda: num_press(5), height=1, width=7) 
    button5.grid(row=5, column=1) 
    button5['font'] = buttonFont
    button6 = tk.Button(gui, text=' 6 ', fg='white', bg='black', 
                     command=lambda: num_press(6), height=1, width=7) 
    button6.grid(row=5, column=2) 
    button6['font'] = buttonFont
    button7 = tk.Button(gui, text=' 7 ', fg='white', bg='black', 
                     command=lambda: num_press(7), height=1, width=7) 
    button7.grid(row=6, column=0) 
    button7['font'] = buttonFont
    button8 = tk.Button(gui, text=' 8 ', fg='white', bg='black', 
                     command=lambda: num_press(8), height=1, width=7) 
    button8.grid(row=6, column=1) 
    button8['font'] = buttonFont
    button9 = tk.Button(gui, text=' 9 ', fg='white', bg='black', 
                     command=lambda: num_press(9), height=1, width=7) 
    button9.grid(row=6, column=2) 
    button9['font'] = buttonFont
    button0 = tk.Button(gui, text=' 0 ', fg='white', bg='black', 
                     command=lambda: num_press(0), height=1, width=7) 
    button0.grid(row=7, column=0) 
    button0['font'] = buttonFont
    enter= tk.Button(gui, text=' ENTER ', fg='white', bg='black', 
                   command=enter_press, height=1, width=7) 
    enter.grid(row=7, column=2) 
    enter['font'] = buttonFont
    clear_button = tk.Button(gui, text='CLEAR', fg='white', bg='black', 
                   command=clear, height=1, width=7)
    clear_button.grid(row=7, column='1') 
    clear_button['font'] = buttonFont
    # start the GUI 
    gui.mainloop()  