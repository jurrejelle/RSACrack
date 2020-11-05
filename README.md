# RSACrack
(Side note: I have recently added the Dutch PDF of the Highschool Research Project that this was made for)

A tool to test how long it takes to crack RSA.

## Heads up!

This tool is built to aproximate the times based on test data you generate yourself. This is meant as a proof of concept, and in no way supposed to be entirely accurate, since one test data sample can change the time for the entire formula.


## Getting Started

With these instructions, you can get your own test data for your computer on how long it takes to crack RSA keys. That is, to factor the coprime `n` into the two primes `p` and `q`.

### Prerequisites

The only thing you need to run this, is python 2.7
It does not work with python 3!


### Installing

First, clone the git repository by doing

```
git clone https://github.com/jurrejelle/RSACrack.git
```

If you don't know what that is or how it works, you can also download a ZIP file containing all the files in the top right
Just unzip the files into a directory, and you should be good to go

## Running the tests

To start cracking, run crack.py by doing
```
python crack.py
```

This will crack the keys and save how long it takes to do it, and thus generate testdata

#### It's very important to leave this running for a while, else you won't have enough testdata to work with

It by default cracks 100 keys per amount of bits. To run the other programs efficiently, it is reccomended you leave it running until atleast 128 bits, preferably higher. Above the 130 bits, it will start cracking only 20 keys per amount of bits, because of time concerns. The amount of testcases can be changed in the crack.py file by editing the variables attempts_under_130 and attempts_above_130

### Checking specific bit-length keys

To get information about any specific bit-length key, you can run

```
python analyze_results.py
```
which will prompt you for a bit-length, which you can select from the list provided
Once you enter the bit-length and press enter, it will give the median, mean, shortest and longest times for that bit-length key


### Turning the data into something graphable

To turn the test data into something that data.html can view, you need to run
```
python generate_datafile.py
```
which will create a datafile.js inside the results directory, which is used by the data.html to graph the data


### Generating the aproximation of the formula

To generate an approximation of the formula for time over bits, you need to run
```
python aproximate_formula.py
```
Which will both print the formula it estimated, aswell as creating an estimated_results.js file in the results directory, which is used by data.html aswell

### Actually viewing the data

To view the test data, aproximated formula and aproximated data, you simply need to open ```data.html``` in a web browser

 
### Credits
Most of the code was written by me, but with one exception, which is why I wanna give a huge shoutout to [primo-ppcg](https://github.com/primo-ppcg) for writing this code for the Multiple Polynomial Quadratic Sieve in [this stack-exchange post](https://codegolf.stackexchange.com/questions/8629/fastest-semiprime-factorization). These are the files in the imports folder

# Contact 
If you have any questions or want to contact me, feel free to contact me on [twitter](https://twitter.com/twinjurre), [instagram](https://instagram.com/jurrejelle), [telegram](https://t.me/jurrejelle) or discord (jurrejelle#4936)
