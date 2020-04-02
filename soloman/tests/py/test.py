from ..soloman import Audio

print('yep')
aud = Audio()
aud.prepare('H:/GitHub/soloman/soloman/audio/data/music/f.mp3')
print('hy')
aud.delay_play(0.00000)

if aud.playing:
    print('yep')
