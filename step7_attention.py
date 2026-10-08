"""Step 7. Push the same idea to its end: the 2020 update rule. Then write the attention step of a chatbot next to
it and compare the numbers."""
import random
from math import exp
from net import N, ICONS, icon, damage, wrong
from save import save


def dot(a, b):
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total


def shares(scores, beta):
    """Boltzmann's rule (softmax): turn scores into shares that add up to 1. A higher beta means a colder,
    stricter choice. Beta is one divided by the temperature."""
    top = max(scores)
    e = [exp(beta * (s - top)) for s in scores]
    total = 0.0
    for x in e:
        total += x
    return [x / total for x in e]


def recall(pictures, state, beta):
    """The 2020 rule, one move: score every stored picture by its overlap with the state, turn the scores into
    shares, and become the mix of the pictures in those shares."""
    part = shares([dot(p, state) for p in pictures], beta)
    new = [0.0] * len(state)
    for share, p in zip(part, pictures):
        for i, x in enumerate(p):
            new[i] += share * x
    return new, part


def attention(query, keys, values, beta):
    """One attention step as a language model does it: compare the query with every key, turn the scores into
    shares, hand back the mix of the values in those shares."""
    scores = []
    for key in keys:
        score = 0.0
        for q, k in zip(query, key):
            score += q * k
        scores.append(score)
    top = max(scores)
    weights = [exp(beta * (s - top)) for s in scores]
    total = 0.0
    for x in weights:
        total += x
    out = [0.0] * len(values[0])
    for wgt, value in zip(weights, values):
        for i, x in enumerate(value):
            out[i] += wgt / total * x
    return out


def signs(state):
    return [1 if x >= 0 else -1 for x in state]


def noise(n, rng):
    return [rng.choice((-1, 1)) for _ in range(n)]


def gray(state):
    """A state with values between -1 and 1, printed in five shades."""
    side = int(len(state) ** 0.5)
    shade = ' .:x#'
    return '\n'.join(''.join(shade[min(4, int((state[r * side + c] + 1) * 2.5))] for c in range(side))
                     for r in range(side))


NAMES = ['heart', 'house', 'face', 'tree', 'key', 'cup']
pics = [icon(n) for n in NAMES]

# 1. One move is enough.
rng = random.Random(7)
start = damage(pics[0], 0.25, rng)
out, part = recall(pics, start, 1.0)
print('Six pictures stored: %s. The heart with 25 squares flipped goes in. Beta is 1.' % ', '.join(NAMES))
print('Overlap with each picture: ' + ', '.join('%s %d' % (n, dot(p, start)) for n, p in zip(NAMES, pics)))
print('Shares after one move:     ' + ', '.join('%s %.6f' % (n, x) for n, x in zip(NAMES, part)))
print('Squares wrong after one move: %d' % wrong(signs(out), pics[0]))
print()

# 2. The temperature dial.
dial = []
print('The same start at different settings of beta:')
for beta in (0.001, 0.01, 0.02, 0.03, 0.05, 0.1, 1.0):
    state = start
    for _ in range(20):
        state, part = recall(pics, state, beta)
    dial.append({'beta': beta, 'shares': part, 'state': state, 'wrong': wrong(signs(state), pics[0])})
    print('beta %-6s shares after 20 moves: %s' % (beta, ' '.join('%s %.2f' % (n, x) for n, x in zip(NAMES, part))))
print()
print('Beta 0.001: the network rests in a mix of everything it knows.')
print(gray(dial[0]['state']))
print()

# 3. How many pictures now?
COUNTS = [100, 1000, 10000, 30000]
SAMPLE = 20
rows = []
print('Random pictures in 100 switches, beta 1. %d are asked back from 25 flipped squares, one move each.' % SAMPLE)
for c in COUNTS:
    r = random.Random(700 + c)
    stored = [noise(N, r) for _ in range(c)]
    ok = 0
    low = 1.0
    for p in stored[:SAMPLE]:
        out, part = recall(stored, damage(p, 0.25, r), 1.0)
        ok += signs(out) == p
        low = min(low, max(part))
    rows.append({'count': c, 'whole': ok, 'lowest_share': low})
    print('%6d pictures stored: %d of %d back whole. Smallest share the right picture got: %.4f' % (c, ok, SAMPLE, low))
print()

# 4. The same numbers from the attention step.
worst = 0.0
for beta in (0.01, 0.05, 1.0):
    for t in range(50):
        q = damage(pics[t % 6], 0.25, random.Random(t))
        a, _ = recall(pics, q, beta)
        b = attention(q, pics, pics, beta)
        worst = max(worst, max(abs(x - y) for x, y in zip(a, b)))
print('recall(pictures, state) against attention(query=state, keys=pictures, values=pictures), 150 cases:')
print('largest difference in any square: %.1e' % worst)
print()

# 5. Keys and values do not have to be the same thing. Keys: the pictures. Values: their names.
labels = [[1.0 if i == k else 0.0 for i in range(6)] for k in range(6)]
lookups = []
print('Keys are the six pictures, values are the six names. A damaged picture goes in as the question.')
for k in (0, 3, 4):
    q = damage(pics[k], 0.25, random.Random(40 + k))
    ans = attention(q, pics, labels, 1.0)
    lookups.append({'asked': NAMES[k], 'query': q, 'answer': ans})
    print('damaged %-6s -> %s' % (NAMES[k], ' '.join('%s %.4f' % (n, x) for n, x in zip(NAMES, ans))))

save(7, names=NAMES, pics=pics, start=start, overlaps=[dot(p, start) for p in pics], one=recall(pics, start, 1.0)[1],
     dial=dial, counts=COUNTS, sample=SAMPLE, rows=rows, worst=worst, lookups=lookups)
