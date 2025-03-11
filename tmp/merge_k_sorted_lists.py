def nth_prime(n):
    if n < 6:
        limit = 15
    else:
        limit = int(n * (1.2 * (n**0.5)))
    
    sieve = [True] * (limit+1)
    sieve[0], sieve[1] = False, False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    
    primes = [i for i in range(len(sieve)) if sieve[i]]
    
    return primes[n-1]

# Run test cases
test_cases = [5, 7, 10]
for n in test_cases:
    print(f"{n}: {nth_prime(n)}")
