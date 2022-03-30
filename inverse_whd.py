from scipy.stats import expon
import numpy as np
import matplotlib.pyplot as plt
import math
#from simulate import simulate

def ewhd_given_h(num_sites, mut_rate, collision_rate, height, time):
    t = time
    k = num_sites
    r = mut_rate
    q = collision_rate
    h = height
    # print(f'### HEIGHT: {h}')
    
    return (2 * (1 - np.exp(-h * r)) ** 2 * (1 - q) + 2 * (1 - np.exp(-h * r)) * (np.exp(-h * r))) * (np.exp(r * (h - t))) 

def simulate(num_sites, mut_rate, collision_rate, height, time, sample):
    total = 0
    for _ in range(sample):
        whd = 0
        shared = 0
        for _ in range(num_sites):
            if expon.rvs(scale=1.0/mut_rate) < time - height:
                shared += 1
        for _ in range(num_sites - shared):
            a, b = 0, 0
            if expon.rvs(scale=1.0/mut_rate) < height:
                a = 1
            if expon.rvs(scale=1.0/mut_rate) < height:
                b = 1
            if a == b and b == 1 and np.random.uniform(low=0.0, high=1.0) < collision_rate:
                a, b = 0, 0
            whd += a + b 
        total += whd
    return total / sample 


def graph(num_sites, mut_rate, collision_rate, time, increment):
    f = lambda h: simulate(num_sites, mut_rate, collision_rate, h, time, 2) #TODO make this num samples a parameter (currently 10)
    g = lambda h: ewhd_given_h(num_sites, mut_rate, collision_rate, h, time)
    x = []
    sim = []
    expect = []
    step = time / increment
    for i in range(increment):
        x.append(step * i)
        sim.append(f(step * i))
        expect.append(g(step * i))
    
    fig = plt.figure()
    fig, ax = plt.subplots()
    line1 = ax.plot(x, sim, label='simulation')
    line2 = ax.plot(x, expect, label='expectation')
    legend1 = ax.legend(handles=line1, loc='upper right')
    ax.add_artist(legend1)
    legend2 = ax.legend(handles=line2, loc='upper left')
    ax.add_artist(legend2)
    ax.set_xlabel('height')
    ax.set_ylabel('weighted hamming')
    title = '_rate' + str(mut_rate) + '_sites' + str(num_sites) + '_collision:' + str(collision_rate) + '_time' + str(time)
    ax.set_title(title)
    plt.savefig(title + '.jpg') 

def inverse(f, y, lower, upper, error_tolerance, depth):
    x = (upper + lower) / 2.0
    # print(abs(f(x) - y))
    if abs(f(x) - y) < error_tolerance or depth >= 10:
        return x
    elif f(x) < y:
        return inverse(f, y, x, upper, error_tolerance, depth+1)
    else:
        return inverse(f, y, lower, x, error_tolerance, depth+1)

def ewhd_inv(num_sites, mut_rate, collision_rate, whd, time, error_tolerance):
    f = lambda x: ewhd_given_h(num_sites, mut_rate, collision_rate, x, time)
    return inverse(f, whd, 0, time,  error_tolerance, 0)