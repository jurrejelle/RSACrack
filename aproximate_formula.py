from __future__ import division
import os
import math

highest = max([int(x.split(".")[0]) for x in os.listdir("results") if ".txt" in x])
lowest = highest-40
#Getmedian calculates the median of the times for a certain z-bit key
def getmedian(z):
    times = []
    if(str(z)+".txt" not in os.listdir("./results")):
        return "doesn't exist"
    bits_file = str(z)+".txt"
    with open("results/"+bits_file) as f:
        for x in [y[:-1] for y in f.readlines()]:
            times.append(x.split(","))
    actual_times = [float(x[0]) for x in times]
    sort = sorted(actual_times)
    if(len(times)%2==1):
        nr = int(math.floor(len(sort)/2)-1)
        median = sort[nr]
    if(len(times)%2==0):
        nr = int(math.floor(len(sort)/2))
        median = sort[nr]
        median = (median+sort[nr-1])/2
    return median

lowestmed = getmedian(lowest)
highestmed = getmedian(highest)
dataset = {lowest:lowestmed,
           highest:highestmed}

#Calculate g by taking the (x2-x1)th power sqrt of y2/y1
g=(dataset[dataset.keys()[1]]/dataset[dataset.keys()[0]])**(1.0/(dataset.keys()[1]-dataset.keys()[0]))
#Calculate b by rewriting the formula y=b*g**x to b=y/(g**x) and substituting one of the datapoints
b=dataset[dataset.keys()[1]]/(g**dataset.keys()[1])

def estimate(x):
    #y=b*g**x
    return b*(g**x)

#Generate a datafile with the points of the estimated formula, and other additional data the data.html file needs
all_times = {}
for x in range(0, highest+4, 4):
    all_times[x]=estimate(x)
with open("results/estimated_datafile.js","w") as f:
    f.write("estimated_imported_data=[{\n"+("".join(['"bits":'+str(x)+',\n"time":'+str(all_times[x])+"\n},{\n" for x in range(32, highest+4, 4)])[:-3])+"];")
    f.write("formula='t = %s*%s**b'\n"%(b,g))
    f.write("g=%s\n"%g)
    f.write("b=%s\n"%b)
print "t = %s*%s**b" % (b,g)
