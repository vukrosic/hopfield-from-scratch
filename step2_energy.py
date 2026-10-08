"""Step 2. Why it always stops. One number for the whole state, the energy, and no flip ever raises it."""
import random
from net import N, icon, learn, energy, push, damage, wrong
from save import save

NAMES = ['heart', 'house', 'face']
pics = [icon(n) for n in NAMES]
w = learn(pics)

e_pics = [energy(w, p) for p in pics]
rng = random.Random(3)
rand = [[rng.choice((-1, 1)) for _ in range(N)] for _ in range(1000)]
e_rand = [energy(w, s) for s in rand]
print('energy of the stored pictures: ' + ', '.join(f'{n} {e:,}' for n, e in zip(NAMES, e_pics)))
print(f'energy of 1,000 random states: from {min(e_rand):,} to {max(e_rand):,}, average {sum(e_rand) / 1000:,.0f}')

# the damaged heart of step 1, flip by flip
rng = random.Random(7)
state = damage(pics[0], 0.25, rng)
order = list(range(N))
rng.shuffle(order)
trace = [energy(w, state)]
for i in order:
    new = 1 if push(w, state, i) >= 0 else -1
    if new != state[i]:
        state[i] = new
        trace.append(energy(w, state))
drops = [a - b for a, b in zip(trace, trace[1:])]
print(f'the damaged heart: energy {trace[0]:,} at the start, {trace[-1]:,} at the end, {len(drops)} flips; '
      f'smallest drop {min(drops)}, largest {max(drops)}')

# every flip from 1,000 random starts
flips = ups = same = 0
most_rounds, ends = 0, {}
for k, s in enumerate(rand):
    r = random.Random(k)
    s = s[:]
    e = e_rand[k]
    for rounds in range(1, 60):
        order = list(range(N))
        r.shuffle(order)
        changed = 0
        for i in order:
            p = push(w, s, i)
            new = 1 if p >= 0 else -1
            if new != s[i]:
                s[i] = new
                e2 = e - 2 * new * p          # the change of energy, from this switch's push alone
                ups += e2 > e
                same += e2 == e
                e = e2
                changed += 1
        flips += changed
        if changed == 0:
            break
    most_rounds = max(most_rounds, rounds)
    assert e == energy(w, s)
print(f'1,000 random starts: {flips:,} flips in all, {ups} raised the energy, {same} left it the same; '
      f'every start stopped, the slowest after {most_rounds} rounds')

save(2, e_pics=e_pics, e_rand_min=min(e_rand), e_rand_max=max(e_rand), e_rand_mean=sum(e_rand) / 1000, trace=trace,
     drops=drops, flips=flips, ups=ups, same=same, most_rounds=most_rounds)
