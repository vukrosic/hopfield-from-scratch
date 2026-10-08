"""Step 6. The 2016 repair by Dmitry Krotov and John Hopfield: let the stored pictures that look like the present
state speak much louder than the rest."""
import random
from net import N, icon, learn, settle, damage, wrong, show
from save import save


def overlap(a, b):
    """Squares that agree minus squares that differ. 100 means the same picture, -100 the negative, 0 unrelated."""
    return sum(x * y for x, y in zip(a, b))


def settle_dense(pictures, state, power, rng, max_sweeps=50):
    """Each switch asks every stored picture two questions: how good is your match if I am on, and if I am off?
    A match counts as overlap to the given power. The switch takes the side with the larger total.
    With power 2 this is exactly the old rule with wires. Everything is counted in whole numbers."""
    state = state[:]
    n = len(state)
    over = [overlap(p, state) for p in pictures]
    flips = 0
    for sweep in range(1, max_sweeps + 1):
        order = list(range(n))
        rng.shuffle(order)
        changed = 0
        for i in order:
            si = state[i]
            total = 0
            for p, m in zip(pictures, over):
                r = m - p[i] * si                       # the match without switch i
                total += (r + p[i]) ** power - (r - p[i]) ** power
            new = 1 if total >= 0 else -1
            if new != si:
                state[i] = new
                for k, p in enumerate(pictures):
                    over[k] += 2 * new * p[i]
                changed += 1
        flips += changed
        if changed == 0:
            return state, flips, sweep
    return state, flips, max_sweeps


def noise(n, rng):
    return [rng.choice((-1, 1)) for _ in range(n)]


# 1. Power 2 is the old network. Same start, same order of visits, same end.
NAMES = ['heart', 'house', 'face']
pics = [icon(n) for n in NAMES]
w = learn(pics)
same = 0
for t in range(200):
    start = noise(N, random.Random(t))
    a, _, _ = settle(w, start, random.Random(t + 1))
    b, _, _ = settle_dense(pics, start, 2, random.Random(t + 1))
    same += a == b
print('Power 2 against the network with wires, 200 random starts: the same end state in %d of 200.' % same)
print()

# 2. The tree that would not fit in step 4.
four = pics + [icon('tree')]
names4 = NAMES + ['tree']
tree_rows = []
print('Four pictures: heart, house, face and the tree. Each asked back 1,000 times from 20 flipped squares.')
print('power    ' + ''.join('%8s' % n for n in names4))
for power in (2, 3, 4):
    got = []
    for k, p in enumerate(four):
        ok = 0
        for t in range(1000):
            rng = random.Random(10000 * k + t)
            out, _, _ = settle_dense(four, damage(p, 0.20, rng), power, rng)
            ok += out == p
        got.append(ok)
    tree_rows.append({'power': power, 'whole': got})
    print('%5d    ' % power + ''.join('%8d' % g for g in got))
print()

# 3. How many random pictures fit in 100 switches now?
COUNTS = [10, 30, 100, 300, 1000, 3000]
SAMPLE = 20
rows = []
print('Random pictures in 100 switches. %d of them are asked back from 10 flipped squares.' % SAMPLE)
print('Pictures that come back whole:')
print('power    ' + ''.join('%8d' % c for c in COUNTS) + '   pictures stored')
for power in (2, 3, 4):
    got = []
    for c in COUNTS:
        rng = random.Random(600 + c)
        stored = [noise(N, rng) for _ in range(c)]
        ok = 0
        for p in stored[:SAMPLE]:
            out, _, _ = settle_dense(stored, damage(p, 0.10, rng), power, rng)
            ok += out == p
        got.append(ok)
    rows.append({'power': power, 'whole': got})
    print('%5d    ' % power + ''.join('%8s' % ('%d/%d' % (g, min(SAMPLE, c))) for g, c in zip(got, COUNTS)))
print()

# 4. The negative pictures of step 4. An odd power has no place for them.
STARTS = 2000
ghosts = []
for power in (2, 3, 4):
    kind = {'picture': 0, 'negative': 0, 'other': 0}
    for t in range(STARTS):
        r = random.Random(t)
        out, _, _ = settle_dense(pics, noise(N, r), power, r)
        if out in pics:
            kind['picture'] += 1
        elif [-x for x in out] in pics:
            kind['negative'] += 1
        else:
            kind['other'] += 1
    ghosts.append({'power': power, **kind})
    print('Power %d, %d random starts: a stored picture %d, a negative %d, anything else %d.' % (
        power, STARTS, kind['picture'], kind['negative'], kind['other']))

# 5. The heart of step 5 under 27 random pictures, and under 1,000.
print()
heavy = []
for extra in (27, 1000):
    for power in (2, 4):
        ok = 0
        for t in range(50):
            rng = random.Random(t)
            stored = pics + [noise(N, rng) for _ in range(extra)]
            out, _, _ = settle_dense(stored, damage(pics[0], 0.10, rng), power, rng)
            ok += out == pics[0]
        heavy.append({'extra': extra, 'power': power, 'whole': ok, 'trials': 50})
        print('Heart, house, face and %d random pictures, power %d: the heart came back whole in %d of 50 runs.' % (
            extra, power, ok))

save(6, same=same, names4=names4, tree=tree_rows, counts=COUNTS, sample=SAMPLE, rows=rows, ghosts=ghosts,
     starts=STARTS, heavy=heavy)
