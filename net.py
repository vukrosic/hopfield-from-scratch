"""The whole network. A neuron is a switch: +1 (on) or -1 (off). A picture of 10 x 10 squares is 100 switches."""
import random

SIDE = 10
N = SIDE * SIDE

ICONS = {
    'heart': ['..........',
              '.XX....XX.',
              'XXXX..XXXX',
              'XXXXXXXXXX',
              'XXXXXXXXXX',
              '.XXXXXXXX.',
              '..XXXXXX..',
              '...XXXX...',
              '....XX....',
              '..........'],
    'house': ['....XX....',
              '...XXXX...',
              '..XXXXXX..',
              '.XXXXXXXX.',
              'XXXXXXXXXX',
              '.X......X.',
              '.X.XX...X.',
              '.X.XX...X.',
              '.X.XX...X.',
              '.XXXXXXXX.'],
    'face': ['..XXXXXX..',
             '.X......X.',
             'X........X',
             'X..X..X..X',
             'X........X',
             'X........X',
             'X.X....X.X',
             'X..XXXX..X',
             '.X......X.',
             '..XXXXXX..'],
    'tree': ['....XX....',
             '...XXXX...',
             '..XXXXXX..',
             '.XXXXXXXX.',
             '..XXXXXX..',
             '.XXXXXXXX.',
             'XXXXXXXXXX',
             '....XX....',
             '....XX....',
             '...XXXX...'],
    'key': ['..........',
            '.XXX......',
            'X...X.....',
            'X...XXXXXX',
            'X...X..X.X',
            '.XXX...X.X',
            '..........',
            '..........',
            '..........',
            '..........'],
    'cup': ['..........',
            'XXXXXXX...',
            'X.....XXX.',
            'X.....X.X.',
            'X.....X.X.',
            'X.....XXX.',
            'X.....X...',
            '.XXXXX....',
            '..........',
            'XXXXXXXXX.'],
}


def icon(name):
    """A picture as a list of 100 switches, row by row."""
    return [1 if c == 'X' else -1 for row in ICONS[name] for c in row]


def show(state):
    return '\n'.join(''.join('#' if state[r * SIDE + c] > 0 else '.' for c in range(SIDE)) for r in range(SIDE))


def add(w, p):
    """Hebb's rule for one picture. For every pair of switches: add 1 if they agree in the picture, take away 1 if
    they differ. Nothing else is stored. The weights are whole numbers, and a switch has no wire to itself."""
    n = len(p)
    for i in range(n):
        pi, row = p[i], w[i]
        for j in range(n):
            if i != j:
                row[j] += pi * p[j]


def learn(pictures):
    """Start with every wire at zero, then add the pictures one by one."""
    n = len(pictures[0])
    w = [[0] * n for _ in range(n)]
    for p in pictures:
        add(w, p)
    return w


def push(w, state, i):
    """What the other switches tell switch i: the sum of weight times state over all its wires."""
    return sum(a * b for a, b in zip(w[i], state))


def energy(w, state):
    """Hopfield's number for a whole state. Low when wired-together switches agree. Counted in whole numbers."""
    n = len(state)
    return -sum(w[i][j] * state[i] * state[j] for i in range(n) for j in range(i + 1, n))


def settle(w, state, rng, max_sweeps=50):
    """Visit the switches in random order. Each one obeys the push it gets. Stop when a full round changes nothing.
    Returns the final state, the number of flips and the number of rounds."""
    state = state[:]
    n = len(state)
    flips = 0
    for sweep in range(1, max_sweeps + 1):
        order = list(range(n))
        rng.shuffle(order)
        changed = 0
        for i in order:
            new = 1 if push(w, state, i) >= 0 else -1
            if new != state[i]:
                state[i] = new
                changed += 1
        flips += changed
        if changed == 0:
            return state, flips, sweep
    return state, flips, max_sweeps


def damage(state, share, rng):
    """Flip a share of the switches, chosen at random."""
    state = state[:]
    for i in rng.sample(range(len(state)), round(share * len(state))):
        state[i] = -state[i]
    return state


def wrong(a, b):
    return sum(x != y for x, y in zip(a, b))
