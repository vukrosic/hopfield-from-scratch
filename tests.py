"""Checks. run_all.sh runs them last, on the numbers the seven steps saved in runs/, and on the network itself."""
import json
import os
import random
from net import N, icon, learn, energy, settle

HERE = os.path.dirname(os.path.abspath(__file__))
r = {i: json.load(open(os.path.join(HERE, 'runs', 'step%d.json' % i))) for i in range(1, 8)}

# the wires: the same strength in both directions, no wire from a switch to itself, 4,950 pairs
pics = [icon(n) for n in ('heart', 'house', 'face')]
w = learn(pics)
assert all(w[i][j] == w[j][i] for i in range(N) for j in range(N)) and all(w[i][i] == 0 for i in range(N))
assert sum(r[1]['wire_counts'].values()) == N * (N - 1) // 2 == 4950
# every stored picture is a resting place, and so is its negative
for p in pics:
    assert settle(w, p, random.Random(0))[0] == p
    assert settle(w, [-x for x in p], random.Random(0))[0] == [-x for x in p]
    assert energy(w, p) == energy(w, [-x for x in p])

# 1. a quarter of the squares flipped: the heart is back; small damage is always repaired, large damage is not
assert r[1]['trace'][-1] == 0 and len(r[1]['flips']) == 25
assert [x[0] for x in r[1]['table']['10']] == [1000, 1000, 1000] and max(x[0] for x in r[1]['table']['60']) == 0

# 2. the energy only falls
assert r[2]['ups'] == 0 and all(d > 0 for d in r[2]['drops']) and r[2]['trace'][-1] == r[2]['e_pics'][0]
assert max(r[2]['e_pics']) < r[2]['e_rand_min']

# 3. half of the wires gone and recall still works; with one wire in ten left it does not
rows = {x['cut']: x for x in r[3]['rows']}
assert rows[50]['ok'] == r[3]['trials'] and rows[90]['ok'] == 0

# 4. random starts end in a picture, a negative or the blend, and in nothing else
c = r[4]['count']
assert sum(c['picture']) + sum(c['negative']) + sum(c['blend'].values()) + c['other'] == r[4]['starts']
assert c['other'] == 0

# 5. more pictures, worse heart; the breaking point comes at a similar share of the switches for every size
assert r[5]['whole'][0] == r[5]['trials'] and r[5]['whole'][-1] < r[5]['trials'] // 10
for row in r[5]['table']:
    assert row['wrong_pct'][0] < 0.1 and row['wrong_pct'][-1] > 20

# 6. power 2 is the old network; a higher power holds what the old one could not
assert r[6]['same'] == 200
assert r[6]['tree'][0]['whole'][3] == 0 and r[6]['tree'][2]['whole'] == [1000] * 4
assert r[6]['rows'][0]['whole'][1] == 0 and r[6]['rows'][2]['whole'][-1] == r[6]['sample']
assert r[6]['ghosts'][1]['negative'] == 0

# 7. one move brings the heart back; the shares add up to 1; attention gives the same numbers
assert abs(sum(r[7]['one']) - 1) < 1e-12 and r[7]['one'][0] > 0.999999
assert r[7]['dial'][-1]['wrong'] == 0 and max(r[7]['dial'][0]['shares']) < 0.18
assert r[7]['worst'] < 1e-12 and all(x['whole'] == r[7]['sample'] for x in r[7]['rows'])

print('all checks passed')
