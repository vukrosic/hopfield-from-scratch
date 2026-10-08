"""Step 5. How many pictures fit? Keep adding pictures to the same wires and watch the old ones."""
import random
from net import N, icon, add, learn, settle, damage, wrong, show
from save import save

NAMES = ['heart', 'house', 'face']
pics = [icon(n) for n in NAMES]


def noise(n, rng):
    """A picture made by tossing a coin for every square."""
    return [rng.choice((-1, 1)) for _ in range(n)]


# Part 1. The three pictures, then one random picture after another on top of them.
EXTRA = 27
TRIALS = 300
whole = [0] * (EXTRA + 1)        # trials in which the heart came back with no wrong square
bad = [0] * (EXTRA + 1)          # wrong squares in the heart, added over the trials
rest = [0] * (EXTRA + 1)         # trials in which the untouched heart stays as it is
SHOWN = (0, 6, 12, 18, 24)
frames = {k: [] for k in SHOWN}     # the heart as it came back in the first twelve runs
for t in range(TRIALS):
    rng = random.Random(t)
    w = learn(pics)
    start = damage(pics[0], 0.10, rng)
    for k in range(EXTRA + 1):
        if k:
            add(w, noise(N, rng))
        out, _, _ = settle(w, start, random.Random(1000 + t))
        miss = wrong(out, pics[0])
        whole[k] += miss == 0
        bad[k] += miss
        same, _, _ = settle(w, pics[0], random.Random(2000 + t))
        rest[k] += same == pics[0]
        if t < 12 and k in SHOWN:
            frames[k].append(out)

print('100 switches. Stored: heart, house, face, then random pictures one by one.')
print('Each time the heart is asked back from a copy with 10 squares flipped. %d different runs.' % TRIALS)
print()
print('pictures stored   heart back whole   wrong squares on average   heart still a resting place')
for k in range(0, EXTRA + 1, 3):
    print('%8d %19s %21.1f %24s' % (k + 3, '%d of %d' % (whole[k], TRIALS), bad[k] / TRIALS, '%d of %d' % (rest[k], TRIALS)))
print()
for k in SHOWN:
    print('%d pictures stored. Wrong squares in the heart, first twelve runs: %s' % (
        k + 3, ' '.join(str(wrong(f, pics[0])) for f in frames[k])))
print()
print('Run 1 with 27 pictures stored:')
print(show(frames[24][0]))
print()

# Part 2. Only random pictures, and three sizes of network. Is the limit a fixed share of the switches?
SIZES = [(100, 40), (200, 20), (400, 10)]
LOADS = [5, 8, 10, 12, 14, 16, 18, 20, 25, 30]      # pictures per 100 switches
table = []
print('Random pictures only. A stored picture is put in untouched, and the network runs until it rests.')
print('Share of squares that end up wrong:')
print()
print('pictures per 100 switches ' + ''.join('%8d' % c for c in LOADS))
for n, trials in SIZES:
    miss = [0] * len(LOADS)
    seen = [0] * len(LOADS)
    for t in range(trials):
        rng = random.Random(50000 + n + t)
        w = [[0] * n for _ in range(n)]
        stored = []
        for c_i, c in enumerate(LOADS):
            while len(stored) < c * n // 100:
                p = noise(n, rng)
                add(w, p)
                stored.append(p)
            for p in stored[:10]:
                out, _, _ = settle(w, p, rng)
                miss[c_i] += wrong(out, p)
                seen[c_i] += n
    row = [100.0 * m / s for m, s in zip(miss, seen)]
    table.append({'n': n, 'trials': trials, 'wrong_pct': row, 'miss': miss, 'seen': seen})
    print('%4d switches             ' % n + ''.join('%7.1f%%' % x for x in row))

save(5, names=NAMES, extra=EXTRA, trials=TRIALS, whole=whole, bad=bad, rest=rest,
     frames={str(k): v for k, v in frames.items()}, loads=LOADS, table=table)
