##PART 1 - CREATE dataset

https://www.nature.com/articles/s41597-025-05233-z #medaesqa
https://www.kaggle.com/datasets/thedevastator/comprehensive-medical-q-a-dataset?resource=download #train kaggle

##step1
clean data1(medaesqa_v1.json) and clean data2(train.xlsx) and merge get existing question and human answer. 

##step2 
get ai response and ai confidence rating - using gemini API 
this creates a separate file -- adding_AI_responses.py and aiResDataset.csv

##step 3 
now we get question type using Antigravity -- gemini had too many halucinations while doing sanity check
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


##PART 2 ANALYSIS

##step 6 
descritive analytics (and interpretation)

##step 7
predictive analytics (and interpretation)

