import RPi.GPIO as GPIO
from tkinter import *
from tkinter.filedialog import *
from functools import partial
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
    keyToSoundDict[key] = "N/A"

class App:
    global keyToSoundDict
	
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.keyToSoundStringVarDict = {}
        self.keyToBtnDict = {}
        self.keyToLblDict = {}
        x = 0 #horizontal pos on grid
        y = 0 #vertical pos on grid

        for key in keys:
            self.keyToBtnDict[key] = Button(frame, text="Btn " + key, command = partial(self.getDirectory, key))
            self.keyToBtnDict[key].grid(row = y, column = x)

            
            
            self.keyToLblDict[key] = Label(frame, textvariable = )
            self.keyToLblDict[key].grid(row = y, column = x+1)  
                  
            x += 2
            temp = y
            y += 1 if x%8==0 else 0
            x = 0 if temp!=y else x

    def getDirectory(self, key):
        dir = askopenfilename(title = "select a mp3 file", filetypes = [("mp3 files", "*.mp3")])
        keyToSoundDict[key] = dir if dir else 'N/A'
 

def loop():
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)  
    keypad.setDebounceTime(50)     
    while(True):
        key = keypad.getKey()   
        if(key != keypad.NULL):  
            print ("You Pressed Key : %c "%(key))
            
if __name__ == '__main__':     #Program start from here
    print ("Program is starting ... ")
    """try:
        loop()
    except KeyboardInterrupt:  #When 'Ctrl+C' is pressed, exit the program. 
        GPIO.cleanup()"""

    root = Tk()
    root.wm_title('Soundboard')
    app = App(root)
    root.mainloop()
