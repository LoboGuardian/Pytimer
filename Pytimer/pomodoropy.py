import time
import os

work=45
rest=15

def convert(t):
    return t * 60

def countdown(t, label):
    # 60
    while t:
        mins, secs = divmod(t, 60)
        # t // 60
        # t % 60
        print(f"{label}: {mins:02d}:{secs:02d}", end="\r")
        time.sleep(1)
        t -= 1

def pomodoro(work, rest):
    # convert min to sec
    w = convert(work)
    r = convert(rest)
    os.system("clear||cls")
    countdown(w, "Work")
    os.system("clear||cls")
    countdown(r, "Rest")
    os.system("clear||cls")

#work = int(input("Enter work time (min): "))
#rest = int(input("Enter rest time (min): "))

pomodoro(work, rest)