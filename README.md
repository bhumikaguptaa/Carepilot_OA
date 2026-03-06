
# Carepilot OA

This is a robust, multi-stage framework designed to audit AI-generated medical responses
for Accuracy, Helpfulness, and Safety. It addresses the critical challenge of "hallucinations" 
by combining LLM-based qualitative judging with high-precision machine learning classifiers.

The project structure

The project is divided into three parts. 

# PART 1

Creating a synthetic medical evaluation dataset. Here is the structure of the dataset (sample_eval_data.csv):

 Column | Type | Description |
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

I used two existing medical question and answer datasets: 
https://www.nature.com/articles/s41597-025-05233-z and https://www.kaggle.com/datasets/thedevastator/comprehensive-medical-q-a-dataset?resource=download


### Step 1
Clean data1 (medaesqa_v1.json) using `clean_medaesqav1.py` using and clean data2 (train.xlsx) and merge using `clean_train_dataset_and_merge.py` to create initial dataset of medical questions and human answers. 

Columns generated so far: `question, reference_answer`

### Step 2 
Generate AI response and confidence rating using `gemini-2.5-flash` API in `adding_AI_responses.py`. The resulting new dataset with AI responses is stored in `aiResDataset.csv`

Columns generated so far: `question, reference_answer, ai_response, confidence_score`


### Step 3 

I used Antigravity to come up with a set of question types, due to an unusual amount of hallucinations from Gemini. 

I used `categorize.py` to assign question types to each row and generate `datasetwithAIResponses_categorized.csv`. 

Columns generated so far: `question, reference_answer, ai_response, confidence_score, question_type`

### Step 4
I created the question_id column to have a unique identifier for each question. 

Next, I generated the `human_rating` column by comparing the cosine similiarity between the semantic sentence embeddings of `ai_response` and `reference_answer`.

Lastly, I created the `response_length` column which denotes the number of words in the `ai_response`. All the data generation in this step was done with `final.py`. With this step I had all the columns necessary to begin analysis.

Dataset in `sample_eval_data.csv`.


### Step 5

Final step was to manually changed a few features to create edge cases in the dataset.

---


# PART 2

Analyzed the sample_eval_data.csv and answered the following questions in `Data_Analysis_PART2.ipynb`. 

Used descritive analytics to answer: 

#### Question 1: What does the data look like in terms of quality (human_rating), length (response_length), and safety (flagging)?

#### Question 2: What are the characteristics of 5 star or 1 star human rating for flagged responses? (profiling extremes)

#### Question 3: How does the model's confidence score relate to actual human ratings? (model calibrations, investigating further)

#### Question 4: Are there specific question types where the model performs better?

#### Question 5: What triggers the human flag? (outliers and overconfidence)

#### Question 6: What specific conditions and thresholds cause an AI-generated response to be flagged by human reviewers?


Used predictive analytics to answer: 

#### Question 7: What combination of length, confidence rating ,human rating, question type makes a response most likely to be flagged by users?

#### Question 8: Can a non-linear machine learning model better predict which responses will be flagged? 

#### Question 9: Is the AI better at responding to certain categories of questions, or are the variations in human rating and confidence score simply due to random chance?

---


# PART 3

**Assumption:** The prompt mentioned that the evaluation pipeline will receive a csv of question/answer pairs. Since it was clear whether the answer referred to human answers or AI answers, **my assumption for this part was that the csv supplied will contain question/ai answer pairs.**

Created a lightweight, reusable evaluation pipeline in `eval_pipline_PART3.py`

Wrote a Python script that takes in a CSV of question ad human response pairs and generates and AI response and confidence scores. 

Based on those responses outputs certain evaluation metrics. 
- Response length analysis - analyses the variation in AI response lengths. Additionally, there is an analysis of token length, as tokens are the primary measure of input data length for AI models.
- A test for semantic entropy — The script generates AI responses for each question 2 more times and finds the cosine similiarity between each generated response and the human answer to measure AI response volatility
- Added an LLM-as-a-judge component where I used an API call to have a model judge the generated ai response and score the responses on specific criteria (accuracy, helpfulness, safety). 

Lastly all these metrics are collected together in a summary report labelled `summary.txt`.


