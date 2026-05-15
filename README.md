# JLPT Vocabulary Learning Tool

This project is a simple interactive tool designed to help users learn Japanese vocabulary for the JLPT exam (starting with N4 level).

## Overview

The tool aims to provide an easy way to memorize Japanese words through a web interface. The vocabulary is sourced from raw text data and converted into a structured format for use in the application.

## Project Structure

- `raw_data/`: Contains the raw text files extracted from web sources.
  - `vacabulary.txt`: Raw N4 vocabulary data.
- `data/`: Contains processed, structured data.
  - `vocabulary.json`: The vocabulary list in JSON format, ready for the web interface.
- `parse_vocabulary.py`: A Python utility script to parse the raw text data into the structured JSON format.
- `index.html`: (Planned) The main interactive interface for learning the words.

## Getting Started

### Data Processing

If the raw data is updated, you can re-run the parser to update the JSON file:

```bash
python parse_vocabulary.py
```

The script handles various entry types (Kanji-based words, Katakana, and Kana-only expressions) and extracts meanings, readings, and word types.

## Future Plans

- Implement a responsive HTML/JavaScript interface.
- Add features for progress tracking and flashcard-style learning.
- Include data for other JLPT levels (N5, N3, etc.).
