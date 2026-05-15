import json
import re
import os
import csv

def parse_vocabulary(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]

    vocabulary = []
    current_entry = []
    current_index = None
    
    # Skip header
    # #	ごい	Vocabulary	Type	Meaning
    start_index = 1
    
    i = start_index
    while i < len(lines):
        line = lines[i]
        # Match a line that is just a number (the index of the word)
        if re.match(r'^\d+$', line):
            if current_entry:
                vocabulary.append(process_entry(current_entry, current_index))
            current_index = line
            current_entry = []
        else:
            if line: # Skip empty lines within entry if they are just whitespace
                current_entry.append(line)
        i += 1
    
    # Add the last entry
    if current_entry:
        vocabulary.append(process_entry(current_entry, current_index))
        
    return vocabulary

def process_entry(lines, index):
    """
    Processes the lines collected for a single entry.
    User note: Kanji always appears just after the figure (index).
    
    Structure A (with Kanji):
    [0] Kanji (上がる)
    [1] Romaji (agaru)
    [2] Reading (あがる)
    [3] Type\tMeaning
    
    Structure B (no Kanji):
    [0] Reading/Kanji (ああ)
    [1] Romaji (aa)
    [2] Type\tMeaning
    """
    entry = {
        "index": index,
        "kanji": "",
        "reading": "",
        "romaji": "",
        "type": "",
        "meaning": ""
    }
    
    if not lines:
        return entry

    # The last line contains Type and Meaning separated by a tab
    last_line = lines[-1]
    if '\t' in last_line:
        entry['type'], entry['meaning'] = last_line.split('\t', 1)
    else:
        entry['meaning'] = last_line

    remaining = lines[:-1]
    
    if len(remaining) >= 3:
        # Case with Kanji, Romaji, and Reading
        entry['kanji'] = remaining[0]
        entry['romaji'] = remaining[1]
        entry['reading'] = remaining[2]
    elif len(remaining) == 2:
        # Case without specific "Reading" line: 
        # Line 0 is the Word (could be Kanji or Kana), Line 1 is Romaji
        entry['kanji'] = remaining[0]
        entry['reading'] = remaining[0] # Fallback reading to the word itself
        entry['romaji'] = remaining[1]
    elif len(remaining) == 1:
        # Fallback for very simple entries
        entry['kanji'] = remaining[0]
        entry['reading'] = remaining[0]
        
    return entry

if __name__ == "__main__":
    input_file = r'raw_data\vacabulary.txt'
    output_file = r'data\vocabulary.json'
    js_output_file = r'data\vocabulary.js'
    
    if os.path.exists(input_file):
        data = parse_vocabulary(input_file)
        # Save as JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Save as JS for file:// protocol compatibility
        with open(js_output_file, 'w', encoding='utf-8') as f:
            f.write("const vocabularyData = ")
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write(";")
        
        # Save as CSV
        csv_output_file = r'data\vocabulary.csv'
        if data:
            keys = data[0].keys()
            with open(csv_output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            
        print(f"Successfully parsed {len(data)} words into {output_file}, {js_output_file} and {csv_output_file}")
    else:
        print(f"Error: {input_file} not found")
