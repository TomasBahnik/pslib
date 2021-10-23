## GCD

The greatest common divisor (gcd) of two positive integers is the largest integer that divides evenly into both of them.
For example, the greatest common divisor of 102 and 68 is 34 since both 102 and 68 are multiples of 34, but no integer 
larger than 34 divides evenly into 102 and 68. You may recall learning about the greatest common divisor when you 
learned to reduce fractions. For example, we can simplify 68/102 to 2/3 by dividing both numerator and denominator
by 34, their gcd. Finding the gcd of huge integers is an important problem that arises in many commercial applications, 
including the famous RSA cryptosystem.

### Euclid’s algorithm

Euclid’s algorithm is an iterative computation based on the following observation for positive integers p and q::

```text
if p > q, then if q divides p, the gcd of p and q is q; otherwise, the gcd of p and q is the same as
the gcd of q and p % q
```

To convince yourself of this fact, first note that the gcd of p and q is the same as the gcd of q and p–q, 
because a number divides both p and q if and only if it divides both q and p–q. By the same argument, q and p–2q, q 
and p–3q, and so forth have the same gcd, and one way to compute p % q is to subtract q from p until we
get a number less than q.

The function gcd() in euclid.py (PROGRAM 2.3.1) is a compact recursive function whose reduction step is
based on this property. The base case is when q is 0, with gcd(p, 0) = p. To see that the reduction step converges
to the base case, observe that the value of the second argument strictly decreases in each recursive call
since p % q < q. If p < q, then the first recursive call switches the two arguments. In fact, the value of the 
second argument decreases by at least a factor of 2 for every second recursive call, so the sequence of argument
values quickly converges to the base case (see EXERCISE 2.3.13). This recursive solution to the problem of computing
the greatest common divisor is known as Euclid’s algorithm and is one of the oldest
known algorithms—it is over 2,000 years old.