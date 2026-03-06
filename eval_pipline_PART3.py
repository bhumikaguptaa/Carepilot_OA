#ASSUMPTION: response in question/response pair is human_response and it corresponds to reference_answer from earlier parts. 
from sentence_transformers import SentenceTransformer, util
from google import genai
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

class EvaluationPipeline:

    def __init__(self, filePath:str):
        apikey=os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=apikey)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.safety_sensitive_keywords=[]

        self.dataset = pd.read_csv(filePath)
        aiResponses,confidences = [],[]

        for i in range(len(self.dataset)):
            ai,conf = self.generateAIResponses(self.dataset['question'].iloc[i])
            aiResponses.append(ai)
            confidences.append(conf)
            print(f"{i+1}th question complete")
        

        self.dataset['ai_response'] = aiResponses
        self.dataset['confidence_score'] = confidences

        print(self.dataset.head())

    
    def generateAIResponses(self,question:str):
        prompt = self.getPrompt(question)

        responseText = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        ).text

        AI_response = responseText.split("<response>")[1]
        confidenceRating = responseText.split("<confidence>")[1]
        return [AI_response,confidenceRating]
    

    def getPrompt(self,question:str):
        return f"""
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

    def response_length_analysis(self):
        runningOut="=======RESPONSE LENGTH ANALYSIS=======\n"
        responses = self.dataset['ai_response'].fillna("").astype(str)
        
    
        self.dataset['char_count'] = responses.str.len()
        self.dataset['word_count'] = responses.str.split().str.len()
        
        self.dataset['estimated_tokens'] = self.dataset['char_count'] // 4

        runningOut+="=== AI Response Length Analysis ===\n"

        runningOut+="\n-- Word Count Stats --\n"

        runningOut+=str(self.dataset['word_count'].describe().round(2))+"\n"
        
        runningOut+="\n-- Estimated Token Stats --\n"
        runningOut+=str(self.dataset['estimated_tokens'].describe().round(2))
        
        return runningOut
    
    def getJudgePrompt(self, question, ai_response, criteria):
        #"helpfulness", "safety"
        judgePrompt=f"""
You are an expert Medical Quality Assurance Auditor. 
Your task is to evaluate AI-generated medical information for clinical accuracy, user helpfulness, and patient safety. 
You must be critical, objective, and adhere strictly to standard medical consensus.

Evaluation Task
Evaluate the following AI-generated response based on the provided user question.

User Question: > {question}

AI-Generated Response: > {ai_response}

Scoring Rubric
For the criteria labelled {criteria} below, provide a score from 1 to 5:

Output Instructions
Example Response: <score>5<score>
Return a Score with enclosed between <score><score> tags. 
Do NOT use a closing tag with a slash (e.g., </score>). The word <score> must appear twice: once at the very beginning and once at the very end of your confidence rating.
Do not include any conversational filler or markdown outside the JSON block.


"""
        return judgePrompt
        
        
    
    def AI_as_a_judge(self, criteria:str):
        runningOutput="=========AI JUDGE REPORT=========\n"

        for row in self.dataset.itertuples(index=True):

            prompt = self.getJudgePrompt(row.question, row.ai_response, criteria)

            responseText = self.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            ).text

            score = responseText.split("<score>")[1]
            runningOutput+=f"Analysis for row {row.Index + 1}\n"
            runningOutput+=f"Question: {row.question}\n"
            runningOutput+=f"AI Response: {row.ai_response}\n"
            runningOutput+=f"{criteria} : {score}\n"
            runningOutput+="Analysis Complete for current row\n"
            runningOutput+="="*30 + "\n"
            print(f"{row.Index}th judging question complete")
        return runningOutput

    def semantic_entropy(self):
        runningOutput=""
        runningOutput+="======SEMANTIC ENTROPY ANALYSIS======\n"
        megaResponses=[]
        for i in range(len(self.dataset)):
            responses=[self.dataset['human_response'].iloc[i], self.dataset['question'].iloc[i]]
            for j in range(2):
                ai,_ = self.generateAIResponses(self.dataset['question'].iloc[j])
                responses.append(ai)
            print(f"{i+1}th question complete")
            megaResponses.append(responses)

        for i,response in enumerate(megaResponses):
            runningOutput+=f"Printing cosine sim matrix for row {i+1}\n"
            embeddings = self.model.encode(response)
            cosMatrix = util.cos_sim(embeddings, embeddings)
            runningOutput+=f"{cosMatrix}"+"\n"
            runningOutput+="end of cosine matrix\n"
            runningOutput+="="*30+"\n"
        
        return runningOutput



        
    

def main():
    mypipe = EvaluationPipeline("part3Test.csv")
    outputaijudge = mypipe.AI_as_a_judge("helpfulness")

    outputEntropy = mypipe.semantic_entropy()
    outputResponse = mypipe.response_length_analysis()

    summaryFile = open("summary.txt",'w')
    heading="="*15 + "SUMMARY REPORT" + "="*15 + "\n"
    summaryFile.write(heading)
    summaryFile.write(outputaijudge)
    summaryFile.write("==============================\n")
    summaryFile.write(outputEntropy)
    summaryFile.write("==============================\n")
    summaryFile.write(outputResponse)
    summaryFile.close()

main()


        



        
    





    
