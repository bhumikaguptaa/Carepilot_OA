import json
import pandas as pd
import sys
import re

def main():
    input_file = 'medaesqa_v1.json'
    output_file = 'merged_dataset.csv'

    print("Loading JSON data...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    extracted_data = []
    for item in data:
        question = item.get('question', '')
        
        question_frame = item.get('question_frame') or {}
        #question_type = question_frame.get('Type', '')
        
        expert_answer = item.get('expert_curated_answer', '')
        machine_answers = item.get('machine_generated_answers', {})
        
        # Remove citation formatting like [123456] or [1234, 5678] from the expert answer
        reference_answer = re.sub(r'\s*\[\s*\d+(?:\s*,\s*\d+)*\s*\]', '', expert_answer)

        row_data = {
            'question': question,
            'expert_curated_answer': reference_answer,
        }
        
        extracted_data.append(row_data)

    print(f"Processing {len(extracted_data)} records...")
    df = pd.DataFrame(extracted_data)
    
    print(f"Saving to {output_file}...")
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
