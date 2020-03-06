##instructions
#open cmd prompt
#mkvirtualenv keep-pc-alive -p=path-to-python3-python.exe-file
#pip install pyautogui
#go to where file will be kept at ex: cd C:\Users\me\randomScripts
#setprojectdir .
### file simulates keyboard movement so that the freaking vpn wont disconnect
#https://automatetheboringstuff.com/chapter18/
import pyautogui
import random
# This disables failsafe so if mouse randomly moves to upper left corner, the script doesnt quit. \
# You need to press ctrl+C for it to stop.
pyautogui.FAILSAFE = False
print('Press Ctrl+C to quit.')
try:
    while True:
        x = random.randint(1,3) 
        print("pause is: ", x)
        y= random.randint(300,900) 
        pyautogui.PAUSE = x #waits x seconds after every function call
        pyautogui.moveRel(y, 0, duration=0.25)
        pyautogui.moveRel(0, y, duration=0.25)
        pyautogui.moveRel(-(y), 0, duration=0.25)
        pyautogui.moveRel(0, -(y), duration=0.25)
except KeyboardInterrupt:
    print('\nDone.')