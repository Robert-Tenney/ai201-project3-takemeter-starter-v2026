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

**Moment 3 (unit 6)**

- *What I asked for:* Help working through the unit 6 milestones: running the
  baseline, reading my three-seed results and confusion matrix, drafting the
  README sections, and writing the verdicts and diagnoses.
- *What came back:* Claude drafted the README text for Baseline vs. Trained, the
  Run Log, and the Verdicts and Diagnoses sections from my uploaded result
  files. It also computed the baseline's score on my 4 held-out posts from the
  baseline predictions it had already saved, and pointed out that my 25-row
  dataset, not my training settings, explained most of my misses. It declined to
  label the 30 staff posts for me.
- *What I changed:* <YOU FILL IN: which sentences you rewrote, which numbers you
  checked against the JSON files yourself, what you disagreed with, and whether
  you kept or changed the "EPOCHS 3 to 15" choice.>
- *What I did myself:* <YOU FILL IN: confirm you labelled the 30 staff posts
  yourself before seeing the staff labels, and wrote the adjudication of each
  disagreement.>

**Pre-labelling disclosure:** The 25 rows currently in `labels.csv` were
pre-labelled by Claude from posts I pasted, and each says so in the note
column. No row is marked `cold`, so none of the 25 was labelled unaided, and
no later rows were added. <YOU FILL IN: how many you changed after reading.>

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

**How I ran it:** In the notebook I set `EPOCHS = 15`, re-ran section 2 to pick
up the change, set `RUN_LABEL = "after"` in section 6, and ran section 6 once.
It wrote `results_three_seeds_after.json`. `results_three_seeds_before.json` is
untouched.

### Run Log — After

Numbers are from `results_three_seeds_after.json`. Device: <cpu, from the JSON>.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | >= 0.60 on every seed | <x.xxx> | <x.xxx> | <x.xxx> | <MET / MISSED> |
| 2. Every label F1 (`analysis` >= 0.40, others >= 0.50) | all labels, every seed | <four F1s> | <four F1s> | <four F1s> | <MET / MISSED> |
| 3. No label > 60%; smallest >= 25 | both parts | largest 44%, smallest 4 | same | same | MISSED (unchanged, a property of `labels.csv`) |
| 4. Agreement with staff >= 70% | one set of 30 posts | 30 of 30 (100%) | not seed-based | not seed-based | MET (unchanged) |
| 5. Recall on `analysis` >= 0.50 on every seed | every seed | <x.xxx> | <x.xxx> | <x.xxx> | <MET / MISSED> |

### Before and after, side by side

| Measure | Before: 42 / 7 / 2024 | After: 42 / 7 / 2024 |
|---|---|---|
| Accuracy | 0.500 / 0.250 / 0.500 | <x / x / x> |
| Macro F1 | 0.222 / 0.167 / 0.222 | <x / x / x> |
| Mean confidence when right (seed 42) | 0.296 | <x.xxx> |
| Recall `analysis` | 0.000 / 0.000 / 0.000 | <x / x / x> |

**Did it help, and how do I know:** <One sentence first: yes, no, or mixed.
Then the evidence: which numbers moved, whether the seeds still disagree, and
whether the after confusion matrix still shows every post going to one label.
With 4 test posts, one post is 25 points of accuracy, so say whether the change
is bigger than that. If it did not help, say so. That is a complete result.>

---

## What's Still Broken

Four of my five criteria are missed in the before run, and criterion 4 is met.
For each one: what I would do, and why I stopped. The "After the change" line on
criteria 1, 2 and 5 is for the result of the `EPOCHS` 3 to 15 re-run.

**Criterion 1 (accuracy >= 0.60 every seed):** Missed before (0.500, 0.250,
0.500). *After the change:* <MET or MISSED, with the three accuracies.> What I
would do next: label more rows. The measure is a 4-post test set, where one post
is 25 points, so no training change can make this number stable. I stopped
because labelling 150 to 200 rows by hand, with care, did not fit this unit, and
it would also have changed `test_split.csv` and broken the like-for-like
comparison with my baseline.

**Criterion 2 (every label F1):** Missed before (three labels at 0.000 on every
seed). *After the change:* <MET or MISSED, with the four F1s per seed.> What I
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
on every seed). *After the change:* <MET or MISSED, with the three recalls.>
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
four ideas. *After the change:* <say whether the after-run matrix still puts
every post in one column or spreads predictions across labels.>

**Anything I would not trust in these results:** every number comes from a
4-post test set on 25 labelled rows, and all 25 rows were pre-labelled by
Claude from my definitions, so even a perfect score would measure agreement with
those pre-labels and not with a human standard. The staff agreement check
measures how I apply someone else's rules, not whether those pre-labels are
right.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**