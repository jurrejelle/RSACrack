#!/usr/bin/env python2
import random
from math import sqrt
from itertools import count, islice
from imports.calc import mpqs, isPrime
import time
import multiprocessing
import os

#This function generates a random x bit odd number
def genrandom(bits):
        y = "".join([str(random.randrange(0,2)) for x in range(0, bits-3)])
        return int("11"+y+"1",2)

#Making the results folder if it doesn't exist yet
if("results" not in os.listdir(".")):
                os.makedirs("results")
times = []
timeout_before = 20#Time to time out in seconds
timeout_after  = 1200
attempts_under_130 = 40 #Amount of testcases which it averages for the result
attempts_above_130 = 20  #Amount of testcases for above 150 bits
for r in range(64, 256, 4):
        timeouts = 0
        #If the file doesn't exist yet, make it
        if(str(r)+".txt" not in os.listdir("./results")):
                with open("results/"+str(r)+".txt", "w") as f:
                        pass
        #Check if the current file already has the required amount of testcases
        with open("results/"+str(r)+".txt") as f:
                current_lines = len(f.readlines())
                if(r<130 and len(f.readlines())>attempts_under_130):
                        continue
                if(r>130 and len(f.readlines())>attempts_above_130):
                        continue
        working = 0
        #Set the timeout for the desired amount of bits
        if(r>130):
                nr = attempts_above_130-current_lines+1
                timeout = timeout_after
        else:
                nr=attempts_under_130-current_lines+1
                timeout = timeout_before
                
        #Do the amount of required testcases
        for count in range(1, nr):
                working = 1
                p,q=30,30
                #Generate the two primes p and q
                while not(isPrime(p)):
                        p = genrandom(int(r/2))
                while not(isPrime(q) and p!=q):
                        q = genrandom(int(r/2))
                print("attempt: %s/%s, bits: %s, n: %s" % (count, nr-1, str(len(str(bin(q*p)))-2), str(p*q)))
                time1 = time.time()
                #Actually perform the mpqs
                factor1 = mpqs(p*q, time1, timeout)
                time2 = time.time()
                print time2-time1,
                times.append(time2-time1)
                print("seconds passed")
                #Check for timeout
                if(factor1=="timeout"):
                        print "timeout"
                        timeouts+=1
                        if(timeouts>20):
                                break;
                        continue;
                #Write the output to stdout and the results file
                print("Primes: "+str(factor1)+str(", ")+str(p*q/factor1)+"\n")
                with open("results/"+str(r)+".txt", "a") as f:
                        f.write(str(time2-time1) +","+str(p*q)+","+str(factor1)+"\n")
        if working:
                print("%s bits: %s seconds" % (str(r), str(sum(times)/len(times))))
        if(timeouts>20):
                break;
