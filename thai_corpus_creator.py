#!/usr/bin/env python3
import csv
import json
import os
from collections import Counter

# Source and target paths
TNC_CSV_PATH = "/tmp/carpalx-th/data/tnc5000_withfreq.csv"
THAISUM_PATH = "/tmp/carpalx-th/data/thaisum-full.json"
OUTPUT_DIR = "static/language_data_raw"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "thai.json")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to extract n-grams from text
def get_ngrams(text, n):
    return [text[i:i+n] for i in range(len(text) - n + 1)]

# A function to create a Thai corpus JSON file with character frequencies
def create_thai_corpus():
    print(f"Creating Thai corpus JSON file from TNC data...")
    raw_text = ""
    
    # First try the TNC CSV file (which has full words)
    try:
        with open(TNC_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word']
                freq = int(float(row['freq']))
                # Repeat words based on frequency to get accurate character distribution
                repetition = min(freq // 1000, 10)
                if repetition < 1:
                    repetition = 1
                raw_text += (word + " ") * repetition
    except Exception as e:
        print(f"Error reading TNC file: {e}")
    
    # If that fails or doesn't provide enough data, use the ThaiSum data
    if len(raw_text) < 10000:
        try:
            with open(THAISUM_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ngram, freq in data.items():
                    # Skip very long n-grams
                    if len(ngram) > 10:
                        continue
                    # Add n-grams based on frequency
                    repetition = min(freq // 1000, 10)
                    if repetition < 1:
                        repetition = 1
                    raw_text += (ngram + " ") * repetition
        except Exception as e:
            print(f"Error reading ThaiSum file: {e}")
    
    # Remove spaces for character counts but keep original text for n-grams
    char_text = raw_text.replace(" ", "")
    
    # Count frequencies
    char_count = Counter(char_text)
    bigram_count = Counter(get_ngrams(char_text, 2))
    trigram_count = Counter(get_ngrams(char_text, 3))
    
    # Calculate total counts
    total_chars = sum(char_count.values())
    total_bigrams = sum(bigram_count.values())
    total_trigrams = sum(trigram_count.values())
    
    # Calculate frequencies as decimal values
    char_freqs = {char: count / total_chars for char, count in char_count.items()}
    bigram_freqs = {bigram: count / total_bigrams for bigram, count in bigram_count.items()}
    trigram_freqs = {trigram: count / total_trigrams for trigram, count in trigram_count.items()}
    
    # Create the final JSON object
    result = {
        "language": "thai",
        "characters": char_freqs,
        "bigrams": bigram_freqs,
        "trigrams": trigram_freqs
    }
    
    # Write to JSON file
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Thai corpus JSON created at {OUTPUT_PATH}")
    print(f"Total unique characters: {len(char_freqs)}")
    print(f"Total unique bigrams: {len(bigram_freqs)}")
    print(f"Total unique trigrams: {len(trigram_freqs)}")
    
    # Print the top 10 most frequent characters
    top_chars = sorted(char_freqs.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop 10 most frequent characters:")
    for char, freq in top_chars:
        print(f"{char}: {freq:.4f}")
    
    # Print the top 10 most frequent bigrams
    top_bigrams = sorted(bigram_freqs.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop 10 most frequent bigrams:")
    for bigram, freq in top_bigrams:
        print(f"{bigram}: {freq:.4f}")

if __name__ == "__main__":
    create_thai_corpus() 