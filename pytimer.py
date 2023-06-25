import time

count = 0
print("The pomodoro timer has started, start working!")

if __name__ == "__main__":
    while True:
        time.sleep(1800)
        count += 1
        print("Good work!")
        print("Take a 10 minute break! You have completed " + str(count) + " pomodoros so far")
        
        time.sleep(600)
        print("Back to work!")
        print("Try doing another pomodoro...")
