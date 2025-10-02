import random
import time
import numpy as np
import matplotlib.pyplot as plt
from phe import paillier

def generate_value(n, min_val = 0, max_val = 100):
    return [random.randint(min_val, max_val) for _ in range(n)]

def computing_time(start, end):
    print("Computing time: ", end - start, "seconds")
    elasped = end - start
    return elasped

def non_private(values):
    start = time.time()
    mean = float(np.mean(values))
    end = time.time()
    elasped = computing_time(start, end)
    
    return mean, elasped


def pillier_average(values):
    start = time.time()

    public_key, private_key = paillier.generate_paillier_keypair()

    enc_values = [public_key.excrypt(x) for x in values]
    enc_sum = sum(enc_values)
    dec_sum = private_key.decrypt(enc_sum)

    mean = dec_sum / len(values)
    
    end = time.time()
    elasped = computing_time(start, end)

    return mean, elasped





def main():
    values = generate_value(5)
    mean = non_private(values)
    print("average: ", mean)

if __name__ == "__main__":
    main()