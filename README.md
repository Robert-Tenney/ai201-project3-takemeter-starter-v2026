# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

This project sorts text from r/touhou, the public subreddit for the Touhou
Project franchise, into four kinds: `analysis` (a point argued from a
specific checkable thing in the games or manga), `hot_take` (a confident
claim with nothing behind it), `request` (asking the community for something
a reply could supply), and `experience` (the writer's own history or feelings
with Touhou). The subreddit is mostly art and memes, so the classifier only
looks at posts and comments that have real text. I chose labels based on what
the text is doing, because the community's own flairs (Help, Fan Discussion,
Game Discussion) were too coarse to separate an argued opinion from a bare
one.

---

## Label Taxonomy

Scope: text in r/touhou. Examples come from Help, Fan Discussion and Game
Discussion posts, and from top-level comments in the Fan Discussion thread
"What touhou opinion would put you in this situation?". Excluded: OC: Art and
Found Fanart, Meme, Video and Cosplay posts (no text), fanfiction chapters,
mod and weekly threads, and ads.

### `analysis`

**Definition:** Makes a point backed by a specific, checkable thing from the
franchise (a game, character, spell card, date, or quote), and the point
depends on it.

**Example 1 (comment):**
> It's less a hard canon fact and a bit more of extrapolation, but Koishi has
> what feels like the biggest evidence of that Spell Card rules aren't as
> foolproof as the community likes to paint them and that you probably can
> loophole abuse. Release of Id and Superego are very similar in structure
> and it's extra notorious because they're almost back to back, only
> separated by a non-spell. They shoot heart-shaped danmaku in sort of
> constantly rotating parabolic trajectories with the individual lanes
> criss-crossing. The main difference being that former is shot outwards (and
> gameplay-wise has hearts pile up at the bottom of screen), while the latter
> "falls" inwards (and has the hearts disappear when they reach their
> target). Even Twilight Frontier seems to have noticed; when she's playable
> in the air fighters they're still separate supers, but her story appearance
> in Hopeless Masquerade just merges them into one Spell Card that alternates
> between the two patterns. [...]

**Example 2 (comment):**
> No, we don't need Mima back; there are several characters who fulfill that
> role in the current canon, including Mizuchi. Continuing with the topic of
> Mizuchi, she, along with the three fairies, would be among the best choices
> for fighting games. Yorihime did win fairly in Silent Sinner in Blue.
> Furthermore, that same manga confirms that the moon rabbits lead normal and
> relatively happy lives, so she's not an abusive slave driver either.

### `hot_take`

**Definition:** A confident claim about Touhou with no support offered, or
with a name or fact that is only decoration.

**Example 1 (comment):**
> The undeniable fact that sakuya sucks

**Example 2 (comment):**
> Fumos are over hyped and many jokes in the fandom suck

### `request`

**Definition:** Asks the community for something a reply could supply, such
as an image, a song, an answer, a recommendation, or an imagined answer to a
what-if.

**Example 1 (post, Help flair):**
> i need help finding old touhou youtube video
> the synopsis is about voodoo doll in eientei, the straw of a kind. reisen
> is targeted somehow. tewi finds it and decide to mess with reisen as usual.
> after some time she had enough and just drop it on the ground i guess and
> accidentally stepped on it, breaking undogein arm. the issue came to
> eirin's light and after that maybe they just prohibits touching it ig. and
> then some wicked shit happens i think. the voodoo or reise started
> attacking tewi i think. the video is old one, mayhaps around the mid 2010s
> . would can see the age in the models and animation. please help me.

**Example 2 (post, Fan Discussion flair):**
> Could touhou cast be able to stop the fall/nyx in persona 3
> I am always wondering when playing persona 3 Could touhou cast able to stop
> the fall/nyx Like how lunarian would react if they moon suddenly crack open
> or how residents of gensokyo would react if they see the moon crack open
> and inside is giant one eye. How would touhou cast react and stop it to
> save they land

### `experience`

**Definition:** Describes the writer's own situation or feelings with Touhou,
without asking for anything or making a claim about the franchise.

**Example 1 (comment):**
> For me EoSD and LoLK are by far my favorite, I'm just biased though.
> Actually I like PCB and IN a lot. PoFV I totally get it. Is it not fair to
> give them a pass for being older?

**Example 2 (comment):**
> I'm just a Reimu(all),Sakuya(fanon) and Yukari(fanon) hater and a
> Yuuka,letty,Seiga lover. that's far from what you're asking.

### The hardest boundary

**Which two labels:** `analysis` vs `hot_take`

**The post that sits between them (comment):**
> Every Touhou game from 10 to 15 is superior in gameplay, characters, story
> and music to every game from Touhou 6 to 9. With EoSD being by far the most
> extremely overrated game in the series and IN being the only one of the
> older windows games that still holds up in most aspects.

**The decision rule I used every time:** [REWORD IN YOUR OWN WORDS. Draft:]
Naming a game is not support. If the point would fall apart without a
specific fact the writer actually cites (a spell card's structure, a manga
event), it's `analysis`, even if the tone is heated. If the names are only
labels on a judgment, it's `hot_take`, even if the tone is calm.

**Other boundaries I hit:** `experience` vs `request`, from the post "WTF is
Touhou how can I stop Touhou from appearing" (a question in the title, but
the body is the writer's own YouTube frustration; I chose `experience`
because a reply could not give the writer anything they asked for). And
`experience` vs `hot_take`, from "Junko is easier than Clownpiece. I can do
Junko in 2 lives with Reisen, Clown took me 4." (the only support is the
writer's own runs).

---

## The Dataset

**Where the posts came from:** r/touhou, public pages only. Posts come from
the Help, Fan Discussion and Game Discussion flairs. Many rows are top-level
comments from the Fan Discussion thread "What touhou opinion would put you in
this situation?", because that is where long text arguments appear. I asked
my TF whether comments count as posts: [ANSWER HERE]. Excluded: art, memes,
video, cosplay, fanfiction chapters, mod threads and ads.

**How I labelled them:** I settled the four definitions with Claude's help (see How I
Used AI), then had Claude pre-label the 25 rows in `labels.csv` from those
definitions, using posts I pasted. Every row's note column says "pre-labelled by
Claude; unverified". None is marked `cold`, so I did not label 20 rows unaided,
and `criteria.md` criterion 4's plan to compare against 20 cold rows could not
be carried out. Three rows are marked as trimmed or partial (two comment
paragraphs left out, one opening sentence to check against the thread), so those
labels rest on incomplete text. <YOU FILL IN: how many of the 25 you read and
changed, or say you changed none.>

**Counts per label (all 25 rows):**

| Label | Count | Share |
|---|---|---|
| `hot_take` | 11 | 44% |
| `analysis` | 5 | 20% |
| `experience` | 5 | 20% |
| `request` | 4 | 16% |
| **Total** | **25** | 100% |

These are the final counts for this submission. They are well short of the 200
rows and the mix (`hot_take` 90, `request` 40, `experience` 40, `analysis` 30)
planned in `criteria.md`, which is why criterion 3 is missed.

**Three hard cases**

**1.**
> *The post:* "Every Touhou game from 10 to 15 is superior in gameplay,
> characters, story and music to every game from Touhou 6 to 9. With EoSD
> being by far the most extremely overrated game in the series..."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose `hot_take`, because:* it names specific games, but the names are
> labels on a judgment. Nothing in the comment (a mechanic, a stat, a scene)
> would let a reader check the claim, so the games are decoration.

**2.**
> *The post:* "WTF is Touhou how can I stop Touhou from appearing..."
>
> *Could have been:* `experience` or `request`
>
> *I chose `experience`, because:* the body is the writer's own YouTube
> recommendations and frustration. The title sounds like a question, but the
> post doesn't ask for anything a reply could supply.

**3.**
> *The post:* "Junko is easier than Clownpiece. I can do Junko in 2 lives
> with Reisen, Clown took me 4."
>
> *Could have been:* `experience` or `hot_take`
>
> *I chose `experience`, because:* the only support is the writer's own
> runs, which makes it a report of their play. [REWORD: say what you would
> do if a reply argued it as a general claim about the game.]

---

## The Training Run

**Base model:** `distilbert-base-uncased` (the notebook default).

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per
post, seed 42.

**Anything I changed from the defaults, and why:** I did not change any
training setting. The only notebook edit was the `LABELS` list, set to
`["analysis", "hot_take", "request", "experience"]` to match `labels.csv`,
plus my name and email in section 1.

One thing I am watching rather than changing: 128 tokens truncates long
posts. My `analysis` examples are among my longest comments, several a few
hundred words, so the model may only see the opening of them. If `analysis`
recall is low in the next unit, truncation is a cause to check before
blaming the labels.

**Split sizes:** `labels.csv` has 25 rows, so the notebook's stratified 70/15/15
split gives 17 train / 4 validation / 4 test at seed 42. Per-label counts
(reproduced with the notebook's `split_dataset` function, and the test posts
match `test_split.csv`):

| Label | Train | Validation | Test | Under the notebook's threshold of 8 in test? |
|---|---|---|---|---|
| `analysis` | 3 | 1 | 1 | yes |
| `experience` | 3 | 1 | 1 | yes |
| `hot_take` | 8 | 1 | 2 | yes |
| `request` | 3 | 1 | 0 | yes |

All four labels are under the threshold, and `request` has no test posts at all,
so its F1 cannot be measured. This is far from the 140 / 30 / 30 split I planned
for 200 rows, and it explains most of the variance in the unit 6 results.

**Device:** `cpu` (device name `CPU`), torch 2.14.1+cpu, `max_length` 128, from
`results.json`. Two runs on the same data and seed can differ across hardware
because the arithmetic runs in a slightly different order, so the device is part
of the result.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I pasted real r/touhou posts and comments and asked
  Claude to draft a label taxonomy from them and find one real example per
  label.
- *What came back:* A draft set of labels with one-sentence definitions, and
  a proposed decision rule for the `analysis` vs `hot_take` boundary. The
  final four labels (`analysis`, `hot_take`, `request`, `experience`) came
  after the second moment below.
- *What I changed:* [YOU FILL IN: which definitions or examples you edited,
  and how you reworded the decision rule.]

**Moment 2**

- *What I asked for:* I pasted the r/touhou front page feed and asked Claude
  to find a real post for each of my draft labels.
- *What came back:* Claude sorted the text-bearing posts and reported that
  none of them argued from a checkable fact or made a bare claim about the
  franchise, so my `analysis` and `hot_take` labels had no real examples in
  that feed. Two of the three real text posts fit no label at all. It also
  pointed out that most of the feed was image-only.
- *What I changed:* I stopped assuming `analysis` and `hot_take` existed and
  went looking for them. I pasted a long Fan Discussion opinion thread, where
  both appeared, and used Claude's list of the real examples there. I also
  overrode Claude's three-label draft: I asked for `analysis` and `hot_take`
  to be kept alongside `request` and `experience`, so Claude folded its
  `speculation` label into `request`. Claude's labels for the examples are
  its judgment; I am treating them as pre-labels to read and correct, not as
  final.


<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

## Baseline vs. Trained

### Setup

- **Baseline model:** `facebook/bart-large-mnli`, zero-shot, run locally on CPU
  with `python baseline.py`. Its only input is the four definitions in
  `label_definitions.txt`, copied from the Label Taxonomy section above. No
  training, no examples.
- **Scored on:** `test_split.csv`, the held-out split the notebook wrote in
  unit 5. It has **4 posts** (2 `hot_take`, 1 `experience`, 1 `analysis`, 0
  `request`), because `labels.csv` currently has only 25 rows. The baseline
  and the trained model are scored on the same 4 posts, so the comparison is
  like-for-like, but 4 posts is far too few to measure anything with. One
  post is 25 points of accuracy.
- **Trained model:** the unit 5 fine-tune (`distilbert-base-uncased`, seed 42,
  CPU), numbers from `results.json`.
- **Earlier run, not used:** my first baseline run happened before
  `test_split.csv` existed, so it scored a random sample of all 25 rows
  (accuracy 0.320). That run is not comparable with the trained model and is
  not in the table below.

### Prediction (written before I saw any Trained numbers)

I predict the trained model will beat the baseline most on `hot_take`. My
definition of it depends on what is absent (no support offered), which a
zero-shot model reads poorly, and my training data shows what unsupported
claims actually look like. I expect the gap to be smallest on `request`,
which has surface cues like questions and "can someone".

### Results

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.250 | 0.500 | +0.250 |
| Macro F1 | 0.100 | 0.222 | +0.122 |
| F1 — `analysis` | 0.400 | 0.000 | -0.400 |
| F1 — `experience` | 0.000 | 0.000 | +0.000 |
| F1 — `hot_take` | 0.000 | 0.667 | +0.667 |
| F1 — `request` | 0.000 | 0.000 | +0.000 |

Posts per label in the held-out set: `analysis` 1, `experience` 1,
`hot_take` 2, `request` 0.

### What the gap means

On accuracy and macro F1 the trained model is ahead, and the biggest gap is
on `hot_take` (+0.667), which is where I predicted it. But the table
overstates what happened. The trained model called all 4 posts `hot_take`
(its confusion row shows the `experience` and `analysis` posts both going
there), and `hot_take` is 2 of the 4 held-out posts, so its 0.500 accuracy is
what always guessing the biggest label would score. The baseline did the
mirror image: it called all 4 posts `analysis`, which got the one real
`analysis` post right and nothing else. So neither model separated the
labels on this set, and the gap shows which single label each one defaulted
to, not that training taught the model anything. `request` has no posts in
the held-out set, so its row says nothing about the model, and my "smallest
gap on `request`" prediction cannot be checked.

The real finding is the size of the data. With 25 labelled rows, the
held-out set is 4 posts, and no comparison on it can be trusted. I need
`labels.csv` at 150 to 200 rows, then a retrain and a rerun of the baseline
on the new `test_split.csv`, before this table means anything.

### What my definitions were worth

I ran the baseline a second time with bare label names instead of my
definitions (`python baseline.py --definitions nonexistent.txt --out
baseline_bare.json`, which falls back to the label names alone). Both runs scored
the same 4 held-out posts.

| Measure | With my definitions | Bare label names | Difference |
|---|---|---|---|
| Overall accuracy | 0.250 | 0.250 | +0.000 |
| Macro F1 | 0.100 | 0.125 | -0.025 |
| F1 `analysis` | 0.400 | 0.000 | +0.400 |
| F1 `experience` | 0.000 | 0.000 | +0.000 |
| F1 `hot_take` | 0.000 | 0.500 | -0.500 |
| F1 `request` | 0.000 | 0.000 | +0.000 |

On accuracy my definitions were worth nothing (0.250 both ways), and on macro F1
they were slightly worse (0.100 against 0.125). The definitions changed which
label the baseline defaulted to, not how well it did: with them it called all 4
posts `analysis`, and with bare names it got one of the two `hot_take` posts
right but lost the `analysis` post. With 4 test posts, one post is 25 points of accuracy, so I read
this as "no measurable difference", not as evidence the definitions are bad. The
baseline table above is the run with definitions.

---

## Run Log — Before

### Three seeds, before any improvement

Run from notebook section 6 with `RUN_LABEL = "before"`. Numbers are copied from
`results_three_seeds_before.json`.

**Device:** `cpu` (CPU), torch 2.14.1+cpu, `max_length` 128. Recorded in every
row of the JSON file.

| Seed | Test posts | Accuracy | Macro F1 | F1 `analysis` | F1 `hot_take` | F1 `request` | F1 `experience` | Recall `analysis` |
|---|---|---|---|---|---|---|---|---|
| 42 | 4 | 0.500 | 0.222 | 0.000 | 0.667 | 0.000 | 0.000 | 0.000 |
| 7 | 4 | 0.250 | 0.167 | 0.000 | 0.500 | 0.000 | 0.000 | 0.000 |
| 2024 | 4 | 0.500 | 0.222 | 0.000 | 0.667 | 0.000 | 0.000 | 0.000 |

Every seed's test split has the same shape: 2 `hot_take`, 1 `analysis`,
1 `experience`, 0 `request`. `request` has no test posts, so its F1 of 0.000
is a placeholder from the scoring code, not a measurement.

**Spread:** accuracy ranges from 0.250 to 0.500, a 25-point swing, well over
the ten points the notebook warns about. With 4 test posts, one post is 25
points, so the swing is a single post moving between right and wrong. That is a
diagnosis in itself: `labels.csv` has 25 rows, which is too small for a stable
measure.

**Confidence (a second sign the model has barely learned):** the model's
average confidence is 0.29 to 0.33 on every seed, and about the same on right
and wrong answers (seed 42: 0.296 right, 0.295 wrong). With four labels, a
model with no idea is near 0.25, so these guesses are close to uniform.

### Criteria table

Targets are the originals from `criteria.md`, unchanged. Values are from
`results_three_seeds_before.json`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | >= 0.60 on every seed | 0.500 | 0.250 | 0.500 | MISSED |
| 2. Every label F1 (`analysis` >= 0.40, others >= 0.50) | all labels, every seed | `analysis` 0.000, `hot_take` 0.667, `request` 0.000, `experience` 0.000 | `analysis` 0.000, `hot_take` 0.500, `request` 0.000, `experience` 0.000 | `analysis` 0.000, `hot_take` 0.667, `request` 0.000, `experience` 0.000 | MISSED |
| 3. No label > 60% of `labels.csv`; smallest label >= 25 examples | both parts | largest 44%, smallest 4 | same (a property of `labels.csv`, not of a seed) | same | MISSED |
| 4. Agreement with staff >= 70% (21 of 30) | one set of 30 posts | 30 of 30 (100%) | not seed-based | not seed-based | MET |
| 5. Recall on `analysis` >= 0.50 on every seed | every seed | 0.000 | 0.000 | 0.000 | MISSED |

### Confusion matrix

Seed 42 (the matrix section 7 prints). Rows are true labels, columns are the
model's guesses.

| true \ predicted | analysis | hot_take | request | experience |
|---|---|---|---|---|
| **analysis** | 0 | 1 | 0 | 0 |
| **hot_take** | 0 | 2 | 0 | 0 |
| **request** | 0 | 0 | 0 | 0 |
| **experience** | 0 | 1 | 0 | 0 |

**My biggest off-diagonal number, and what it means:** The largest wrong cell
is 1, tied between `analysis` called `hot_take` and `experience` called
`hot_take`, so there is no single biggest confusion. What the matrix does show
is that the model called all 4 posts `hot_take`: its whole `hot_take` column is
full and every other column is empty. That is a model defaulting to the biggest
label, not learning the `analysis`/`hot_take` boundary. Seed 7 differs (one
`hot_take` post and the `analysis` post both went to `experience`), but it
still never predicted `analysis` or `request`.

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | >= 0.60 on every seed | MISSED | 0.500, 0.250, 0.500. All three are under 0.60, and the target had to hold on every seed. |
| 2 | Every label F1 | >= 0.50 each, `analysis` >= 0.40, every seed | MISSED | Three of four labels scored 0.000 on all three seeds. Only `hot_take` was above 0 (0.667, 0.500, 0.667), and it met its 0.50 line on every seed. See the note below. |
| 3 | Label balance | no label > 60%; smallest >= 25 | MISSED | The largest label is `hot_take` at 44%, which passes. The smallest label is `request` with 4 examples, far under 25, so the second part fails. |
| 4 | Agreement with staff | >= 70% (21 of 30) | MET | 30 of 30 matched staff (100%), against a target of 21. |
| 5 | Recall on `analysis` | >= 0.50 on every seed | MISSED | Recall was 0.000 on all three seeds. The model never predicted `analysis`. |

**Diagnoses**

**Criterion 2: note on `hot_take`.** On seed 7, `hot_take` F1 was 0.500, which
meets the 0.50 line exactly. The criterion still fails because the other three
labels scored 0.000. Separately, `request` had no posts in any test split, so
its 0.000 is a placeholder from the scoring code and not a measurement of the
model. This criterion could not be properly tested on this data. I am leaving
the verdict as MISSED because the other two labels with test posts also scored
0.000.

**Criteria 1, 2 and 5: too few examples, and the model barely trained.**
`labels.csv` has 25 rows. The notebook's 70/15/15 split gives about 17 train,
4 validation and 4 test posts. Evidence:
- The confusion matrix (seed 42) shows all 4 test posts predicted `hot_take`.
  The `analysis` and `experience` posts both went there, and nothing was ever
  predicted as `analysis` or `request`.
- Average confidence was 0.29 to 0.33 on every seed, and the same on right and
  wrong answers (seed 42: 0.296 vs 0.295). With four labels, a model with no
  idea sits near 0.25, so its guesses were close to uniform.
- With about 17 training rows and a batch size of 16, three epochs is about 6
  training steps in total. That is not enough for the model to learn four
  labels.
- Accuracy swung 25 points between seeds (0.250 to 0.500), but each of the 4
  test posts is worth 25 points, so that swing is one post. This is the
  dataset being too small for a stable measure.

I cannot separate "my labels are inconsistent" from "too little data" with
this run. The agreement report is the evidence for that, and see below.

**Criterion 3: too few examples, by my own plan.** My plan was 200 posts with
`analysis` smallest at about 30. The real file has 25 rows, and the smallest
label is `request` at 4, not `analysis`. This is the same cause as above:
I collected 25 of the 200 rows I planned. Criterion 2's wording also assumes
`analysis` is the smallest label, which is not true of the data I have. That
is a mismatch between my plan and my data, not a broken criterion, so I am not
revising it.

**Criterion 4:** Met, so there is nothing to diagnose as a miss. I matched
staff on all 30 posts, including the 7 staff marked as borderline. What it does
and does not tell me: it shows I can apply a written `analysis` / `hot_take` /
`reaction` rule consistently, so my misses on criteria 1, 2 and 5 are not
explained by me being loose with a written rule. It does not show that Claude's
pre-labels on my own 25 rows are right or consistent, because I did not label
those. So it rules out one cause of the misses without confirming my own labels.

**Evidence from the baseline that bears on the boundary:** the zero-shot
baseline called 10 of 11 `hot_take` posts `analysis` on the 25-post fallback
run. That points at the `analysis` / `hot_take` boundary being hard to read
from the definition alone, which fits my "hardest boundary" section. It is
only one run on the fallback sample, so I treat it as a lead, not a finding.

**Which criteria are broken rather than missed:** none. Every criterion was
measurable and I got a number for each, so I have not revised any.

---

## Agreement Report

**Staff taxonomy:** `analysis`, `hot_take`, `reaction`, applied under the
definitions and decision rules in `data/staff_taxonomy.md` (not my own
taxonomy). I labelled all 30 posts myself, and `agreement.py` then compared
my file with the staff labels. <YOU CONFIRM: whether you labelled before seeing
the staff labels, and when `my_staff_labels.csv` was committed. Keep only what
is true.>

**Agreement rate:** 30 / 30 = 100%

My target in `criteria.md` (criterion 4) was at least 70% (21 of 30). Met.

**Disagreements:** none, so there is nothing to adjudicate. `agreement.py` listed
no disagreements and wrote `agreement_results.json`.

**Was the set easy, or is the rule tight?** The staff file marks 7 of the 30
posts as borderline (`sp_005`, `sp_010`, `sp_014`, `sp_019`, `sp_020`, `sp_028`,
`sp_029`), and I matched staff on all 7. The taxonomy says a rate in the 70s is
normal because posts were picked for ambiguity, so 100% is above what staff
expected. <YOU FILL IN, in your own words and honestly: which of the 7 borderline
posts you hesitated on, and which numbered rule (1 to 4) settled each one. Say
that you labelled all 30 before seeing `staff_labels.csv`, if that is true, and
whether you read the staff file's `why` column before or after labelling.>

**Counts by pile:** not applicable, since there are no disagreements.

**What this tells me about my labels:** Matching on all 30 shows I apply a
written rule the way its authors did. It is the only instrument I had for
telling a labelling problem from a model problem, and here it points away from
my own application of a written rule. It does not cover my 25 training rows,
which Claude pre-labelled, so I cannot use it to say those labels are
consistent.

**A limit on this check:** my own `labels.csv` rows were pre-labelled by
Claude and none is marked `cold`, so I cannot compare this rate against my own
cold labels as `criteria.md` planned.

---

## The Improvement

**What I changed:** One training setting: `EPOCHS` in notebook section 2, from
3 to 15. Nothing else. Labels, taxonomy, criteria, `labels.csv`, learning rate
(2e-5), batch size (16), `MAX_LENGTH` (128) and the three seeds (42, 7, 2024)
are the same as in the before run. Because `labels.csv` and the seed are
unchanged, `test_split.csv` is unchanged too, so the before and after runs are
scored on the same test posts, and so is the baseline.

**Which diagnosis pointed at it:** My diagnosis for criteria 1, 2 and 5 was
that the model barely trained. With about 17 training rows and a batch size of
16, three epochs is about 6 training steps. The model's confidence was 0.29 to
0.33 on every seed and the same on right and wrong answers, which is close to
the 0.25 of a model guessing among four labels, and it predicted `hot_take` for
every test post on seed 42. Training longer is the one change that addresses
that cause directly. I did not pick "add examples" or "relabel a boundary"
because the first would change `test_split.csv` and break the comparison with my
baseline, and the second had nothing to point at: my agreement check found no
disagreements, so it named no boundary that I applied two ways.

**What I expect:** More epochs should raise confidence and spread predictions
across labels. It may not fix criterion 3, which is about how many examples I
have, not how long I trained. If accuracy rises but only because the model now
memorises its 17 training rows, the validation numbers and the confusion matrix
should show that.

**How I ran it:** I changed `EPOCHS` from 3 to 15 in the notebook's settings
cell (section 2), set `RUN_LABEL = "after"` in section 6, and ran section 6. It
wrote `results_three_seeds_after.json`. `results_three_seeds_before.json` is
untouched. I ran section 6 twice, and both runs wrote the same numbers.

**What went wrong with the test:** the after file is identical to the before
file. All three seeds match on accuracy, every per-label F1, the confusion
matrices and the confidence values (for example seed 42 mean confidence when
right is 0.29601359367370605 in both). The notebook is deterministic for a given
seed and settings, and 15 epochs would have changed those numbers, so these
results are what 3 epochs produces. I could not confirm that `EPOCHS = 15` was
in effect when section 6 ran. Section 6 reads `EPOCHS` from the kernel's
memory, so editing the value without re-running the settings cell would leave it
at 3. <YOU FILL IN: what you did to check, for example the settings line the
notebook printed (`... 15 epochs ...` or `... 3 epochs ...`).>

### Run Log — After

Numbers are from `results_three_seeds_after.json`. Device: `cpu`, torch
2.14.1+cpu.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | >= 0.60 on every seed | 0.500 | 0.250 | 0.500 | MISSED |
| 2. Every label F1 (`analysis` >= 0.40, others >= 0.50) | all labels, every seed | `analysis` 0.000, `hot_take` 0.667, `request` 0.000, `experience` 0.000 | `analysis` 0.000, `hot_take` 0.500, `request` 0.000, `experience` 0.000 | `analysis` 0.000, `hot_take` 0.667, `request` 0.000, `experience` 0.000 | MISSED |
| 3. No label > 60%; smallest >= 25 | both parts | largest 44%, smallest 4 | same | same | MISSED (unchanged, a property of `labels.csv`) |
| 4. Agreement with staff >= 70% | one set of 30 posts | 30 of 30 (100%) | not seed-based | not seed-based | MET (unchanged) |
| 5. Recall on `analysis` >= 0.50 on every seed | every seed | 0.000 | 0.000 | 0.000 | MISSED |

### Before and after, side by side

| Measure | Before: 42 / 7 / 2024 | After: 42 / 7 / 2024 |
|---|---|---|
| Accuracy | 0.500 / 0.250 / 0.500 | 0.500 / 0.250 / 0.500 |
| Macro F1 | 0.222 / 0.167 / 0.222 | 0.222 / 0.167 / 0.222 |
| Mean confidence when right (seed 42) | 0.296 | 0.296 |
| Recall `analysis` | 0.000 / 0.000 / 0.000 | 0.000 / 0.000 / 0.000 |

**Did it help, and how do I know:** No, and it also was not a valid test. Every
number is the same as before, which means the change did not take effect, not
that training for longer does nothing. So I have no evidence either way on
whether more epochs would help. My diagnosis (about 6 training steps on 17 rows,
confidence near 0.25) still points at training, and the next step would be to
confirm the settings cell printed `15 epochs`, re-run section 6, and compare. I
stopped here because I ran out of time to find why the setting did not apply.
<Edit if that is not the reason.>

---

## What's Still Broken

Four of my five criteria are missed and criterion 4 is met, in both the before
and the after run (the two runs are identical). For each one: what I would do,
and why I stopped.

**Criterion 1 (accuracy >= 0.60 every seed):** Missed before (0.500, 0.250,
0.500). *After the change:* Missed (0.500, 0.250, 0.500, identical to before, so the change did not apply). What I
would do next: label more rows. The measure is a 4-post test set, where one post
is 25 points, so no training change can make this number stable. I stopped
because labelling 150 to 200 rows by hand, with care, did not fit this unit, and
it would also have changed `test_split.csv` and broken the like-for-like
comparison with my baseline.

**Criterion 2 (every label F1):** Missed before (three labels at 0.000 on every
seed). *After the change:* Missed, identical to before (three labels at 0.000 on every seed). What I
would do next: add `request` examples first, because it is my thinnest label.
`request` has no posts in the test split, so its F1 cannot be measured until it
has more examples (it has 4 in `labels.csv`). I stopped for the same reason as
criterion 1.

**Criterion 3 (label balance, smallest >= 25):** Missed, and unchanged by
training. `labels.csv` has 25 rows and the smallest label has 4. The only fix is
collecting and labelling more posts. I stopped because that is the work of
unit 5, not a change I could make and measure in this unit.

**Criterion 4 (agreement with staff >= 70%):** Met at 30 of 30. Nothing left to
fix here. The check does not cover my 25 pre-labelled rows, which is the part I
would audit next.

**Criterion 5 (recall on `analysis` >= 0.50 every seed):** Missed before (0.000
on every seed). *After the change:* Missed (0.000 on every seed, identical to before).
What I would do next: my baseline called 10 of 11 `hot_take` posts `analysis`,
and my model never predicted `analysis`, so the two models fail that boundary in
opposite directions. My staff check showed I can apply a written `analysis` /
`hot_take` rule consistently, so I would first reread the 5 `analysis` and 11
`hot_take` pre-labels in `labels.csv` against my own rule, then add `analysis`
examples. I stopped because 5 `analysis` rows (about 1 in the test split) cannot
support any conclusion about that boundary.

**The gap between what I meant my labels to capture and what the model
learned:** I meant `analysis` to be an argument that depends on a specific,
checkable fact, `hot_take` a claim with nothing behind it, `request` something a
reply could supply, and `experience` the writer's own situation. In the before
run the seed 42 confusion matrix shows the model called all 4 test posts
`hot_take`, the biggest label, so it learned the shape of my data and not these
four ideas. *After the change:* the after-run matrix is the same as the before one, so
this still holds, but I could not test whether more training would change it.

**Anything I would not trust in these results:** every number comes from a
4-post test set on 25 labelled rows, and all 25 rows were pre-labelled by
Claude from my definitions, so even a perfect score would measure agreement with
those pre-labels and not with a human standard. The staff agreement check
measures how I apply someone else's rules, not whether those pre-labels are
right.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

---

## Capstone

**The System**

TakeMeter, project 3 in this repo. It sorts r/touhou text into `analysis`,
`hot_take`, `request` and `experience`. The path I am extending is
`labels.csv` -> stratified 70/15/15 split -> fine-tuned
`distilbert-base-uncased` -> `results.json`. I am extending this same
repository, not a copy, so the extension sits next to the original work.

**The Shape**

Shape B, harden against failure. TakeMeter works when its input is clean, and
several of its failures are silent. Today `check_dataset` in the notebook
prints `[FIX ME]` lines, but the next cell trains anyway. `split_dataset`
quietly drops stratification when a label has fewer than 2 rows. A missing
file or column ends in a raw traceback. I am adding one failure-handling layer
in front of training: a validation gate (`guard.py`, called before the split)
that checks the file, the columns, empty text, labels not in `LABELS`,
duplicates, and rows per label. It either passes or stops with a one-line,
named reason. Every refusal and every pass writes a structured log record.
When I am finished I will claim two things: bad input is refused with a clear
reason and a log entry, and good input still trains exactly as it did before.

**What's Out of Scope**

- Collecting or relabelling more rows. `labels.csv` is too small, but that is
  the project 3 problem, not this unit's extension.
- Changing the model, the training settings or `EPOCHS`.
- Saving the model or adding a predict/serving endpoint. That would be Shape C.
- Touching `baseline.py` or `agreement.py`, including baseline's silent
  fallback to a random sample when `test_split.csv` is missing.
- Hosting it. I plan to run it locally (Path B).

**The Run Path**

Path B, local with logs. The start command is `python run.py`, documented in
`RUNNING.md` with the environment it needs. I chose Path B because the system
carries a local model (`distilbert-base-uncased`, about 270 MB), which does not
fit on a free 512 MB host. `run.py` is new in this unit. It runs the gate, then
the same split, training settings and scoring as the notebook, then writes one
log record. I tested the instructions on myself: I cloned the repo into a new
folder and followed `RUNNING.md` from the top. It worked the first time, and
nothing was missing from the instructions.

**Instrumentation**

Every run appends one JSON line to `run_log.jsonl` with named fields:
`timestamp`, `input` (data file, seed, labels, rows), `output` (status, code,
message, and on success accuracy, macro F1, test size and device),
`duration_ms` and `stages_ms`. The gate also writes its own line to
`guard_log.jsonl` for every check. Refused and crashed runs leave records too.

Ten successful runs, from `python run.py --runs 10`, copied unedited from
`run_log.jsonl`:

```jsonl
{"run": 1, "timestamp": "2026-11-12T21:06:14+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 18077.9, "stages_ms": {"validate": 361.9, "train_and_score": 17716.0}}
{"run": 2, "timestamp": "2026-11-12T21:06:32+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5697.6, "stages_ms": {"validate": 4.4, "train_and_score": 5693.2}}
{"run": 3, "timestamp": "2026-11-12T21:06:37+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5880.5, "stages_ms": {"validate": 3.5, "train_and_score": 5877.0}}
{"run": 4, "timestamp": "2026-11-12T21:06:43+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5944.8, "stages_ms": {"validate": 3.7, "train_and_score": 5941.0}}
{"run": 5, "timestamp": "2026-11-12T21:06:49+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5553.6, "stages_ms": {"validate": 3.5, "train_and_score": 5550.0}}
{"run": 6, "timestamp": "2026-11-12T21:06:55+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5542.6, "stages_ms": {"validate": 3.4, "train_and_score": 5539.1}}
{"run": 7, "timestamp": "2026-11-12T21:07:00+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5610.0, "stages_ms": {"validate": 3.3, "train_and_score": 5606.7}}
{"run": 8, "timestamp": "2026-11-12T21:07:06+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5566.9, "stages_ms": {"validate": 3.4, "train_and_score": 5563.4}}
{"run": 9, "timestamp": "2026-11-12T21:07:12+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5651.9, "stages_ms": {"validate": 3.5, "train_and_score": 5648.3}}
{"run": 10, "timestamp": "2026-11-12T21:07:17+00:00", "input": {"data": "labels.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128, "rows": 25}, "output": {"status": "ok", "code": null, "message": "trained and scored", "accuracy": 0.5, "f1_macro": 0.2222, "n_train": 17, "n_test": 4, "device": "cpu"}, "duration_ms": 5696.5, "stages_ms": {"validate": 3.6, "train_and_score": 5692.9}}
```

One failed run, from `python run.py --data nope.csv`, copied unedited. It was
refused by the gate and still left a record. The `run` field is 1 because it
was its own invocation:

```jsonl
{"run": 1, "timestamp": "2026-11-12T21:21:21+00:00", "input": {"data": "nope.csv", "seed": 42, "labels": ["request", "experience", "hot_take", "analysis"], "epochs": 3, "max_length": 128}, "output": {"status": "refused", "code": "file_missing", "message": "No file at nope.csv."}, "duration_ms": 350.9, "stages_ms": {}}
```

All ten runs agree on the result: accuracy 0.5 and macro F1 0.2222 every time,
with 17 training posts and 4 test posts. That matches `results.json` from the
notebook (accuracy 0.500, macro F1 0.222), so the gated script reproduces the
original system and did not change it. Only the timing differed. Run 1 took
18,078 ms and runs 2 to 10 took between 5,543 and 5,945 ms. In run 1 the
`validate` stage took 361.9 ms against about 3.5 ms in later runs, and
`train_and_score` took 17,716 ms against about 5,600 ms. I did not measure why,
but this is the first run in a fresh process, so the likely cause is one-time
work such as loading libraries and the model, which later runs in the same
process reuse. That is a guess, not a finding.

**What It Costs**

This system calls no hosted API, so there is no spend per run. The real cost is
compute time, and I measured that instead of estimating it. I ran
`python run.py --runs 10` on the device below, which logged `duration_ms` for
each run, and took the mean of the ten. I also checked the mean in PowerShell
with `Measure-Object -Average -Minimum -Maximum` on the `duration_ms` values,
and it gave the same 6,922 ms.

| Measure | Value |
|---|---|
| Device | `cpu` (the `device` field in the run log) |
| Mean seconds per run, all ten runs | 6.92 s (6,922 ms) |
| Mean seconds per run, runs 2 to 10 only | 5.68 s (5,683 ms) |
| Min / max seconds | 5.54 s (run 6) / 18.08 s (run 1) |
| Cost in dollars | $0.00, no hosted API is called |

The mean of all ten is the cost number I am reporting, because run 1 is a real
run that a person starting the script would pay for. The 5.68 s figure is what
a repeat run costs once the process is warm, so it is the number to use for
back-to-back runs. Run 1 is about three times slower than the rest, which pulls
the mean up by about 1.2 s.

[Milestone 7 adds the hundred-people-a-day sentence with the arithmetic.]

**Run Log**

Five criteria from `criteria.md`, three separate trials each, nothing changed
between trials. Each trial is one invocation of `python capstone_test.py
--trial N`. The measurements and how I read each criterion are written at the
top of `capstone_test.py`, which was committed before any trial was run. The
table below is the output of `python capstone_test.py --report`. Real output
from every trial is in `capstone_results/`.

Device: `cpu`, the same machine as the Milestone 3 run log. Each trial's
`timing/run_log.jsonl` records the `device` field, and
`capstone_results/trial_1/summary.json` records the Python version and platform.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. At least 75% of 100 bad inputs blocked | >= 75 of 100 | 88/100 | 88/100 | 88/100 | MET |
| 2. Every bad-input run logged, completely | 100 of 100 complete, none missing | 100/100 complete, 100 records | 100/100 complete, 100 records | 100/100 complete, 100 records | MET |
| 3. Original still works (seed 42, vs results.json) | accuracy 0.5, macro F1 0.2222 | acc 0.5, F1 0.2222 | acc 0.5, F1 0.2222 | acc 0.5, F1 0.2222 | MET |
| 4. At least 90% of 100 good inputs pass | >= 90 of 100 | 100/100 | 100/100 | 100/100 | MET |
| 5. Run 1 <= 8 s and runs 2-10 <= 2 s | all of runs 2-10 under 2.0 s | first 17.33s, rest max 5.47s | first 17.29s, rest max 5.12s | first 16.71s, rest max 5.82s | MISSED |

How I read the criteria that had no number or definition. These were chosen
before running, and are written in `capstone_test.py`:

- Criterion 1: "blocked" means the run finished with status `refused`. A file
  that gets past the gate does not count, even if it later crashes.
- Criterion 2: "properly logged" means exactly one complete record per input in
  `run_log.jsonl` (timestamp, input, output with a status and message, a code on
  every refused or errored run, and `duration_ms`), and one record per input in
  `guard_log.jsonl`.
- Criterion 3: "still works" means the gate returns the DataFrame unchanged, and
  `python run.py` on `labels.csv` at seed 42 reproduces the notebook's
  `results.json` (accuracy 0.5, macro F1 0.2222, 4 test posts).
- Criterion 5: I used the upper end of each range in the criterion as the
  threshold. Run 1 at 8 seconds or less, and every one of runs 2 to 10 at 2
  seconds or less, in one process.

What the 100 bad and 100 good inputs were. 84 of the bad inputs are kinds the
gate checks for (missing file, empty file, wrong columns, header only, blank
text, blank label, unknown label, duplicates, a label with fewer than 3 rows,
one label over 70%, an unreadable file). 16 are kinds it has no check for on
purpose, so the 75% target could be missed: 6 near-duplicates that differ only
by case, 6 posts that are only punctuation, and 4 paths that are folders.
The 100 good inputs are 10 kinds, 10 files each: plain, Windows line endings,
a byte-order mark, commas and line breaks inside a post, non-English text, an
extra column, columns in the other order, very long posts, the smallest valid
file (12 rows) and a large file (300 rows). All files are generated per trial
from a seed, so each trial gets different files with the same mix.

Real output from trial 1, copied from `python capstone_test.py --report`. The
file and function that produced each part are named above it.

Criterion 1, from `run.py` `run_once` and `guard.py` `validate_dataset`. Columns
are the kind of bad input, whether the gate has a check for it, blocked out of
attempted, the refusal codes, and every status seen:

```
  file_missing             yes  8/8   {'file_missing': 8}   {'refused': 8}
  file_empty               yes  8/8   {'file_empty': 8}   {'refused': 8}
  columns_missing          yes  8/8   {'columns_missing': 8}   {'refused': 8}
  no_rows                  yes  8/8   {'no_rows': 8}   {'refused': 8}
  empty_text               yes  8/8   {'empty_text': 8}   {'refused': 8}
  label_blank              yes  8/8   {'label_blank': 8}   {'refused': 8}
  label_unknown            yes  8/8   {'label_unknown': 8}   {'refused': 8}
  duplicates               yes  8/8   {'duplicates': 8}   {'refused': 8}
  label_too_thin           yes  8/8   {'label_too_thin': 8}   {'refused': 8}
  label_dominant           yes  8/8   {'label_dominant': 8}   {'refused': 8}
  file_unreadable          yes  4/4   {'file_unreadable': 4}   {'refused': 4}
  near_duplicates          NO   0/6   {}   {'ok': 6}
  punctuation_only_text    NO   0/6   {}   {'ok': 6}
  directory_not_file       NO   4/4   {'file_empty': 4}   {'refused': 4}
  blocked 88 of 100; 0 of those refused as 'unexpected'
```

Criterion 2, from `run.py` `run_once` (`run_log.jsonl` and `guard_log.jsonl`):

```
{'attempted': 100, 'run_log_records': 100, 'run_log_unreadable_lines': 0, 'complete_records': 100, 'guard_log_records': 100, 'guard_log_unreadable_lines': 0, 'every_input_logged_once': True}
```

Criterion 3, from `run.py` `train_and_score` and `results.json`:

```
{
  "reference_results_json": {
    "accuracy": 0.5,
    "f1_macro": 0.2222,
    "n_test": 4
  },
  "run_py_result": {
    "status": "ok",
    "accuracy": 0.5,
    "f1_macro": 0.2222,
    "n_test": 4,
    "n_train": 17,
    "message": "trained and scored"
  },
  "gate_returns_frame_unchanged": true,
  "run_py_exit_code": 0,
  "run_py_matches_results_json": true
}
```

Criterion 4, from `guard.py` `validate_dataset`. Passed out of 10 for each kind:

```
  plain                            10/10
  crlf_line_endings                10/10
  utf8_bom                         10/10
  commas_quotes_newlines_in_text   10/10
  unicode_text                     10/10
  extra_column                     10/10
  columns_in_other_order           10/10
  very_long_text                   10/10
  smallest_valid_file              10/10
  large_file                       10/10
```

Criterion 5, from `run.py` `main` with `--runs 10`. Seconds per run, trial 1:

```
[17.33, 5.26, 5.27, 4.88, 5.47, 4.9, 4.84, 4.93, 5.03, 5.35]
```

Per-trial values, so the spread is visible:

```
trial 1: c1 88  c2 100  c3 0.5  c4 100  c5 [17.33, 5.26, 5.27, 4.88, 5.47, 4.9, 4.84, 4.93, 5.03, 5.35]
trial 2: c1 88  c2 100  c3 0.5  c4 100  c5 [17.29, 5.05, 4.92, 4.61, 4.68, 5.03, 4.98, 5.12, 4.96, 5.1]
trial 3: c1 88  c2 100  c3 0.5  c4 100  c5 [16.71, 4.94, 4.99, 4.8, 4.75, 5.13, 4.88, 5.38, 5.45, 5.82]
```

Two things in the output that the table does not show. The 12 near-duplicate and
punctuation-only files were not blocked: all 12 passed the gate and went on to
train, and each logged status `ok`. And the 4 folder paths were blocked, but with
the code `file_empty`, because on this machine a folder reports a size of 0 bytes.
The gate stopped them for the wrong stated reason.

Criteria 1, 2, 3 and 4 gave identical numbers on all three trials. The gate is
deterministic, so that is expected, and the trials differ only in the files they
generated. Criterion 5 was the only one that varied between trials.

**Verdicts and Diagnoses**

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Bad inputs blocked | >= 75 of 100 | MET | 88, 88 and 88 of 100 on the three trials. All 12 that were not blocked were kinds the gate has no check for. |
| 2 | Every bad-input run logged completely | 100 of 100 complete, none missing | MET | 100 of 100 complete records on every trial, with 100 gate records and every input logged once. |
| 3 | Original still works | accuracy 0.5, macro F1 0.2222 | MET | Accuracy 0.5 and macro F1 0.2222 with 17 train and 4 test posts on every trial, matching `results.json`. The gate returned the data unchanged. |
| 4 | Good inputs pass | >= 90 of 100 | MET | 100, 100 and 100 of 100. No false refusals in any of the 10 kinds. |
| 5 | Run 1 <= 8 s, runs 2 to 10 <= 2 s | both, every trial | MISSED | Run 1 took 17.33, 17.29 and 16.71 s against 8 s. The slowest of runs 2 to 10 took 5.47, 5.12 and 5.82 s against 2 s. Both thresholds were missed on all three trials, and all 27 warm runs were over 2 s (the fastest was 4.61 s). |

**Criterion 5, where and how.** The stage is `train_and_score` in `run.py`. The
Milestone 3 log splits each run into stages, and in both cases that one stage is
almost all of the time:

- Run 1: 17,716 ms of 18,078 ms in `train_and_score`, and 361.9 ms in `validate`.
- Runs 2 to 10: for example 5,693 ms of 5,697 ms in `train_and_score`, and 4.4 ms
  in `validate`. The gate costs about 4 ms once it is warm.

So the new code is not the cause. The miss has two mechanisms inside that one
stage:

1. **Warm runs (about 5 s against a 2 s target).** Every run fine-tunes
   DistilBERT from the base weights for 3 epochs on 17 posts, and nothing is kept
   between runs. The notebook's own trainer reported 4.28 to 4.48 s for just the
   training step on the three seeds, which is most of the 5 s. My criterion
   assumed that after the first run the program would be "near instant", but only
   the imports and the file reads can be reused. The training cannot, and
   shortening it means changing the training settings or saving the model, both of
   which I put out of scope.
2. **Run 1 (about 17 s against 8 s).** Run 1 is about 12 s slower than the warm
   runs on every trial (17.33 against a 5.10 s warm mean, 17.29 against 4.94,
   16.71 against 5.13). Run 1 is where `torch`, `transformers` and `datasets`
   are imported, because the imports are inside `train_and_score`, and where the
   model files are read for the first time. I did not measure how the 12 s splits
   between the imports and the model load, so that split is an inference.

This is one problem seen twice, not two separate failures. Both numbers come from
one stage, and the 1 to 2 s target was not based on a measurement of what that
stage costs. [CHECK AND EDIT: my Milestone 3 log already showed warm runs near
5.7 s before I wrote the target. Say what is true for you.]

**The pattern across the criteria.** Criteria 1 to 4 are about the extension and
the original system, and they were met with identical numbers on every trial. The
only miss is about how long the original system's training takes. That is why the
miss shows nothing about the gate or the log.

**Were my targets set low?** Two of them probably were. Criterion 4 was met at
100 of 100 against a target of 90, which would allow 10 good files to be refused,
and a refused good file is a user who cannot train. I would tighten it to 100 of
100 and widen the good set. Criterion 1 was met at 88, but 4 of those were folders
that were blocked by accident: on this machine a folder reports 0 bytes, so the
gate called them `file_empty`. Without those 4 it is 84, and the 12 near-duplicate
and punctuation-only files got through and trained. [YOUR CALL: say which you
would tighten and to what.]

**Which criteria are broken rather than missed.** None is broken. I added written
definitions under criteria 2 and 3 in `criteria.md`, because "properly logged" and
"still works" could not be scored from the sentence alone. Those definitions were
written in `capstone_test.py` before any trial ran, and the original lines are
unchanged. I did not change any target, and criterion 5 stays as written because
it was measurable and I missed it.

**The Improvement**

**What I changed:** One change, in `run.py`. The model and tokenizer now load from
the local cache first (`local_files_only=True`), and only go to the Hub if the
files are not cached. It is a function called `offline_first`, with three tests in
`test_guard.py`, and the log now records `model_source` (`cache` or `hub`) in each
output. Nothing else changed: the model, the settings, `EPOCHS`, the seed, the
split and `labels.csv` are the same, and `set_seed(seed)` is called before each
load attempt so the starting weights are the same either way. The test harness
gained `--label after` and `--compare` so the after run goes to its own folder. The
measurements, the targets and the files each trial builds are unchanged.

**Which diagnosis pointed at it:** The miss is all inside `train_and_score`, and
part of that stage is loading the model, which happens on every run. As I
understand it, `from_pretrained` asks the Hub whether its cached files are still
current each time, even when they are on disk. I did not measure that cost. Of the
changes I allowed myself, this is the only one that touches the model load without
touching training, which is out of scope. I did not pick "save the model", because
that is the Shape C work in my out-of-scope list, and I did not pick fewer epochs,
because it would change the results criterion 3 protects.

**What I expect (written before the after run):** A small improvement and the same
verdict. The Hub checks are a network round trip per file, so I expect run 1 to
drop by up to a few seconds and the warm runs by under a second. I expect
criterion 5 to still be MISSED, because about 4.3 s of every run is training that
this change does not touch. Criterion 3 is the check on the change itself: if
accuracy or macro F1 differ from 0.5 and 0.2222, the change altered training and
has to be reverted.

**How I ran it:** `python test_guard.py` first, then
`python capstone_test.py --trial N --label after` for N = 1, 2 and 3, then
`python capstone_test.py --report --label after` and
`python capstone_test.py --compare`. The after files are in
`capstone_results_after/`, and `capstone_results/` is untouched.

**Run Log After**

[PASTE THE TABLE FROM `python capstone_test.py --report --label after` HERE. Do
not edit the numbers.]

**Before and after, side by side**

[PASTE THE TWO TABLES FROM `python capstone_test.py --compare` HERE. Do not edit
the numbers.]

**Did it help, and how do I know:** [WRITE THIS FROM THE REAL NUMBERS. Say whether
run 1 and the warm runs got faster, and by how much, using the compare table. Say
whether criterion 5 changed verdict. Say whether criterion 3 still matched
`results.json`. Say whether `model_source` shows `cache` in the after logs. If it
did not help, say that. If it helped but still missed, say how far it still is
from 8 s and 2 s.]