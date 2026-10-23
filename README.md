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

**How I labelled them:** [FILL IN IN YOUR OWN WORDS.] First I labelled 20
rows cold with no tools and marked them `cold` in the note column. Then I had
Claude pre-label the rest from my definitions, and I read and corrected every
row. Rows pre-labelled by Claude say so in the note column. The first 25 rows
in `labels.csv` were pre-labelled by Claude from posts I pasted. I have
changed 0 of them so far; I will update this once I have read all 25.

**Counts per label (interim, 25 rows so far):**

| Label | Count | Share |
|---|---|---|
| `hot_take` | 11 | 44% |
| `analysis` | 5 | 20% |
| `experience` | 5 | 20% |
| `request` | 4 | 16% |
| **Total** | **25** | 100% |

Final counts: [UPDATE when labels.csv reaches 150 to 200 rows. Target mix
from criteria.md: hot_take 90, request 40, experience 40, analysis 30.]

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

**Split sizes:** about 140 train / 30 validation / 30 test (70/15/15 of 200
rows, stratified). Expected per-label counts in the test split, from my
planned mix in `criteria.md`:

| Label | Expected in test | Under the notebook's threshold of 8? |
|---|---|---|
| `hot_take` | about 14 | no |
| `request` | about 6 | yes |
| `experience` | about 6 | yes |
| `analysis` | about 4 | yes |

These are expected values, not what the notebook printed. [REPLACE with the
section 3 table once `labels.csv` is final, and say which labels it
flagged.] Three of four labels are under 8 test examples, so their F1 will
move a lot between seeds. That is a known property of my dataset size and
will explain a lot of next unit's variance.

**Device:** [CONFIRM from section 1 or the `device` and `device_name` fields
in `results.json`: `cpu`, `cuda` or `mps`.] Two runs on the same data and
seed can differ across hardware because the arithmetic runs in a slightly
different order, so the device is part of the result.

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

**Pre-labelling disclosure:** The 25 rows currently in `labels.csv` were
pre-labelled by Claude from posts I pasted, and each says so in the note
column. [YOU FILL IN: how many you changed after reading, which 20 rows you
labelled cold yourself, and whether any later rows were also pre-labelled.]

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

Not measured yet. Command: `python baseline.py --definitions nonexistent.txt
--out baseline_bare.json`. Bare-names accuracy: <x.xxx>, against 0.250 with
my definitions, so the definitions were worth <+/-x.xxx>.

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
| 4. Agreement with staff >= 70% (21 of 30) | one set of 30 posts | not seed-based | not seed-based | not seed-based | <MET or MISSED, from `agreement.py`> |
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
| 4 | Agreement with staff | >= 70% (21 of 30) | <MET or MISSED> | <rate from `agreement.py`, compared with 21 of 30> |
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

**Criterion 4:** <Write after `agreement.py`. State the rate, which label pair
caused most disagreements, and whether it is the `analysis` / `hot_take` pair
that my baseline and my model both struggled with.>

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
taxonomy). I labelled all 30 posts myself before seeing the staff labels, and
committed `my_staff_labels.csv` before running `agreement.py`.

**Agreement rate:** <N> / 30 = <NN>%

My target in `criteria.md` (criterion 4) was at least 70% (21 of 30).
<Met / Missed>.

**Disagreements**

**1.** <first ~12 words of the post>...
- Staff said `<label>`, I said `<label>`.
- **My call:** <staff is right / I am right / split>, because <which numbered
  rule (1 to 4) applies and what the post actually does under it>.
- **Pile:** <(a) rule covered it, I applied it loosely / (b) rule doesn't say /
  (c) rule ambiguous, my reading defensible>

**2.** <repeat for every disagreement>

**Counts by pile:** (a) <n>, (b) <n>, (c) <n>.

**What the pattern in my disagreements tells me:** <Which label pair came up
most? Is it the same boundary my confusion matrix struggled with? Say plainly
what this can and cannot show.>

**A limit on this check:** my own `labels.csv` rows were pre-labelled by
Claude and none is marked `cold`, so I cannot compare this rate against my own
cold labels as `criteria.md` planned. This check shows whether I can apply a
written rule consistently. It does not show whether Claude's pre-labels on my
25 rows are right.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

---

## What's Still Broken

**The gap between what I meant my labels to capture and what the model
learned:**

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**