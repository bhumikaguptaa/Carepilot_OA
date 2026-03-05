# CarePilot — Take-Home Assignment

**AI + Data Analytics**

---

**Estimated time:** 4–6 hours total across all parts
**Format:** Jupyter Notebook (.ipynb) or Python scripts + a short writeup
**Submission:** Share a GitHub repo link
**Questions?** Totally fine to ask — reach out anytime.

---

## Hey! Welcome

Thanks for your interest in CarePilot! We put this together so you can show off your skills in a low-pressure way. There are no trick questions and no single *right* answer — we're way more interested in how you think than whether you nail every detail.

This assignment has three parts that build on each other. You can use Python, any libraries you want, and Claude/ChatGPT/etc. We'd rather see clean, thoughtful work on two parts than rushed work on all three.

---

## Some Context

Imagine you're working with a healthcare-adjacent AI company that uses large language models (LLMs) to help answer questions about health-related topics. A core part of the work involves making sure the AI's responses are accurate, safe, and genuinely helpful.

For this assignment, you'll work with a synthetic dataset you create yourself. It simulates the kind of data you might encounter: questions, AI-generated responses, and some metadata.

---

## The Dataset

You'll generate a CSV (`sample_eval_data.csv`) with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `question_id` | integer | Unique ID for each question |
| `category` | string | Topic area (e.g., nutrition, medication, exercise, mental_health, sleep) |
| `question` | string | The health-related question asked |
| `ai_response` | string | The LLM-generated answer |
| `reference_answer` | string | A gold-standard human-written answer |
| `response_length` | integer | Word count of the AI response |
| `confidence_score` | float | Model's self-reported confidence (0–1) |
| `human_rating` | float | Human evaluator score (1–5 scale) |
| `flagged` | boolean | Whether a human flagged the response as problematic |

*You'll generate this dataset yourself as part of Part 1.*

---

## Part 1: Build the Dataset

**Goal:** Create the synthetic evaluation dataset described above.
**Time estimate:** ~1–2 hours

Write a Python script that generates a realistic-looking CSV with at least 100 rows. Here's what we're looking for:

- Questions should feel like real things someone might ask about health topics (be creative!)
- AI responses should vary in quality — some good, some mediocre, a few clearly bad
- The numeric fields (confidence, ratings, etc.) should have realistic distributions, not just random noise
- Flagged responses should correlate (at least loosely) with lower human ratings
- You can use an LLM API to help generate text content if you want — just note it in your writeup

> **Bonus:** Add a few intentionally tricky edge cases — e.g., a response with high confidence but low human rating, or a flagged response that actually seems fine. We love seeing people think about messy, real-world data.

---

## Part 2: Analyze the Data

**Goal:** Dig into the dataset from Part 1 and surface interesting patterns.
**Time estimate:** ~1.5–2 hours

Using the CSV you generated, explore the data and answer questions like:

1. How does the model's confidence score relate to actual human ratings? Is the model well-calibrated?
2. Are there meaningful differences across categories? (e.g., does the model do better on nutrition questions than mental health?)
3. What characterizes flagged responses? Can you build a simple classifier or heuristic to predict them?
4. Does response length have any relationship with quality?

We're looking for clear visualizations (matplotlib, seaborn, plotly — whatever you like), brief written interpretations, and any surprising findings. A Jupyter Notebook works great for this.

> **Bonus:** Go beyond descriptive stats. Try a simple regression, a clustering approach, or a text similarity metric between AI responses and reference answers.

---

## Part 3: Build a Mini Eval Pipeline

**Goal:** Create a lightweight, reusable evaluation pipeline.
**Time estimate:** ~1.5–2 hours

Now that you've explored the data, build something that could be run again on new data. Specifically:

- Write a Python script or module that takes in a CSV of question/response pairs and outputs a set of evaluation metrics
- Include at least 2–3 automated metrics (e.g., text similarity scores, response length analysis, keyword checks for safety-sensitive terms)
- Generate a summary report (can be a printed output, a markdown file, or even a simple HTML page)
- Include basic error handling and a README explaining how to run it

This doesn't need to be production-ready. We just want to see how you think about building tools that are reusable and maintainable.

> **Bonus:** Add an LLM-as-a-judge component where you use an API call to have a model score the responses on specific criteria (accuracy, helpfulness, safety). Even a simple version of this is impressive.

---

## What We're Looking For

| We Care About | What That Means |
|---------------|-----------------|
| Thoughtfulness | Did you think carefully about the problem, or just blast through it? |
| Clean code | Readable, well-organized, with comments where they help |
| Communication | Can you explain your thinking clearly in writing? |
| Curiosity | Did you explore, ask interesting questions, or try something unexpected? |
| Pragmatism | Did you scope your work well and make smart tradeoffs? |

We explicitly do **not** care about: pixel-perfect visualizations, exhaustive statistical testing, or covering every possible edge case. Do good work on the parts that interest you most.

---

## Submission

When you're done, send us:

- Your code (Jupyter notebooks, Python files, or both)
- The generated CSV dataset
- A short writeup (can be in the notebook or a separate doc) covering your approach, any assumptions you made, and what you'd do with more time

A GitHub repo is ideal, but a .zip file works too. No stress on presentation — substance over style.

There's no hard deadline, but we'd love to have it back within **7-14 days**. If you need more time, just let us know. Seriously, it's fine.

---

Good luck, have fun with it. If you have any questions at all, don't hesitate to reach out. We're rooting for you!

*— The CarePilot Team*
