import pandas as pd
import sys

def main():
    train_file = 'train.xlsx'
    medaesqa_file = 'merged_dataset.csv'
    output_train_csv = 'train_cleaned.csv'

    print(f"Loading {train_file}...")
    try:
        df_train = pd.read_excel(train_file)
    except Exception as e:
        print(f"Error reading {train_file}: {e}")
        sys.exit(1)

    print(f"Original shape: {df_train.shape}")
    
    df_train_cleaned = df_train.drop_duplicates(subset=['Question']).copy()
    print(f"Shape after removing duplicate questions: {df_train_cleaned.shape}")

    print(f"Saving cleaned train dataset to {output_train_csv}...")
    df_train_cleaned.to_csv(output_train_csv, index=False, encoding='utf-8')

    df_sample = df_train_cleaned.sample(n=100, random_state=42).copy()
    
    # Mapping new columns to existing columns
    df_sample.rename(columns={
        'Question': 'question',
        'Answer': 'reference_answer'
    }, inplace=True)
    

    print(f"Loading {medaesqa_file}...")
    try:
        df_medaes = pd.read_csv(medaesqa_file)
    except Exception as e:
        print(f"Error reading {medaesqa_file}: {e}")
        sys.exit(1)

    print(f"Original medaesqa shape: {df_medaes.shape}")
    
    df_sample = df_sample[['question', 'reference_answer']]
    
    # Append the 100 questions
    df_combined = pd.concat([df_medaes, df_sample], ignore_index=True)
    #print(f"Combined medaesqa shape: {df_combined.shape}")

    #print(f"Saving merged dataset back to {medaesqa_file}")
    df_combined.to_csv(medaesqa_file, index=False, encoding='utf-8')
    #print("All tasks finished successfully.")

if __name__ == '__main__':
    main()
