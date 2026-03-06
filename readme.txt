
Carepilot OA

This is a robust, multi-stage framework designed to audit AI-generated medical responses
for Accuracy, Helpfulness, and Safety. It addresses the critical challenge of "hallucinations" 
by combining LLM-based qualitative judging with high-precision machine learning classifiers.

The project structure

The project is divided into three parts. 

PART 1

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

##step1
clean data1(medaesqa_v1.json) and clean data2(train.xlsx) and merge get existing question and human answer. 

##step2 
get ai response and confidence rating - using gemini API 
this creates separate files -- adding_AI_responses.py and aiResDataset.csv

##step 3 
now I get question type using Antigravity -- gemini had too many halucinations 
this creates -- datasetwithAIResponses_categorized.csv

##step 4
with these five columns, we create the 
                    flagged responses, 
                    question_id, 
                    human rating (using sentence embeddings and to make the distribution even - quadratic normalization),
                    ai response length (by number of words), 
and this all with the other colums creates -- sample_eval_data.csv and final.py

##step 5
manually went in the data and changed a few features to create edge cases for the part 2 of the OA. 

PART 2

Analyzed the sample_eval_data.csv and answered the following questions in Data_Analysis.ipynb. 

Used descritive analytics to answer: 
Queston 1: What does the data look like in terms of quality (human_rating), length (response_length), and safety (flagging)?
Question 2: What are the characteristics of 5 star or 1 star human rating for flagged responses? (profiling extremes)
Question3: How does the model's confidence score relate to actual human ratings? (model calibrations, investigating further)
Question 4: Are there specific question types where the model performs better?
Quesiton 5: What triggers the human flag? (outliers and overconfidence)
Question 6: What specific conditions and thresholds cause an AI-generated response to be flagged by human reviewers?


Used predictive analytics to answer: 
(Generating one-encoded mapping for all the question_type of the dataset)
Question 7: What combination of length, confidence rating ,human rating, question type makes a response most likely to be flagged by users?
Question 8: Can a non-linear machine learning model better predict which responses will be flagged? 
Question 9: Is the AI better at responding to certain categories of questions, or are the variations in human rating and confidence score simply due to random chance?

PART 3

Created a lightweight, reusable evaluation pipeline in eval_pipline.py

Wrote a Python script that takes in a CSV of question ad human response pairs and outputs an AI response 
and confidence scores. Based on those responses outputs certain evaluation metrics. 
Those include:
response length analysis
text similarity scores 
key words checks for sensitive words
and also includes the summary report. Added an LLM-as-a-judge component where I used an API call to have a model
score the responses on specific criteria (accuracy, helpfulness, safety). 

How to run the file:

Follow these steps to set up the environment and run the evaluation pipeline on your local machine.

1. You will need an OpenAI API Key to power the "LLM-as-a-Judge" scoring component.
2. Installation:
'''
git clone https://github.com/your-username/carepilot-eval.git
cd carepilot-eval
pip install -r requirements.txt
'''

3. Configuration:
Windows
'''
set OPENAI_API_KEY=sk-your-key-here
'''

Mac 
'''
export OPENAI_API_KEY='sk-your-key-here'
'''

4. Running the eval pipeline:
'''
python eval_pipline.py
'''

