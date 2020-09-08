import RPi.GPIO as GPIO
from tkinter import *
from tkinter.filedialog import *
from functools import partial
import os
import threading
import Keypad
import vlcSoundboard

ROWS = 4    
COLS = 4 
keys =  [   '1','2','3','A',  
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]        #connect to the row pinouts of the keypad
colsPins = [19,15,13,11]        #connect to the column pinouts of the keypad
stopButton = 'A' #the letter that will act as a 'stop player' button

soundFolder = "/sounds"
soundFolderDir = "raspberryPiSoundboard/" + soundFolder
soundboard = vlcSoundboard.Soundboard(soundFolder.replace("/", '')) #vlc doesnt like the slah at the front

#declaring dict that will contain the directories to the sound files when the buttons are pressed
keyToSoundDict = {}

for key in keys:
    if (key is not 'A'):
        keyToSoundDict[key] = "N/A"
    else:
        keyToSoundDict[key] = "Stop"

root = Tk()

def loop():
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)  
    keypad.setDebounceTime(50)     
    key = keypad.getKey()   
    if (key != keypad.NULL):  
        print ("You Pressed Key : %c "%(key))
        sound = keyToSoundDict[key]
        
        if (key != stopButton and sound != "N/A"):
            soundboard.playSound(sound)
        elif(key == stopButton):
            soundboard.stopPlayer()
    root.after(10, loop) #loops the function onto itself, does not cause a infinite recursion error

def printThreads():
    for thread in threading.enumerate():
        print(thread.name + "\n")
	
def inSoundFolder(directory):
	return os.getcwd()+soundFolder in directory
	
def getFileName(directory):
	file = directory
	if (inSoundFolder(file)):
            soundFolderAbsDir = os.getcwd() + soundFolder
            file = file.replace(soundFolderAbsDir + "/", '')
	return file

class App:
    global keyToSoundDict
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
            if (key is not stopButton):
		
                self.keyToBtnDict[key] = Button(frame, text="Btn " + key, command = partial(self.getDirectory, key))
                self.keyToBtnDict[key].grid(row = y, column = x)

                self.keyToSoundStringVarDict[key] = StringVar()
                self.keyToSoundStringVarDict[key].set(keyToSoundDict[key])

                self.keyToLblDict[key] = Label(frame, textvariable = self.keyToSoundStringVarDict[key])
                self.keyToLblDict[key].grid(row = y, column = x+1)
            else:
                self.keyToLblDict[key] = [None] * 2
                self.keyToLblDict[key][0] = Label(frame, text = "Btn " + key)
                self.keyToLblDict[key][0].grid(row = y, column = x)
                self.keyToLblDict[key][1] = Label(frame, text = keyToSoundDict[key])
                self.keyToLblDict[key][1].grid(row = y, column = x+1)
                  
            x += 2
            temp = y
            y += 1 if x%8==0 else 0
            x = 0 if temp!=y else x

    def getDirectory(self, key):
        directory = askopenfilename(title = "select a mp3 file", filetypes = [("mp3 files", "*.mp3")])
        if (directory and inSoundFolder(directory)):
        	keyToSoundDict[key] = getFileName(directory)
        	self.keyToSoundStringVarDict[key].set(keyToSoundDict[key])
        elif inSoundFolder(directory):
                messagebox.showwarning(title = "Invaild Response", message = "File has to be in the 'sounds' folder")
                self.getDirectory(key)
        else:
                keyToSoundDict[key] = 'N/A'
                self.keyToSoundStringVarDict[key].set(keyToSoundDict[key])

    def report_callback_exception(self, exc, val, tb): #overrides tkinter's callback exception function
        tkMessageBox.showerror("Exception", message=str(val))
	
    def onClosing(self):
        root.destroy()
        GPIO.cleanup()
      
if __name__ == '__main__':     #Program start from here
    print ("Program is starting ... ")
    
    root.wm_title('Soundboard')
    app = App(root)

    root.wm_protocol("WM_DELETE_WINDOW", app.onClosing)
    root.after(10, loop)
    root.mainloop()
