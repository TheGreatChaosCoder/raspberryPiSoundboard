import RPi.GPIO as GPIO
from tkinter import *
from tkinter.filedialog import *
from functools import partial
import threading
import Keypad


ROWS = 4    
COLS = 4 
keys =  [   '1','2','3','A',  
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]        #connect to the row pinouts of the keypad
colsPins = [19,15,13,11]        #connect to the column pinouts of the keypad

root = Tk()
appClosed = False

def loop():
    global appClosed
    
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)  
    keypad.setDebounceTime(50)     
    while(not appClosed):
        key = keypad.getKey()   
        if(key != keypad.NULL):  
            print ("You Pressed Key : %c "%(key))

def printThreads():
    for thread in threading.enumerate():
        print(thread.name + "\n")

keypadThread = threading.Thread(name = "matrix keypad", target=loop)

keyToSoundDict = {}

for key in keys:
    keyToSoundDict[key] = "N/A"

class App:
    global keyToSoundDict
    global keypadThread
    global appClosed
	
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

            self.keyToSoundStringVarDict[key] = StringVar()
            self.keyToSoundStringVarDict[key].set(keyToSoundDict[key])

            self.keyToLblDict[key] = Label(frame, textvariable = self.keyToSoundStringVarDict[key])
            self.keyToLblDict[key].grid(row = y, column = x+1)  
                  
            x += 2
            temp = y
            y += 1 if x%8==0 else 0
            x = 0 if temp!=y else x

    def getDirectory(self, key):
        directory = askopenfilename(title = "select a mp3 file", filetypes = [("mp3 files", "*.mp3")])
        keyToSoundDict[key] = directory if directory else 'N/A'
        self.keyToSoundStringVarDict[key].set(keyToSoundDict[key])

    def report_callback_exception(self, exc, val, tb): #overrides tkinter's callback exception function
        tkMessageBox.showerror("Exception", message=str(val))
	
    def onClosing(self):
        print("i am also here")
        appClosed = True
        root.destroy()
        keypadThread.join() #joins thread to main thread
        printThreads()
        GPIO.cleanup()
        print("i am here")
            
if __name__ == '__main__':     #Program start from here
    print ("Program is starting ... ")
    
    root.wm_title('Soundboard')
    app = App(root)

    root.wm_protocol("WM_DELETE_WINDOW", app.onClosing)

    keypadThread.start()
    root.mainloop()

    print("stopping app, closing threads")
    #keypadThread.join()
    GPIO.cleanup()

