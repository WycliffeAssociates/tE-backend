import gzip, zlib
from struct import *
import struct
import os
import json
from functools import partial
import sys

f = open('/Users/lcheng/Desktop/en-x-demo2_ulb_b42_mrk_c07_v01_t05.wav', 'r+')

#Go to header 40-43 and add to bytearray and then unpack to get how long the audio segment is
lst = []
f.seek(40,0)
for _ in range(4):
    lst.append(f.read(1))
values = bytearray(lst)
g = struct.unpack('I', values)
f.seek(g[0], 0)
position = f.tell()

#how many bytes are there total
f.seek(0, 2)
endval = f.tell()

#position of where cuechunkid is
pos_cue = 0
#number of times to loop
numleft = (endval - (position + 44)) / 4
aiya = f.seek((position + 44), 0)
for _ in range(numleft):
    aiya = f.read(4)
    if aiya == "cue ":
        pos_cue = f.tell()
        break
#find out how long the cuechunk is and then add 8 for the chunkid
lst1 = []
for _ in range(4):
    lst1.append(f.read(1))
lst1 = bytearray(lst1)
h = struct.unpack('I', lst1)
length_cue = h[0]

#Find the labl by looking for LIST
f.seek((position + 44), 0)
for _ in range(numleft):
    aiya = f.read(4)
    if aiya == "LIST":
        fmore = f.tell()
        aiya = f.read(4)
        lbllength = f.tell()
        aiya = f.read(4)
        if aiya == "adtl":
            pos_lbl = fmore
            break
f.seek(fmore,0)
lst2 = []
#Obtain length of data for labl
for _ in range(4):
    lst2.append(f.read(1))
length_labl = bytearray(lst2)
lblln = struct.unpack('I', length_labl)
lbl = lblln[0]

#hard coded metadata sample

data = {}
data['anthology'] = 'nt'
data['lang'] = 'en-x-demo2'
data['version'] = 'ulb'
data['slug'] = 'mrk'
data['book_number'] = '42'
data['mode'] = 'chunk'
data['chapter'] = '7'
data['startv'] = '1'
data['endv'] = '1'
data['markers'] = {'1':0}
json_data = json.dumps(data)
padding = (len(json_data)) % 4
if padding is not 0:
    padding = 4 - padding
    for _ in range(padding):
        json_data = json_data + " "
#json_data = json.dumps({"anthology":"nt","language":"en-x-demo2","version":"ulb","slug":"mrk","book_number":"42","mode":"chunk","chapter":"7","startv":"1","endv":"1","markers":{"1":0}})

#Find and pack metadata length + metadata chunk length
numChar = '<' + str(len(json_data)) + 's'
s = struct.Struct(numChar)
packed_data = s.pack(json_data)
bytesused = s.size
listnum = bytesused + 20
bused = struct.pack('I', bytesused)
lnum = struct.pack('I', listnum)

for _ in range(numleft):
    aiya = f.read(4)
    if aiya == "LIST":
        flocaton = f.tell()
        aiya = f.read(4)
        metadatatotal = f.tell()
        aiya = f.read(4)
        if aiya == "INFO":
            break

#write into new file
byte_to_audio = position + 44
byte_of_cuetot = length_cue + 8
f.seek(0,0)
#new length of entire file
lengthall = byte_to_audio + byte_of_cuetot + (lbl+8) + 4 + 4 + 8 + 4 + bytesused
totallength = struct.pack('I',lengthall)
with open('final.wav', 'w+') as outFile:
    outFile.write(f.read(4))
    outFile.write(totallength)
    f.seek(8,0)
    outFile.write(f.read(byte_to_audio - 8))
    f.seek(pos_cue - 4,0)
    outFile.write(f.read(byte_of_cuetot))
    f.seek(fmore - 4, 0)
    outFile.write(f.read(lbl + 8))
    f.seek(flocaton - 4, 0)
    outFile.write(f.read(4))
    outFile.write(lnum)
    f.seek(flocaton + 4, 0)
    outFile.write(f.read(8))
    outFile.write(bused)
    outFile.write(packed_data)
