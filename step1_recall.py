"""Step 1. A memory you can ask with a broken picture. Three pictures go into 100 switches and 4,950 wires."""
import random
from net import N, SIDE, icon, learn, settle, damage, wrong, show, push
from save import save

NAMES = ['heart', 'house', 'face']
pics = [icon(n) for n in NAMES]
w = learn(pics)
wires = [w[i][j] for i in range(N) for j in range(i + 1, N)]
print(f'{N} switches, {len(wires):,} wires. Three pictures stored: {", ".join(NAMES)}.')
print('   wire strengths: ' + ', '.join(f'{v:+d}: {wires.count(v):,}' for v in sorted(set(wires))))

# one damaged heart, watched switch by switch
rng = random.Random(7)
start = damage(pics[0], 0.25, rng)
state, trace, flips = start[:], [wrong(start, pics[0])], []
order = list(range(N))
rng.shuffle(order)
for i in order:
    new = 1 if push(w, state, i) >= 0 else -1
    if new != state[i]:
        state[i] = new
        flips.append(i)
    trace.append(wrong(state, pics[0]))
print(f'A heart with 25 of 100 squares flipped. One round through the switches: {len(flips)} flips, '
      f'{wrong(state, pics[0])} squares wrong at the end.')
print(show(start))
print()
print(show(state))

# half of the picture covered
half = {}
for k, name in enumerate(NAMES):
    cut = pics[k][:N // 2] + [-1] * (N // 2)
    out, _, rounds = settle(w, cut, random.Random(k))
    half[name] = {'start_wrong': wrong(cut, pics[k]), 'end_wrong': wrong(out, pics[k]), 'rounds': rounds}
    print(f'   {name}, bottom half wiped: {wrong(cut, pics[k])} squares wrong before, {wrong(out, pics[k])} after')

# how much damage is too much
TRIALS = 1000
table = {}
for share in (0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6):
    got = []
    for k in range(3):
        ok = neg = 0
        for t in range(TRIALS):
            r = random.Random(100000 * k + 1000 * round(share * 100) + t)
            out, _, _ = settle(w, damage(pics[k], share, r), r)
            ok += out == pics[k]
            neg += out == [-x for x in pics[k]]
        got.append((ok, neg))
    table[str(round(share * 100))] = got
    print(f'   {round(share * 100):2d} squares flipped, {TRIALS:,} tries each: came back '
          + ', '.join(f'{NAMES[k]} {got[k][0]:,}' for k in range(3))
          + f'   (ended as the negative: {sum(g[1] for g in got):,})')

save(1, names=NAMES, pics=pics, wire_counts={str(v): wires.count(v) for v in sorted(set(wires))}, start=start,
     flips=flips, order=order, trace=trace, half=half, table=table, trials=TRIALS)
