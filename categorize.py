import pandas as pd
import re

def categorize_question(row):
    text = str(row['question']).lower() + " " + str(row['reference_answer']).lower()
    
    categories = {
        "Genetics & Rare Diseases": ["gene", "mutation", "syndrome", "genetic", "chromosome", "inherited", "variant", "dysplasia", "rare disease", "family history"],
        "Cardiovascular & Blood": ["heart", "blood", "cad ", "angina", "t wave", "artery", "cardiac", "stroke", "bleeding", "hypotension", "aorta", "vascular", "cholesterol", "hypertension", "anemia"],
        "Neurological & Mental Health": ["nerve", "brain", "ptsd", "ms ", "multiple sclerosis", "numbness", "huntington", "neuropathy", "seizure", "intellectual", "alzheimer", "cognitive", "dyspraxia", "autism", "epilepsy", "headache", "dementia", "psychiatric", "mental", "anxiety", "depression", "stress", "spinal cord"],
        "Respiratory Health": ["copd", "breath", "lung", "asthma", "apnea", "respiratory", "pulmonary", "airway", "chest"],
        "Gastrointestinal & Liver": ["ibs", "crohn", "bowel", "digestion", "liver", "stomach", "pancreas", "digestive", "gastro", "gut", "diarrhea", "constipation", "hepatic"],
        "Bones, Joints & Muscles": ["bone", "fracture", "lumbar", "disc", "muscle", "joint", "orthopedic", "skeletal", "spine", "arthritis", "rickets", "osteoporosis", "pelvic", "scoliosis"],
        "Skin & Dermatological": ["skin", "melanoma", "rash", "pigmentation", "aplasia cutis", "dermatitis", "bruis", "acne", "ulcer", "hair", "nail", "dermal", "keratoderma"],
        "Endocrine & Metabolic": ["diabetes", "thyroid", "cortisol", "vitamin", "metabolic", "hormone", "endocrine", "pcos", "weight", "obesity", "hypothyroidism", "hyperthyroidism", "a1c"],
        "Eyes, Ears, Nose & Throat": ["cornea", "cataract", "bad breath", "hearing", "vision", "eye", "ear", "dental", "tooth", "mouth", "throat", "nasal", "sinus", "gaze", "optic", "macular"],
        "General Health & Oncology": ["cancer", "tumor", "carcinoma", "oncology", "leukemia", "lymphoma", "surgery", "drug", "medication", "pain", "infection", "fever", "vaccine", "pediatric", "injury", "treatment"]
    }
    
    # Simple check for matches. Order defines priority if there are multiple matches.
    # We will score each category based on number of matches in the text.
    scores = {cat: 0 for cat in categories}
    
    for cat, keywords in categories.items():
        for kw in keywords:
            # use a simple regex for word boundaries to avoid overmatching
            pattern = re.compile(r'\b' + re.escape(kw) + r'\b')
            scores[cat] += len(pattern.findall(text))
            
    # Also add scores just based on the question alone (with a multiplier) to prioritize what the question asks
    question_text = str(row['question']).lower()
    for cat, keywords in categories.items():
        for kw in keywords:
            pattern = re.compile(r'\b' + re.escape(kw) + r'\b')
            scores[cat] += 3 * len(pattern.findall(question_text))
            
    best_category = "General Health & Oncology"
    max_score = 0
    for cat, score in scores.items():
        if score > max_score:
            max_score = score
            best_category = cat
            
    return best_category

def main():
    input_file = "aiResDataset.csv"
    output_file = "datasetwithAIResponses_categorized.csv"
    
    df = pd.read_csv(input_file)
    df['question_type'] = df.apply(categorize_question, axis=1)
    
    # Save the new CSV without changing anything else
    df.to_csv(output_file, index=False, encoding='utf-8')
    print("Categorization complete! Saved to", output_file)
    print("Category distribution:")
    print(df['question_type'].value_counts())

if __name__ == "__main__":
    main()
