import tkinter as tk
import time
import os
import pygame

bg_color = "#333333"
fg_color = "#FFFFFF"

clock='clock_01.ogg'
relaxing = 'Meditate.opus'
audio = 'clock_02.ogg'

pygame.init()
sound = pygame.mixer.Sound(clock)
cheers = pygame.mixer.Sound(audio)
relax = pygame.mixer.Sound(relaxing)

def clear():
    os.system("clear||cls")

def convert(t):
    return t * 60

def countdown(t, label):
    global running
    running = True
    while t and running:
        mins, secs = divmod(t, 60)
        timer_label.config(text=f"{label}: {mins:02d}:{secs:02d}")
        root.update()
        time.sleep(1)
        t -= 1
        if label == "Work":
            sound.play()
        elif label == "Rest":
            relax.play()
        
def pause_timer():
    # Detiene el temporizador
    global running
    running = False

def pomodoro():
    # work_time = int(work_entry.get())
    # rest_time = int(rest_entry.get()) 
    work_time = int(45)
    rest_time = int(15)
    w = convert(work_time)
    r = convert(rest_time)
    work_label.pack_forget()
    work_entry.pack_forget()
    rest_label.pack_forget()
    rest_entry.pack_forget()
    start_button.pack_forget()
    pause_button.pack()
    clear()
    countdown(w, "Work")
    clear()
    cheers.play()
    countdown(r, "Rest")
    clear()
    #work_label.pack()
    #work_entry.pack()
    #rest_label.pack()
    #rest_entry.pack()
    start_button.pack()
    pause_button.pack_forget()

root = tk.Tk()
root.title("Pomodoro Timer")
root.resizable(False, False)
#root.geometry("100x200")
root.configure(padx=15, pady=15, bg=bg_color) # Agrega un margen de 15px en los bordes

work_label = tk.Label(root, text="Work time (min):", fg=fg_color)
#work_label.pack()
work_entry = tk.Entry(root)
#work_entry.pack()

rest_label = tk.Label(root, text="Rest time (min):", fg=fg_color)
# rest_label.pack()
rest_entry = tk.Entry(root)
# rest_entry.pack()

start_button = tk.Button(root, text="Start", command=pomodoro,)
time.sleep(3)
start_button.pack()

timer_label = tk.Label(root, text="00:00", font=("Courier", 30),)
timer_label.pack()

pause_button = tk.Button(root, text="Pause", command=pause_timer,)
time.sleep(1)
pause_button.pack()

root.mainloop()