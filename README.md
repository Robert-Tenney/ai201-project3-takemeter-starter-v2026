## The Dataset

**Where the posts came from:** r/touhou, public pages only. Posts come from
the Help, Fan Discussion and Game Discussion flairs. Many rows are top-level
comments from the Fan Discussion thread "What touhou opinion would put you in
this situation?", because that is where long text arguments appear. I have
asked my TF whether comments count as posts: [ANSWER HERE]. Excluded: art,
memes, video, cosplay, fanfiction chapters, mod threads and ads.

**How I labelled them:** [FILL IN.] First I labelled 20 rows cold with no
tools and marked them `cold` in the note column. Then I had Claude pre-label
the rest from my definitions, and I read and corrected every row. Rows
pre-labelled by Claude say so in the note column. The first 25 rows in
`labels.csv` were pre-labelled by Claude from posts I pasted. I have changed
0 of them so far; I will update this once I have read all 25.

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
> runs, which makes it a report of their play. [REWORD: also say what you
> would do if a reply argued it as a general claim about the game.]

---