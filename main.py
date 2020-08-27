import RPi.GPIO as GPIO
from tkinter import *
import Keypad


ROWS = 4    
COLS = 4 
keys =  [   '1','2','3','A',  
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]        #connect to the row pinouts of the keypad
colsPins = [19,15,13,11]        #connect to the column pinouts of the keypad

keyToSoundDict = {}

for key in keys:
    keyToSoundDict[key] = ""

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.keyToBtnDict = {}
        self.keyToLblDict = {}
        x = 0 #horizontal pos on grid
        y = 0 #vertical pos on grid
        for key in keys:
            self.keyToBtnDict[key] = Button(master, text="Btn " + key, command = self.getDirectory(key))
            self.keyToBtnDict[key].grid(row = x, column = y)
            
            self.keyToLblDict[key] = Label(frame, text=keyToSoundDict[key])
            self.keyToBtnDict[key].grid(row = x+1, column = y)  
                                   
            x += 1
            y += x%4==0 ? 1 : 0
            
    def getDirectory(key):
        dir = filedialog.askdirectory()
        keyToSoundDict[key] = dir
        self.keyToLblDict[key]["text"] = dir
      

def loop():
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)  
    keypad.setDebounceTime(50)     
    while(True):
        key = keypad.getKey()   
        if(key != keypad.NULL):  
            print ("You Pressed Key : %c "%(key))
            
if __name__ == '__main__':     #Program start from here
    print ("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:  #When 'Ctrl+C' is pressed, exit the program. 
        GPIO.cleanup()
