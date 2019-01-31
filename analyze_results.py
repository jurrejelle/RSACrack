#!/usr/bin/env python2
import os
bits_file = ""
if(not(bits_file)):
    if("results" in os.listdir(".")):
        print "\n".join(os.listdir("results"))
        bits_file = raw_input("Which file do you want to open? ")
folder = "results"
if(".txt" not in bits_file):
    bits_file+=".txt"
print "\n\nAnalyzing %s" % folder+"/"+bits_file

times = []
with open(folder+"/"+bits_file) as f:
    for x in [y[:-1] for y in f.readlines()]:
        times.append(x.split(","))
actual_times = [float(x[0]) for x in times]
sort = sorted(actual_times)
print "Number of datapoints: %s" % len(times)
print "Mean: %s" % (sum(actual_times)/float(len(times)))
if(len(times)%2==1):
    median = sort[len(sort)/2-1]
if(len(times)%2==0):
    median = sort[int(len(sort))/2]
    median = (median+sort[int(len(sort))/2-1])/2
print "Median: %s" % median
print "Longest time: %s" % str(max(actual_times))
print "Shortest time: %s" % str(min(actual_times))
while 1:
    pass
