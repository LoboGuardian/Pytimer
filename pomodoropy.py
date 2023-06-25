import time
import os

def convert(t):
    return t * 60

def countdowm(t, label):
    # 60
    while t:
        mins, secs = divmod(t, 60)
        # t // 60
        # t % 60
        print(f"{label}: {min:02d}:{secs:02d}", end="\r")
        #print('{:02d}:{:02d} '.format(min, secs))
        time.sleep(1)
#        print("%s:%0")
        t -= 1

def pomodoro(work, rest):
    # convert min to sec
    w = convert(work)
    r = convert(rest)
    countdowm(w, "Work")
    os.system("clear||cls")
    countdowm(r, "Rest")
    os.system("clear||cls")

work = int(input("Enter work time (min): "))
rest = int(input("Enter rest time (min): "))

pomodoro(work, rest)