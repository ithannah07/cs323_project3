import random
import time
import math
import numpy as np
from phe import paillier

def generate_value(n, min_val = 0, max_val = 100):
    return [random.randint(min_val, max_val) for _ in range(n)]

def computing_time(start, end):
    # print("Computing time: ", end - start, "seconds")
    elasped = end - start
    return float(round(elasped, 10))

def non_private(values):
    start = time.time()
    mean = float(round(np.mean(values), 3))
    end = time.time()
    elasped = computing_time(start, end)
    
    return mean, elasped


def paillier_average(values):
    start = time.time()

    public_key, private_key = paillier.generate_paillier_keypair()

    enc_values = [public_key.encrypt(x) for x in values]

    enc_sum = enc_values[0]
    for i in range(1, len(enc_values)):
        enc_sum += enc_values[i]
    
    dec_sum = private_key.decrypt(enc_sum)

    mean = round((dec_sum / len(values)), 3)

    end = time.time()
    elasped = computing_time(start, end)

    return mean, elasped

def shamir_secret_sharing(values, n):
    start = time.time()
    # t = floor(n/2)
    t = max(2, math.floor(n/2))
    recovered = []

    # 1. Define polynomial f(x) of degree t-1 for each value
    for v in values:
        coeffs = generate_polynomial(v, t)

        # 2. n개의 share (i, f(i)) 생성
        shares = generate_shares(coeffs, n)
        # print("shares: ", shares)
    
        # 3. 임의로 t개 이상의 share 선택 (trusted party들)
        selected_shares = t_shares(shares, t)
        # print("selected shares: ", selected_shares)

        # 4. Lagrange interpolation을 사용해 원래 값 복원
        reconstruction_value = reconstruction(selected_shares)
        # print("reconstruction value: ", reconstruction_value)
        recovered.append(reconstruction_value)

    # 5. 모든 값 복원 후 평균 계산
    mean = float(round(sum(recovered) / len(recovered), 3))
    end = time.time()
    elasped = computing_time(start, end)

    return mean, elasped

def generate_polynomial(value, t):
    degree = t - 1
    coeffs = [value] + [random.randint(0, 100) for _ in range(degree)]
    return coeffs

def computing_polynomial(coeffs, x):
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result

def generate_shares(coeffs, n):
    shares = []
    for i in range(1, n + 1):
        result = computing_polynomial(coeffs, i)
        shares.append((i, result))
    return shares

def t_shares(shares, t):
    return random.sample(shares, t)

def reconstruction(selected_shares):
    """
    selected shares: [(x1, y1), (x2, y2), ..., (xt, yt)]
    f_i(0) = Σ f_i(j) * l_i(j)
    """
    xs = [x for x, _ in selected_shares]
    ys = [y for _, y in selected_shares]

    secret_i = 0.0

    for j in range(len(xs)):
        xj = xs[j]
        fj = ys[j]
        lj = 1.0

        for k in range(len(xs)):
            if k != j:
                xk = xs[k]
                lj *= ( 0- xk) / (xj - xk)
        secret_i += fj * lj

    return int(round(secret_i))

def main():
    
    for _ in range(5):
        n = input("Enter the number of total parties: ")
        n = int(n)
        values = generate_value(n)
        avg1, t1 = non_private(values)
        avg2, t2 = paillier_average(values)
        avg3, t3 = shamir_secret_sharing(values, n)
        print("Non-private, average: ", avg1, "elapsed time: ", t1)
        print("Paillier, average: ", avg2, "elapsed time: ", t2)
        print("Shamir, average: ", avg3, "elapsed time: ", t3)
        print()
    

if __name__ == "__main__":
    main()