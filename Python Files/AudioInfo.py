# import wave, contextlib
from tinytag import TinyTag


# assign the file to the audio source - replace for your own file or use in large program
# later for the file that gets sent via API
audio = 'C:/Users/wyatt/Downloads/Chapter.wav'


file = TinyTag.get(audio)
print (float(file.filesize) / 1000000), "MB"
print ""
print file.artist
print ""
print 'It is %f seconds long.' % file.duration
print ""

# another way to read the file - and get it's info

# with contextlib.closing(wave.open(audio, 'r')) as f:
#     #get the number of frames in the file
#     frames = f.getnframes()
#     #get the frame rate
#     rate = f.getframerate()
#     #calculate duration
#     duration = frames / float(rate)
#     #seconds of length
#     print duration,'Seconds long'
#
#     #calculate minutes
#     minutes = duration / 60
#     print float(minutes), "Minutes long"
#     print ""
#     print f.tell()
#     f.close()


# Un-comment below if we want to actually know the value for each bit in the stream of the WAV file

# wavFile = wave.open(audio)
# length = wavFile.getnframes()

# for i in range(0, length):
#     waveData = wavFile.readframes(1)
#     data = struct.unpack("<h", waveData)
    # print int(data[0])
