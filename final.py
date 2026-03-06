from sentence_transformers import SentenceTransformer, util
import pandas as pd



model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_rating(row):

    human = str(row['reference_answer'])
    ai = str(row['ai_responses']) 
    
    if not human.strip() or not ai.strip():
        return 1
    

    embeddings = model.encode([human, ai], convert_to_tensor=True)
    

    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    

    rating = 1 + (similarity**2 * 4)
    
    # Return as an integer (rounded) or float depending on your preference
    return int(round(rating))

def response_length(row):
    aires = str(row['ai_responses'])
    return aires.count(" ")+1

def human_flagging(row):
    score=float(row['confidence_score'])
    if score<0.5: #anything befow 50% of confidence
        return 1
    else:
        return 0



#Counter({4: 56, 3: 41, 2: 22, 1: 17, 5: 4})


dataset = pd.read_csv('datasetwithAIResponses_categorized.csv') 

dataset['human_rating'] = dataset.apply(calculate_rating, axis=1)
dataset['response_length'] = dataset.apply(response_length, axis=1)
dataset['flagged'] = dataset.apply(human_flagging, axis=1)

dataset.insert(0, 'question_id', range(len(dataset)))

dataset.to_csv("sample_eval_data.csv",index=False)

## 
