import numpy as np


with open("inputs/09-txt") as f:
    input = [line.strip() for line in f.readlines()]


def diff(seq):
    derivatives = [seq]
    while not all(seq == np.zeros_like(seq)):
        seq = np.diff(seq)
        derivatives.append(seq)
    return derivatives


def forward(dt):
    dt[-1] = np.append(dt[-1], 0)
    for i in range(2, len(dt) + 1):
        dt[-i] = np.append(dt[-i], dt[-i][-1] + dt[-i + 1][-1])
    return dt


def backward(dt):
    dt[-1] = np.insert(dt[-1], 0, 0)
    for i in range(2, len(dt) + 1):
        dt[-i] = np.insert(dt[-i], 0, dt[-i][0] - dt[-i + 1][0])
    return dt


acc = 0
for line in input:
    seq = np.array([int(n) for n in line.split()])
    dt = diff(seq)
    # print(dt)
    # predicted = forward(dt)
    predicted = backward(dt)
    # print(predicted)
    # acc += predicted[0][-1]
    acc += predicted[0][0]
print(acc)
