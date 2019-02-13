with open("results/estimated_datafile.js") as f:
	lines = f.readlines()
	g = float(lines[-2].strip().split("=")[1])
	b = float(lines[-1].strip().split("=")[1])
def estimate_real(x):
    return b*(g**x)
def estimate_fastest(x):
    return (210*(x**2)+1060*x-1410)*(10**-9)
def estimate_slowest(x):
    return (2650*(x**3)+1060*x-1410)*(10**-9)
#Generate a datafile with the points of the estimated formula, and other additional data the data.html file needs
all_times_real = {}
all_times_slowest = {}
all_times_fastest = {}
highest = 2048
for x in range(4, highest+4, 4):
    all_times_real[x]=estimate_real(x)
    all_times_slowest[x]=estimate_slowest(x)
    all_times_fastest[x]=estimate_fastest(x)
with open("results/quantum_datafile.js","w") as f:
    f.write("estimated_extended_data=[{\n"+("".join(['"bits":'+str(x)+',\n"time":'+str(all_times_real[x])+"\n},{\n" for x in range(4, highest+4, 4)])[:-3])+"];")
    f.write("fastest_data=[{\n"+("".join(['"bits":'+str(x)+',\n"time":'+str(all_times_fastest[x])+"\n},{\n" for x in range(4, highest+4, 4)])[:-3])+"];")
    f.write("slowest_data=[{\n"+("".join(['"bits":'+str(x)+',\n"time":'+str(all_times_slowest[x])+"\n},{\n" for x in range(4, highest+4, 4)])[:-3])+"];")
