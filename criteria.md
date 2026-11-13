# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

Labels: `analysis`, `hot_take`, `request`, `experience`. Four labels means a
random guesser gets about 25%.

Planned label mix for 200 posts: `hot_take` 90 (45%), `request` 40 (20%),
`experience` 40 (20%), `analysis` 30 (15%). With a 70/15/15 split that is
about 30 posts in the held-out set. These are plans made before collecting;
the real counts go in the README's Dataset section.

---

## 1.

Overall accuracy on the held-out set is at least 0.60 on every one of the
three seeds.

**Why this target:** My biggest label will probably be `hot_take`, because
most comments in the r/touhou threads I read were short unsupported claims.
If it is about 45% of my data, a model that always says `hot_take` scores
about that much, so 0.60 has to clear it by a real margin. It is also well
above the 0.25 a random guesser gets on four labels. I did not go higher
because the held-out set is only about 30 posts, so one seed can swing
several points on a handful of posts.

---

## 2.

Every label has an F1 of at least 0.50 on the held-out set on every seed,
except my smallest label (`analysis`), which must reach at least 0.40.

**Why this target:** `request` and `experience` are recognisable from
surface features (a question, "help me", "I like"), so they should be easier.
`analysis` is the label I expect to be thinnest, with about 30 examples and
only about 4 landing in the test split. An F1 on that few posts moves a
lot between seeds, so I loosened its target and I am saying so up front
rather than after I miss.

---

## 3.

No label is more than 60% of `labels.csv`, and my smallest label has at
least 25 examples.

**Why this target:** The brief's cap is 70%. I set mine lower because
`hot_take` is the label I expect to run large, and at 70% a model that guesses
it every time scores 0.70, which would beat my accuracy target without
learning anything. The 25-example floor gives the smallest label about 4 in
the test split, which is still jumpy, but fewer than that makes its F1
meaningless.

---

## 4.

My agreement with the staff labels on the 30 staff posts is at least 70%
(21 of 30).

**Why this target:** The staff taxonomy note says several of those posts were
chosen because they are ambiguous and that a rate in the 70s is normal. I
picked the bottom of that range rather than above it, because I have not yet
applied someone else's written rule to a real set. I will compare it with my
20 cold-labelled rows in `labels.csv` to see whether my own labels were
consistent.

---

## 5.

On the held-out set, at least 50% of true `analysis` posts are predicted as
`analysis` (recall of at least 0.50), on every seed.

**Why this target:** The boundary between `analysis` and `hot_take` is the
one I expect to be hardest, because many comments name a game or character
without arguing from it. A model that collapses everything unsupported into
`hot_take` would score fine on accuracy while missing the one label I care
about most. This criterion measures that directly. With only about 4
`analysis` posts in test, the number is noisy, so I chose a recall that is
better than a coin flip rather than a high one.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->


---

## Capstone

Five acceptance criteria for the capstone extension (Shape B, harden against
failure): the validation gate in `guard.py`, and the gated run in `run.py` with
its structured log. The five above are the project 3 criteria and are left as
they were. These five were written before any capstone results existed.

At least three are about the extension, and at least one is about what happens
when input is bad. Each has a target a person could check without asking me
what I meant, and a reason that points at something in this system.

---

### 1.

On the new set, at least 75% of bad inputs in a set of 100 are detected and
blocked.

**Why this target:** I choose to allow a quarter of bad inputs pass to ensure
that the criterion 2 works.

---

### 2.

Regardless of the amount of bad inputs, the run is properly logged.

**Why this target:** I want the run to be properly logged so I can use the
failures to troubleshoot any issues.

> **Revised in Milestone 6:** Over 100 bad inputs run through `run.py`,
> `run_log.jsonl` holds exactly 100 records, one per input, and every record is
> complete: a timestamp, an input holding the file path, an output with a status
> (`ok`, `refused` or `error`) and a non-empty message, a code on every status
> that is not `ok`, and a numeric `duration_ms`. `guard_log.jsonl` also holds
> exactly 100 records.
>
> **Why revised:** "properly logged" and "regardless of the amount" gave me
> nothing to check, and two people could not have scored it the same way. The
> definition above was written into `capstone_test.py` before any trial ran, and
> is recorded here so the criteria file matches what was tested. The original
> line above is unchanged.

---

### 3.

The original function still works even with the new changes added.

**Why this target:** I want to make sure that if the new changes were reverted
the program will still function.

> **Revised in Milestone 6:** On the real `labels.csv`, the gate returns the
> DataFrame unchanged (equal to what `pd.read_csv` reads), and `python run.py` at
> seed 42 reproduces the notebook's `results.json`: accuracy 0.5, macro F1
> 0.2222 (rounded to 4 decimals), and 4 test posts.
>
> **Why revised:** "still works" had no measure, so I could not reach a verdict
> from it. The definition above was written into `capstone_test.py` before any
> trial ran, and is recorded here so the criteria file matches what was tested.
> The original line above is unchanged.

---

### 4.

In the new set, at least 90% of the good inputs in a set of 100 are able to
pass without problems.

**Why this target:** I choose to set the criterion to 90% to see how the
program would react to marking a good input as invalid.

---

### 5.

After the first run of the program, the time it takes for the program to run is
significantly faster. For example, the first run should take up to 5 to 8
seconds while the rest should take 1 to 2 seconds.

**Why this target:** After the initialization the program should be able to run
near instantly.