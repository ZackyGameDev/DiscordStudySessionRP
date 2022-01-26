from datetime import timedelta
from os import system as cmd
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "true"
from pygame import mixer
import threading
import sys
import time


def suffixed_time_to_int(string_representation_of_time: str) -> int:
    """
    This function takes something like `"2m 6h 1s"` and returns back the time duration in seconds (int)
    """
    time = string_representation_of_time.split()
    for i in range(len(time)):
        if time[i].endswith("s"):
            time[i] = int(time[i][:-1])
        elif time[i].endswith("m"):
            time[i] = int(time[i][:-1]) * 60
        elif time[i].endswith("h"):
            time[i] = int(time[i][:-1]) * 60 * 60
        elif time[i].endswith("d"):
            time[i] = int(time[i][:-1]) * 60 * 60 * 24
        else:
            raise ValueError("Proper duration not passed")

    return sum(time)


# Timer
def timer(end_timestamp):
    while True:
        time_left = str(timedelta(seconds=end_timestamp-int(time.time())))
        print("\rSession Ending In: ", time_left, end="")
        time.sleep(1)
        sys.stdout.flush()
        if time_left == "0:00:00" or time_left == "00:00:00":
            break

    print("\n\n-------------------------------\nThe Study Session has ended, please \nClose his window to shut down the \nDiscord Activity\n-------------------------------")
    
    # Playing the Notification Sound
    mixer.init()
    mixer.music.load('notification.ogg')
    while True:
        mixer.music.play()
        time.sleep(3)
    

# Introduction
print(
'''
-----------------------------------------------------------------
   STUDY SESSION TIMER AND DISCORD ACTIVITY DISPLAYER
                 Developed by Zacky
             (utilizes Pizzabelly/EasyRP)
-----------------------------------------------------------------
'''
)

# Getting the status report
study_duration: int = suffixed_time_to_int(input("How long will this study session last?\n(for e.g. 2h 6m 1s)\nOnce the session is over, a notification sound will play\n> "))
status: str = input("\nWhat is your current status?\n(for e.g. Studied 2 hours so far, or, Trying to focus)\n> ")
start_timestamp: int = int(time.time())
end_timestamp: int = start_timestamp + study_duration

EasyRPConfig: str = '''
[Identifiers]
ClientID=893044045541179392

[State]
State={status}
Details={study_duration_hours} Hour Study Session
StartTimestamp={start_timestamp}
EndTimestamp={end_timestamp}

[Images]
LargeImage=studybagbig
LargeImageTooltip=Focusing
SmallImage=
SmallImageTooltip=
'''

f = open("config.ini", "w+")
f.write(EasyRPConfig.format(
    start_timestamp=start_timestamp, end_timestamp=end_timestamp, status=status, study_duration_hours=round(study_duration/3600, 1)))
f.close()

t1 = threading.Thread(target=cmd, args=("\"easyrp.exe\"", ))
t2 = threading.Thread(target=timer, args=(end_timestamp, ))
print("\n-------------------------------\nStarting the rish presence activity program now...")
t1.start()
time.sleep(3)
print("\n-------------------------------")
t2.start()
