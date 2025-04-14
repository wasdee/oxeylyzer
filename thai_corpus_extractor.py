#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///

import json
import os
import shutil
from collections import defaultdict

# Source and target paths
CARPALX_TH_PATH = "/tmp/carpalx-th/data"
OXEYLYZER_THAI_PATH = "static/language_data_raw/thai.json"

# Load Thai trigram/character frequency data
def extract_thai_corpus():
    # Try to load from thaisum-full.json as primary source
    source_file = os.path.join(CARPALX_TH_PATH, "thaisum-full.json")
    
    print(f"Loading Thai corpus data from {source_file}")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to the format Oxeylyzer expects
    # Oxeylyzer expects a dictionary of character or ngram -> frequency
    formatted_data = {}
    
    # Process single characters and bigrams/trigrams
    for key, frequency in data.items():
        formatted_data[key] = frequency
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OXEYLYZER_THAI_PATH), exist_ok=True)
    
    # Write the output file
    with open(OXEYLYZER_THAI_PATH, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)
    
    print(f"Thai corpus data exported to {OXEYLYZER_THAI_PATH}")
    print(f"Number of entries: {len(formatted_data)}")

# Extract Thai layouts from carpalx-th
def extract_thai_layouts():
    kedmanee = [
        ["ๅ", "/", "_", "ภ", "ถ", "ุ", "ึ", "ค", "ต", "จ", "ข", "ช"],
        ["ๆ", "ไ", "ำ", "พ", "ะ", "ั", "ี", "ร", "น", "ย", "บ", "ล", "ฃ"],
        ["ฟ", "ห", "ก", "ด", "เ", "้", "่", "า", "ส", "ว", "ง"],
        ["ผ", "ป", "แ", "อ", "ิ", "ื", "ท", "ม", "ใ", "ฝ"],
        ["+", "๑", "๒", "๓", "๔", "ู", "฿", "๕", "๖", "๗", "๘", "๙"],
        ["๐", '"', "ฎ", "ฑ", "ธ", "ํ", "๊", "ณ", "ฯ", "ญ", "ฐ", ",", "ฅ"],
        ["ฤ", "ฆ", "ฏ", "โ", "ฌ", "็", "๋", "ษ", "ศ", "ซ", "."],
        ["(", ")", "ฉ", "ฮ", "ฺ", "์", "?", "ฒ", "ฬ", "ฦ"],
    ]
    
    pattachote = [
        ["๛", "๒", "๓", "๔", "๕", "ู", "๗", "๘", "๙", "๐", "๑", "๖"],
        ["็", "ต", "ย", "อ", "ร", "่", "ด", "ม", "ว", "แ", "ใ", "ฌ", "ฃ"],
        ["้", "ท", "ง", "ก", "ั", "ี", "า", "น", "เ", "ไ", "ข"],
        ["บ", "ป", "ล", "ห", "ิ", "ค", "ส", "ะ", "จ", "พ"],
        ["1", '"', "/", ",", "?", "ุ", "_", ".", "(", ")", "-", "%"],
        ["๊", "ฤ", "ๆ", "ญ", "ษ", "ึ", "ฝ", "ซ", "ถ", "ฒ", "ฯ", "ฦ", "ฅ"],
        ["๋", "ธ", "ำ", "ณ", "์", "ื", "ผ", "ช", "โ", "ฆ", "ฑ"],
        ["ฎ", "ฏ", "ฐ", "ภ", "ั", "ศ", "ฮ", "ฟ", "ฉ", "ฬ"],
    ]
    
    manoonchai = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
        ["ใ", "ต", "ห", "ล", "ส", "ป", "ั", "ก", "ิ", "บ", "็", "ฬ", "ฯ"],
        ["ง", "เ", "ร", "น", "ม", "อ", "า", "่", "้", "ว", "ื"],
        ["ุ", "ไ", "ท", "ย", "จ", "ค", "ี", "ด", "ะ", "ู"],
        ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"],
        ["ฒ", "ฏ", "ซ", "ญ", "ฟ", "ฉ", "ึ", "ธ", "ฐ", "ฎ", "ฆ", "ฑ", "ฌ"],
        ["ษ", "ถ", "แ", "ช", "พ", "ผ", "ำ", "ข", "โ", "ภ", '"'],
        ["ฤ", "ฝ", "ๆ", "ณ", "๊", "๋", "์", "ศ", "ฮ", "?"],
    ]
    
    # Create layout directory if it doesn't exist
    layouts_dir = "static/layouts"
    os.makedirs(layouts_dir, exist_ok=True)
    
    # Create layout files
    def save_layout(name, layout_matrix):
        layout_path = os.path.join(layouts_dir, f"{name}.json")
        # Converting to the format Oxeylyzer might expect
        # This is a simplified format and may need adjustment
        layout_data = {
            "name": name,
            "matrix": layout_matrix
        }
        
        with open(layout_path, 'w', encoding='utf-8') as f:
            json.dump(layout_data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved layout {name} to {layout_path}")
    
    # Save the layouts
    save_layout("kedmanee", kedmanee)
    save_layout("pattachote", pattachote)
    save_layout("manoonchai", manoonchai)
    
    # Print some stats
    print("\nThai layouts extracted:")
    print("1. Kedmanee: Traditional Thai layout")
    print("2. Pattachote: Alternative Thai layout")
    print("3. Manoonchai: Optimized Thai layout")
    
    # Print instructions
    print("\nTo use these layouts in Oxeylyzer, use the following commands:")
    print("1. cargo run")
    print("2. load thai --raw")
    print("3. generate kedmanee 1000")
    print("4. stats")

if __name__ == "__main__":
    extract_thai_corpus()
    extract_thai_layouts() 