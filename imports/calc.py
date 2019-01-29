from my_math import *
from math import log
from time import clock
from argparse import ArgumentParser
import multiprocessing
import time
# Multiple Polynomial Quadratic Sieve
def mpqs(n, time_new=0.0, timeout=30,verbose=False):
  if verbose:
    time1 = clock()

  root_n = isqrt(n)
  root_2n = isqrt(n+n)
  # formula chosen by experimentation
  # seems to be close to optimal for n &lt; 10^50
  bound = int(5 * log(n, 10)**2)

  prime = []
  mod_root = []
  log_p = []
  num_prime = 0
  # find a number of small primes for which n is a quadratic residue
  p = 2
  while p < bound or num_prime < 3:
    
    # legendre (n|p) is only defined for odd p
    if p > 2:
      leg = legendre(n, p)
    else:
      leg = n & 1

    if leg == 1:
      prime += [p]
      mod_root += [int(mod_sqrt(n, p))]
      log_p += [log(p, 10)]
      num_prime += 1
    elif leg == 0:
      if verbose:
        print 'trial division found factors:'
        print p, 'x', n/p
      return p

    p = next_prime(p)
  # size of the sieve
  x_max = len(prime)*60

  # maximum value on the sieved range
  m_val = (x_max * root_2n) >> 1

  # fudging the threshold down a bit makes it easier to find powers of primes as factors
  # as well as partial-partial relationships, but it also makes the smoothness check slower.
  # there's a happy medium somewhere, depending on how efficient the smoothness check is
  thresh = log(m_val, 10) * 0.735

  # skip small primes. they contribute very little to the log sum
  # and add a lot of unnecessary entries to the table
  # instead, fudge the threshold down a bit, assuming ~1/4 of them pass
  min_prime = int(thresh*3)
  fudge = sum(log_p[i] for i,p in enumerate(prime) if p < min_prime)/4
  thresh -= fudge

  if verbose:
    print 'smoothness bound:', bound
    print 'sieve size:', x_max
    print 'log threshold:', thresh
    print 'skipping primes less than:', min_prime

  smooth = []
  used_prime = set()
  partial = {}
  num_smooth = 0
  num_used_prime = 0
  num_partial = 0
  num_poly = 0
  root_A = isqrt(root_2n / x_max)

  if verbose:
    print 'sieving for smooths...'
  while True:
    # find an integer value A such that:
    # A is =~ sqrt(2*n) / x_max
    # A is a perfect square
    # sqrt(A) is prime, and n is a quadratic residue mod sqrt(A)
    while True:
      root_A = next_prime(root_A)
      leg = legendre(n, root_A)
      if leg == 1:
        break
      elif leg == 0:
        if verbose:
          print 'dumb luck found factors:'
          print root_A, 'x', n/root_A
        return root_A
    if(time.time()>time_new+timeout):
      return "timeout"
    A = root_A * root_A

    # solve for an adequate B
    # B*B is a quadratic residue mod n, such that B*B-A*C = n
    # this is unsolvable if n is not a quadratic residue mod sqrt(A)
    b = mod_sqrt(n, root_A)
    B = (b + (n - b*b) * mod_inv(b + b, root_A))%A

    # B*B-A*C = n &lt;=&gt; C = (B*B-n)/A
    C = (B*B - n) / A

    num_poly += 1

    # sieve for prime factors
    sums = [0.0]*(2*x_max)
    i = 0
    for p in prime:
      if p < min_prime:
        i += 1
        continue
      logp = log_p[i]

      inv_A = mod_inv(A, p)
      # modular root of the quadratic
      a = int(((mod_root[i] - B) * inv_A)%p)
      b = int(((p - mod_root[i] - B) * inv_A)%p)

      k = 0
      while k < x_max:
        if k+a < x_max:
          sums[k+a] += logp
        if k+b < x_max:
          sums[k+b] += logp
        if k:
          sums[k-a+x_max] += logp
          sums[k-b+x_max] += logp

        k += p
      i += 1

    # check for smooths
    i = 0
    for v in sums:
      if v > thresh:
        x = x_max-i if i > x_max else i
        vec = set()
        sqr = []
        # because B*B-n = A*C
        # (A*x+B)^2 - n = A*A*x*x+2*A*B*x + B*B - n
        #               = A*(A*x*x+2*B*x+C)
        # gives the congruency
        # (A*x+B)^2 = A*(A*x*x+2*B*x+C) (mod n)
        # because A is chosen to be square, it doesn't need to be sieved
        val = sieve_val = A*x*x + 2*B*x + C

        if sieve_val < 0:
          vec = set([-1])
          sieve_val = -sieve_val

        for p in prime:
          while sieve_val%p == 0:
            if p in vec:
              # keep track of perfect square factors
              # to avoid taking the sqrt of a gigantic number at the end
              sqr += [p]
            vec ^= set([p])
            sieve_val = int(sieve_val / p)

        if sieve_val == 1:
          # smooth
          smooth += [(vec, (sqr, (A*x+B), root_A))]
          used_prime |= vec
        elif sieve_val in partial:
          # combine two partials to make a (xor) smooth
          # that is, every prime factor with an odd power is in our factor base
          pair_vec, pair_vals = partial[sieve_val]
          sqr += list(vec & pair_vec) + [sieve_val]
          vec ^= pair_vec
          smooth += [(vec, (sqr + pair_vals[0], (A*x+B)*pair_vals[1], root_A*pair_vals[2]))]
          used_prime |= vec
          num_partial += 1
        else:
          # save partial for later pairing
          partial[sieve_val] = (vec, (sqr, A*x+B, root_A))
      i += 1

    num_smooth = len(smooth)
    num_used_prime = len(used_prime)

    if verbose:
      print 100 * num_smooth / num_prime, 'percent complete\r',

    if num_smooth > num_used_prime:
      if verbose:
        print '%d polynomials sieved (%d values)'%(num_poly, num_poly*x_max*2)
        print 'found %d smooths (%d from partials) in %f seconds'%(num_smooth, num_partial, clock()-time1)
        print 'solving for non-trivial congruencies...'

      used_prime_list = sorted(list(used_prime))

      # set up bit fields for gaussian elimination
      masks = []
      mask = 1
      bit_fields = [0]*num_used_prime
      for vec, vals in smooth:
        masks += [mask]
        i = 0
        for p in used_prime_list:
          if p in vec: bit_fields[i] |= mask
          i += 1
        mask <<= 1

      # row echelon form
      col_offset = 0
      null_cols = []
      for col in xrange(num_smooth):
        pivot = col-col_offset == num_used_prime or bit_fields[col-col_offset] & masks[col] == 0
        for row in xrange(col+1-col_offset, num_used_prime):
          if bit_fields[row] & masks[col]:
            if pivot:
              bit_fields[col-col_offset], bit_fields[row] = bit_fields[row], bit_fields[col-col_offset]
              pivot = False
            else:
              bit_fields[row] ^= bit_fields[col-col_offset]
        if pivot:
          null_cols += [col]
          col_offset += 1

      # reduced row echelon form
      for row in xrange(num_used_prime):
        # lowest set bit
        mask = bit_fields[row] & -bit_fields[row]
        for up_row in xrange(row):
          if bit_fields[up_row] & mask:
            bit_fields[up_row] ^= bit_fields[row]

      # check for non-trivial congruencies
      for col in null_cols:
        all_vec, (lh, rh, rA) = smooth[col]
        lhs = lh   # sieved values (left hand side)
        rhs = [rh] # sieved values - n (right hand side)
        rAs = [rA] # root_As (cofactor of lhs)
        i = 0
        for field in bit_fields:
          if field & masks[col]:
            vec, (lh, rh, rA) = smooth[i]
            lhs += list(all_vec & vec) + lh
            all_vec ^= vec
            rhs += [rh]
            rAs += [rA]
          i += 1

        factor = gcd(list_prod(rAs)*list_prod(lhs) - list_prod(rhs), n)
        if factor != 1 and factor != n:
          break
      else:
        if verbose:
          print 'none found.'
        continue
      break

  if verbose:
    print 'factors found:'
    print factor, 'x', n/factor
    print 'time elapsed: %f seconds'%(clock()-time1)
  
  return factor

def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True
def isPrime(n, _precision_for_huge_n=16):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])
_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if isPrime(x)]


if __name__ == "__main__":
  parser =ArgumentParser(description='Uses a MPQS to factor a composite number')
  parser.add_argument('composite', metavar='number_to_factor', type=long,
      help='the composite number to factor')
  parser.add_argument('--verbose', dest='verbose', action='store_true',
      help="enable verbose output")
  args = parser.parse_args()

  if args.verbose:
    mpqs(args.composite, args.verbose)
  else:
    time1 = clock()
    print mpqs(args.composite)
    print 'time elapsed: %f seconds'%(clock()-time1)
