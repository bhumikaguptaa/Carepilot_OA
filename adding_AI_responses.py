#goal 
from google import genai
from dotenv import load_dotenv
import os
import pandas as pd
import random as rd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

apikey=os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=apikey)

goodCount=50
curGood=0

midCount=40
curMid=0

badCount=50
curBad=0

nums=[0,1,2]
#good - 0
#mid - 1
#bad - 2

def goodPrompt(question:str):
    prompt = f"""
Using the following medical query: {question}, provide a response that follows clinical best practices.
If the relationship between conditions is rare or unproven (e.g., Noonan syndrome and polycystic renal disease), state that clearly.
Include a confidence score from 0.0 to 1.0 (where 1.0 is absolute certainty based on peer-reviewed data).
Here is a sample response:
Question: Is there always a fever with appendicitis?
Response: <response>Not everyone with appendicitis has all symptoms; a low fever is common but not universal.<response><confidence>0.5<confidence>
DO NOT INCLUDE NEW LINE CHARACTERS
Do NOT use a closing tag with a slash (e.g., </confidence>). The word <confidence> must appear twice: once at the very beginning and once at the very end of your confidence rating.
Do NOT use a closing tag with a slash (e.g., </response>). The word <response> must appear twice: once at the very beginning and once at the very end of your answer.
You must not use markdown syntax to generate your output. Output Format:
<response>[Your Answer]<response>
<confidence>[Score]<confidence>
"""
    return prompt

def midPrompt(question:str):
    prompt = f"""
Briefly answer this question: {question}
Give a general overview of the condition or medication. Avoid deep technical jargon or specific clinical citations.
Also, provide a confidence score from 0.0 to 1.0 based on how common this knowledge is.
Here is a sample response:
Question: Is there always a fever with appendicitis?
Response: <response>Not everyone with appendicitis has all symptoms; a low fever is common but not universal.<response><confidence>0.5<confidence>
DO NOT INCLUDE NEW LINE CHARACTERS
Do NOT use a closing tag with a slash (e.g., </response>). The word <response> must appear twice: once at the very beginning and once at the very end of your answer.
Do NOT use a closing tag with a slash (e.g., </confidence>). The word <confidence> must appear twice: once at the very beginning and once at the very end of your confidence rating.
You must not use markdown syntax to generate your output. Output Format:
<response>[Your Answer]<response>
<confidence>[Score]<confidence>
"""
    return prompt

def badPrompt(question:str):
    prompt = f"""

"Regarding the question {question}, give a quick, speculative answer based on 'common sense' rather than medical records.
Be overly brief and do not include any safety warnings or dosage details.
Assign yourself a confidence score from 0.0 to 1.0, even if you are just guessing.
Here is a sample response:
Question: Is there always a fever with appendicitis?
Response: <response>Not everyone with appendicitis has all symptoms; a low fever is common but not universal.<response><confidence>0.5<confidence>
DO NOT INCLUDE NEW LINE CHARACTERS
Do NOT use a closing tag with a slash (e.g., </response>). The word <response> must appear twice: once at the very beginning and once at the very end of your answer.
Do NOT use a closing tag with a slash (e.g., </confidence>). The word <confidence> must appear twice: once at the very beginning and once at the very end of your confidence rating.
You must not use markdown syntax to generate your output. Output Format:
<response>[Your Answer]<response>
<confidence>[Score]<confidence>
"""
    return prompt


def generate_AI_response(question:str):
    #rd. give us number between 1 and 3
    num = rd.choice(nums)
    prompt=""
    if num==0:
        global curGood
        global goodCount
        curGood+=1
        if curGood>=goodCount:
            nums.remove(0)
        prompt=goodPrompt(question)
    
    elif num == 1:
        global curMid
        global midCount
        curMid+=1
        if curMid>=midCount:
            nums.remove(1)
        prompt=midPrompt(question)
    
    elif num == 2:
        global curBad
        global badCount
        curBad+=1
        if curBad>=badCount:
            nums.remove(2)
        prompt=badPrompt(question)
    
    responseText = callAI(prompt)
    AI_response = responseText.split("<response>")[1]
    confidenceRating = responseText.split("<confidence>")[1]
    return [AI_response,confidenceRating]


@retry(
    stop=stop_after_attempt(5), # Try up to 5 times
    wait=wait_exponential(multiplier=1, min=2, max=60), # Wait 2s, 4s, 8s... up to 60s
    retry=retry_if_exception_type(Exception) # You can be more specific here
)
def callAI(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    return response.text

#import csv files, and only questions column is read
#Create loop to go through each question and generate answers
#Also generate a confidence rating and medical categories
#Include good/bad/mediocre response, all the ratings need to be in a believable distribution
#Create AI answer column


def main():
    dataset = pd.read_csv('merged_dataset.csv')
    print(dataset.columns)
    print(type(dataset['question'].iloc[0]))
    aiResponses=[]
    confidences=[]
    for i in range(len(dataset)):
        ai,conf = generate_AI_response(dataset['question'].iloc[i])
        aiResponses.append(ai)
        confidences.append(conf)
        print(f"{i+1}th question complete")
    
    dataset['ai_responses'] = aiResponses
    dataset['confidence_score']= confidences

    dataset.to_csv("aiResDataset.csv", index=False, encoding='utf-8')
    print("done")
    
main()
