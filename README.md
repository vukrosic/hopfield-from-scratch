# Hopfield from scratch

Code for the video **Become John Hopfield in 16 Minutes**.
You hear three notes of a song and the whole song plays in your head. A computer cannot do that: it needs the address of the file. In 1982 the physicist John Hopfield showed that 100 simple switches joined by wires can: give them a piece of a picture and they hand back the whole picture.
These seven small programs build that machine, find its limit, and follow the 2016 and 2020 repairs to the step inside every modern chatbot. 805 lines of Python 3, standard library only, nothing to install.

```bash
python3 tests.py      # checks every step
./run_all.sh          # runs all seven; expected output is in demo-output.txt
```

| File | Idea | What the run shows |
| --- | --- | --- |
| `net.py` | The machine | 100 switches (a 10 by 10 picture), 4,950 wires, the storing rule and the voting rule. Every step imports it. |
| `step1_recall.py` | Store three pictures, ask one back | Heart, house and face go onto the same wires; each wire ends between -3 and +3. A heart with 25 of 100 squares flipped comes back with 0 squares wrong after one round. With 30 squares flipped it comes back 988 times in 1,000; with 45 flipped, 331 times. |
| `step2_energy.py` | Why it always stops | One number, the energy. The stored pictures sit at -4,954 (heart, house) and -4,994 (face); random states average 7. Over 1,000 random starts and 43,876 flips, 0 flips raised the energy. Every start stopped within 3 rounds. |
| `step3_cut.py` | Cut the wires | With 75% of the wires cut, 899 of 900 damaged pictures still come back whole. With 90% cut, 0 of 900. |
| `step4_ghosts.py` | Memories nobody stored | From 10,000 random starts: 4,073 stop at a stored picture, 4,019 at the negative of one, 1,908 at a blend of all three. A fourth picture that looks like the house (a tree) is changed in 4 squares the moment it is stored. |
| `step5_capacity.py` | How many pictures fit | Over 300 runs the heart comes back whole 267 times with 12 pictures stored, 121 times with 18, 7 times with 27. With 200 and 400 switches the break sits at the same place: between 12 and 16 pictures per 100 switches. |
| `step6_dense.py` | The 2016 repair | The same energy without wires, with the match raised to a power. Power 2 is the old machine (same end state in 200 of 200 starts). Power 4 keeps 1,000 random pictures in 100 switches, 20 of 20 asked back whole; power 2 fails at 30. |
| `step7_attention.py` | The 2020 rule | Shares by the exponential rule, one move. 30,000 random pictures in 100 switches: 20 of 20 asked back whole. The same function with the arguments renamed query, keys and values is the attention step of a transformer: largest difference over 150 cases, 0. |

`save.py` writes each step's numbers to `runs/`, and the animation reads them from there, so every number on screen comes from these runs.
Python 3.9 and 3.12 print the same output for all seven steps.

## What this is not

- A model of memory, not a brain. Real brain cells are not two-state switches, and their connections do not pull equally in both directions.
- Small: 100 switches, pictures of 10 by 10 squares. The capacity tests use random pictures, which are the easy case. Pictures that look alike disturb each other sooner (`step4_ghosts.py`, the tree and the house).
- The edge of 138 pictures per 1,000 switches is from the literature (Hertz, Krogh, Palmer 1991). These runs only show errors starting between 12 and 16 per 100.
- No transformer was trained or run. `step7_attention.py` shows that one function is both the 2020 recall rule and the attention formula. In a real chatbot the keys and values are computed from the words by learned layers; they are not a fixed store of pictures.
- Transformers were not designed from this machine. Attention was published in 2017; the link to Hopfield's network was shown in 2020.

## Sources

- J. J. Hopfield, "Neural networks and physical systems with emergent collective computational abilities", PNAS 79 (8), 1982.
- D. Krotov and J. J. Hopfield, "Dense associative memory for pattern recognition", 2016.
- M. Demircigil and others, "On a model of associative memory with huge storage capacity", 2017.
- H. Ramsauer and others, "Hopfield Networks is All You Need", arXiv 2008.02217, 2020.
- A. Vaswani and others, "Attention Is All You Need", 2017.

MIT licence.
