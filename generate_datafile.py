#!/usr/bin/env python2
import os
folder = "results/"
all_times = {}
times_list = []
#Generate all the medians
for z in range(64, 256, 4):
    times = []
    if(str(z)+".txt" not in os.listdir("./results")):
        break
    bits_file = str(z)+".txt"
    with open(folder+"/"+bits_file) as f:
        for x in [y[:-1] for y in f.readlines()]:
            times.append(x.split(","))
    actual_times = [float(x[0]) for x in times]
    sort = sorted(actual_times)
    if(len(times)%2==1):
        median = sort[len(sort)/2-1]
    if(len(times)%2==0):
        median = sort[int(len(sort))/2]
        median = (median+sort[int(len(sort))/2-1])/2
    all_times[z]=median
    times_list.append(z)
    print "Done %s bits" % z
#Write the medians and amount of bits to the datafile for every bit 64+4n, in a format that javascript can read
with open("results/datafile.js","w") as f:
    f.write("imported_data=[{\n"+("".join(['"bits":'+str(x)+',\n"time":'+str(all_times[x])+"\n},{\n" for x in times_list])[:-3])+"];")
print "Written and done!"
