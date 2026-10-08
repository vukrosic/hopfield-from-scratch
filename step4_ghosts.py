"""Step 4. Memories nobody stored. Start from random states and see where the network ends."""
import random
from net import N, icon, learn, settle, wrong, show, energy
from save import save

NAMES = ['heart', 'house', 'face']
pics = [icon(n) for n in NAMES]
w = learn(pics)
neg = [[-x for x in p] for p in pics]


def blend(signs):
    """Every square takes a vote of the three pictures (some of them turned into negatives first)."""
    return [1 if sum(s * p[i] for s, p in zip(signs, pics)) > 0 else -1 for i in range(N)]


blends = {}
for a in (1, -1):
    for b in (1, -1):
        for c in (1, -1):
            blends[''.join('+' if s > 0 else '-' for s in (a, b, c))] = blend((a, b, c))

STARTS = 10000
count = {'picture': [0, 0, 0], 'negative': [0, 0, 0], 'blend': {k: 0 for k in blends}, 'other': 0}
others = {}
for t in range(STARTS):
    r = random.Random(t)
    out, _, _ = settle(w, [r.choice((-1, 1)) for _ in range(N)], r)
    if out in pics:
        count['picture'][pics.index(out)] += 1
    elif out in neg:
        count['negative'][neg.index(out)] += 1
    else:
        hit = [k for k, b in blends.items() if b == out]
        if hit:
            count['blend'][hit[0]] += 1
        else:
            count['other'] += 1
            others[tuple(out)] = others.get(tuple(out), 0) + 1
n_blend = sum(count['blend'].values())
print(f'{STARTS:,} random starts. Where they stopped:')
print('   a stored picture: ' + ', '.join(f'{n} {c:,}' for n, c in zip(NAMES, count['picture'])) + f'   ({sum(count["picture"]):,})')
print('   the negative of one: ' + ', '.join(f'{n} {c:,}' for n, c in zip(NAMES, count['negative'])) + f'   ({sum(count["negative"]):,})')
print(f'   a blend of all three (each square by majority vote): {n_blend:,}')
print(f'   anything else: {count["other"]:,} starts, {len(others)} different states')
both = blends['+++']
print(f'the plain blend differs from heart, house, face in {", ".join(str(wrong(both, p)) for p in pics)} squares; '
      f'energy {energy(w, both):,} against {energy(w, pics[0]):,} for the heart')
print(show(both))

# a fourth picture that looks like two of the others
tree = icon('tree')
w4 = learn(pics + [tree])
out, _, _ = settle(w4, tree, random.Random(0))
print(f'add a tree (it differs from the house in {wrong(tree, pics[1])} squares, from the heart in {wrong(tree, pics[0])}):')
print(f'   shown the exact tree, the network changes {wrong(out, tree)} squares of it')
kept = []
for k in range(3):
    ok = 0
    for t in range(1000):
        r = random.Random(100000 * k + t)
        s = pics[k][:]
        for i in r.sample(range(N), 20):
            s[i] = -s[i]
        ok += settle(w4, s, r)[0] == pics[k]
    kept.append(ok)
print('   the first three from 20 flipped squares, 1,000 tries each: ' + ', '.join(f'{n} {c}' for n, c in zip(NAMES, kept)))
key = icon('key')
w4k = learn(pics + [key])
kept_key = []
for k, p in enumerate(pics + [key]):
    ok = 0
    for t in range(1000):
        r = random.Random(100000 * k + t)
        s = p[:]
        for i in r.sample(range(N), 20):
            s[i] = -s[i]
        ok += settle(w4k, s, r)[0] == p
    kept_key.append(ok)
print(f'add a key instead (it differs from the others in {", ".join(str(wrong(key, p)) for p in pics)} squares): '
      + ', '.join(f'{n} {c}' for n, c in zip(NAMES + ['key'], kept_key)))

save(4, starts=STARTS, count=count, blends=blends, others=len(others), plain=both, tree=tree, tree_out=out, kept=kept,
     key=key, kept_key=kept_key, e_blend=energy(w, both))
