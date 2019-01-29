def list_prod(a):
  size = len(a)
  if size == 1:
    return a[0]
  return list_prod(a[:size>>1]) * list_prod(a[size>>1:])

# greatest common divisor of a and b
def gcd(a, b):
  while b:
    a, b = b, a%b
  return a

# modular inverse of a mod m
def mod_inv(a, m):
  a = int(a%m)
  x, u = 0, 1
  while a:
    x, u = u, x - (m/a)*u
    m, a = a, m%a
  return x

# legendre symbol (a|m)
# note: returns m-1 if a is a non-residue, instead of -1
def legendre(a, m):
  return pow(a, (m-1) >> 1, m)

# modular sqrt(n) mod p
# p must be prime
def mod_sqrt(n, p):
  a = n%p
  if p%4 == 3:
    return pow(a, (p+1) >> 2, p)
  elif p%8 == 5:
    v = pow(a << 1, (p-5) >> 3, p)
    i = ((a*v*v << 1) % p) - 1
    return (a*v*i)%p
  elif p%8 == 1:
    # Shank's method
    q = p-1
    e = 0
    while q&1 == 0:
      e += 1
      q >>= 1

    n = 2
    while legendre(n, p) != p-1:
      n += 1

    w = pow(a, q, p)
    x = pow(a, (q+1) >> 1, p)
    y = pow(n, q, p)
    r = e
    while True:
      if w == 1:
        return x

      v = w
      k = 0
      while v != 1 and k+1 < r:
        v = (v*v)%p
        k += 1

      if k == 0:
        return x

      d = pow(y, 1 << (r-k-1), p)
      x = (x*d)%p
      y = (d*d)%p
      w = (w*y)%p
      r = k
  else: # p == 2
    return a

#integer sqrt of n
def isqrt(n):
  c = n*4/3
  d = c.bit_length()

  a = d>>1
  if d&1:
    x = 1 << a
    y = (x + (n >> a)) >> 1
  else:
    x = (3 << a) >> 2
    y = (x + (c >> a)) >> 1

  if x != y:
    x = y
    y = (x + n/x) >> 1
    while y < x:
      x = y
      y = (x + n/x) >> 1
  return x

# strong probable prime
def is_sprp(n, b=2):
  if n < 2: return False
  d = n-1
  s = 0
  while d&1 == 0:
    s += 1
    d >>= 1

  x = pow(b, d, n)
  if x == 1 or x == n-1:
    return True

  for r in xrange(1, s):
    x = (x * x)%n
    if x == 1:
      return False
    elif x == n-1:
      return True

  return False

# lucas probable prime
# assumes D = 1 (mod 4), (D|n) = -1
def is_lucas_prp(n, D):
  P = 1
  Q = (1-D) >> 2

  # n+1 = 2**r*s where s is odd
  s = n+1
  r = 0
  while s&1 == 0:
    r += 1
    s >>= 1

  # calculate the bit reversal of (odd) s
  # e.g. 19 (10011) <=> 25 (11001)
  t = 0
  while s:
    if s&1:
      t += 1
      s -= 1
    else:
      t <<= 1
      s >>= 1

  # use the same bit reversal process to calculate the sth Lucas number
  # keep track of q = Q**n as we go
  U = 0
  V = 2
  q = 1
  # mod_inv(2, n)
  inv_2 = (n+1) >> 1
  while t:
    if t&1:
      # U, V of n+1
      U, V = ((U + V) * inv_2)%n, ((D*U + V) * inv_2)%n
      q = (q * Q)%n
      t -= 1
    else:
      # U, V of n*2
      U, V = (U * V)%n, (V * V - 2 * q)%n
      q = (q * q)%n
      t >>= 1

  # double s until we have the 2**r*sth Lucas number
  while r:
    U, V = (U * V)%n, (V * V - 2 * q)%n
    q = (q * q)%n
    r -= 1

  # primality check
  # if n is prime, n divides the n+1st Lucas number, given the assumptions
  return U == 0

# primes less than 212
small_primes = set([
    2,  3,  5,  7, 11, 13, 17, 19, 23, 29,
   31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
   73, 79, 83, 89, 97,101,103,107,109,113,
  127,131,137,139,149,151,157,163,167,173,
  179,181,191,193,197,199,211])

# pre-calced sieve of eratosthenes for n = 2, 3, 5, 7
indices = [
    1, 11, 13, 17, 19, 23, 29, 31, 37, 41,
   43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
   89, 97,101,103,107,109,113,121,127,131,
  137,139,143,149,151,157,163,167,169,173,
  179,181,187,191,193,197,199,209]

# distances between sieve values
offsets = [
  10, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6,
   6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4,
   2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6,
   4, 2, 4, 6, 2, 6, 4, 2, 4, 2,10, 2]

max_int = 2147483647

# an 'almost certain' primality check
def is_prime(n):
  if n < 212:
    return n in small_primes

  for p in small_primes:
    if n%p == 0:
      return False

  # if n is a 32-bit integer, perform full trial division
  if n <= max_int:
    i = 211
    while i*i < n:
      for o in offsets:
        i += o
        if n%i == 0:
          return False
    return True

  # Baillie-PSW
  # this is technically a probabalistic test, but there are no known pseudoprimes
  if not is_sprp(n, 2): return False

  # idea shamelessly stolen from Mathmatica
  # if n is a 2-sprp and a 3-sprp, n is necessarily square-free
  if not is_sprp(n, 3): return False

  a = 5
  s = 2
  # if n is a perfect square, this will never terminate
  while legendre(a, n) != n-1:
    s = -s
    a = s-a
  return is_lucas_prp(n, a)

# next prime strictly larger than n
def next_prime(n):
  if n < 2:
    return 2
  # first odd larger than n
  n = (n + 1) | 1
  if n < 212:
    while True:
      if n in small_primes:
        return n
      n += 2

  # find our position in the sieve rotation via binary search
  x = int(n%210)
  s = 0
  e = 47
  m = 24
  while m != e:
    if indices[m] < x:
      s = m
      m = (s + e + 1) >> 1
    else:
      e = m
      m = (s + e) >> 1

  i = int(n + (indices[m] - x))
  # adjust offsets
  offs = offsets[m:] + offsets[:m]
  while True:
    for o in offs:
      if is_prime(i):
        return i
      i += o
