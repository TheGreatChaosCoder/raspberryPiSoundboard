import vlc

vlcInstance = vlc.Instance()
player = vlcInstance.media_player_new()

class Soundboard:
    global vlcInstance
    global player
    
    def __init__(self, soundFolderDir):
        self.soundFolderDir = soundFolderDir

    def stopPlayer(self):
        player.stop()
        #player.set_media(vlcInstance.media_new_path(None)) #removes old media

    def playSound(self, soundName):
        soundFileDir = self.soundFolderDir + "/" + soundName
        print(player.get_media())
        player.set_media(vlcInstance.media_new_path(soundFileDir))
        player.play()
                
        
