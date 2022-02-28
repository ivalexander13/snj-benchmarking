import numpy as np
import matplotlib.pyplot as plt
import math

# from simulate import simulate
def ewhd_given_h(num_sites, mut_rate, collision_rate, height, time):
    t = time
    k = num_sites
    r = mut_rate
    q = collision_rate
    h = height

    expected = float(0)

    temp = 1 - np.exp(-h * r)
    temp1 = 1 - np.exp((h - t) * r)
    a = 2 * (temp ** 2) * (1 - q)
    b = 2 * temp * (1 - temp)
    for m in range(k):
        psi = math.comb(k, m) * (temp1) ** m * (1 - temp1) ** (k - m)
        expected += (k - m) * (a + b) * psi

    return expected


def graph(num_sites, mut_rate, collision_rate, time, increment):
    f = lambda h: simulate(
        num_sites, mut_rate, collision_rate, h, time, 2
    )  # TODO make this num samples a parameter (currently 100)
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
    line1 = ax.plot(x, sim, label="simulation")
    line2 = ax.plot(x, expect, label="expectation")
    legend1 = ax.legend(handles=line1, loc="upper right")
    ax.add_artist(legend1)
    legend2 = ax.legend(handles=line2, loc="upper left")
    ax.add_artist(legend2)
    ax.set_xlabel("height")
    ax.set_ylabel("weighted hamming")
    title = (
        "_rate"
        + str(mut_rate)
        + "_sites"
        + str(num_sites)
        + "_collision:"
        + str(collision_rate)
        + "_time"
        + str(time)
    )
    ax.set_title(title)
    plt.savefig(title + ".jpg")


def inverse(f, y, lower, upper, error_tolerance):
    x = (upper + lower) / 2.0
    if abs(f(x) - y) < error_tolerance:
        return x
    elif f(x) < y:
        return inverse(f, y, x, upper, error_tolerance)
    else:
        return inverse(f, y, lower, x, error_tolerance)


def ewhd_inv(num_sites, mut_rate, collision_rate, h, time, error_tolerance):
    f = lambda x: ewhd_given_h(num_sites, mut_rate, collision_rate, x, time)
    return inverse(f, h, 0, time, error_tolerance)
