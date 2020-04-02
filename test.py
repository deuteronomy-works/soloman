from soloman import Audio

aud = Audio()
aud.prepare('H:/GitHub/soloman/soloman/audio/data/music/f.mp3')
print('her')
aud.delay_play(0.00000)

if aud.playing:
    print('hee')
