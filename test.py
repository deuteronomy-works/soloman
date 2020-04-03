from time import sleep
from soloman import Audio

aud = Audio()
aud.prepare('H:/GitHub/soloman/soloman/audio/data/music/f.mp3')
aud.delay_play(0.00000)
sleep(.1)

#aud.stop()
print(aud)

