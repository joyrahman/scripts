import urllib2
mp3file = urllib2.urlopen("http://www.example.com/songs/mp3.mp3")
output = open('test.mp3','wb')
output.write(mp3file.read())
output.close()


