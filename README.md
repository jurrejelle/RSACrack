# RSACrack

A tool to test how long it takes to crack RSA.

## Getting Started

With these instructions, you can get your own test data for your computer on how long it takes to crack RSA keys. That is, to factor the coprime n into the two primes p and q.

### Prerequisites

The only thing you need to run this, is python 2.7
It does not work with python 3!


### Installing

A step by step series of examples that tell you how to get a development env running

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
aproximate_formula.py
```
Which will both print the formula it estimated, aswell as creating an estimated_results.js file in the results directory, which is used by data.html aswell

### Actually viewing the data

To view the test data, aproximated formula and aproximated data, you simply need to open ```data.html``` in a web browser

