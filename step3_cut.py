"""Step 3. Where is the memory? Cut wires at random and ask again."""
import random
from net import N, icon, learn, settle, damage, wrong, show
from save import save

NAMES = ['heart', 'house', 'face']
pics = [icon(n) for n in NAMES]
pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
TRIALS = 300
rows, example = [], None
for cut in (0, 25, 50, 75, 90, 95, 98):
    w = learn(pics)
    rng = random.Random(cut)
    gone = rng.sample(pairs, round(len(pairs) * cut / 100))
    for i, j in gone:
        w[i][j] = w[j][i] = 0
    ok, bad = 0, 0
    for k in range(3):
        for t in range(TRIALS):
            r = random.Random(100000 * k + 1000 * cut + t)
            out, _, _ = settle(w, damage(pics[k], 0.2, r), r)
            ok += out == pics[k]
            bad += wrong(out, pics[k])
    rows.append({'cut': cut, 'left': len(pairs) - len(gone), 'ok': ok, 'wrong': bad / (3 * TRIALS)})
    print(f'   {cut:2d}% of the wires cut ({len(pairs) - len(gone):,} left): {ok} of {3 * TRIALS} damaged pictures came back whole; '
          f'on average {bad / (3 * TRIALS):.1f} of 100 squares wrong')
    if cut == 50:
        r = random.Random(5)
        s0 = damage(pics[2], 0.2, r)
        example = {'gone': gone, 'start': s0, 'end': settle(w, s0, r)[0]}

# the other way around: one switch and its wires
w = learn(pics)
print(f'   wires on one switch: {N - 1}. Each wire counts three pictures at once, as one number from -3 to +3.')
save(3, rows=rows, trials=3 * TRIALS, example=example)
