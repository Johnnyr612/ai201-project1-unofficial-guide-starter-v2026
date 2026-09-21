# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
I picked 4 of 5 because one of my questions is about a very specific local fact and the corpus is uneven across towns and topics. A retrieval system that gets 4 out of 5 right is doing the core job without setting an unrealistic target that would fail for a reasonable amount of variation in the data.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
I chose 5 of 5 because this project is supposed to ground answers in the corpus rather than generate unsupported claims. If the answer does not tie back to a document, it breaks the whole point of a retrieval system and I want that failure to be obvious at evaluation time.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
The corpus is structured and constrained, so I expect the in-corpus and out-of-corpus questions to be separated by a clear distance gap. I chose 4 of 5 because a single borderline case is realistic even when the gate is mostly working, and that still gives a meaningful standard for refusing bad questions.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks read as a complete thought and do not cut a sentence or heading in half.

**Why this target:**
My corpus contains long, sectioned travel guides where useful information is spread across paragraphs. If chunks break inside a sentence or right at the boundary of a heading, the retrieved material becomes hard to interpret, so this target measures whether the chunking strategy preserves usable context.

---

## 5. Your choice

For at least 4 of my 5 questions, the answer includes a concrete place, time, or number from the corpus rather than a vague summary.

**Why this target:**
This corpus is full of practical, location-specific details such as walking times, dining hours, and price differences. I care about factual grounding more than broad summaries, because a vague answer is easy to generate but not useful for a guide designed around real logistics.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
