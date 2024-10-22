import json
import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models
from .config import settings
import logging
import re

# Path to the JSON file
json_file_path = './data-folder/scraped_data.json'

def clean_text(text):
    """Removes punctuation and unnecessary special characters from the text."""
    return re.sub(r'[^\w\s]', '', text).strip().lower()

def get_relevant_data(question: str):
    try:
        # Clean the question text
        clean_question = clean_text(question)

        # Load the JSON data from the file
        if os.path.exists(json_file_path):
            logging.info(f"JSON file found at: {json_file_path}")
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data_list = json.load(json_file)
                logging.info(f"Loaded {len(data_list)} items from JSON.")

                # Search for the question in the JSON data
                for item in data_list:
                    title = item.get('title', '')
                    paragraphs = item.get('paragraphs', '')
                    headings_h1 = item.get('headings', {}).get('h1', '')
                    headings_h2 = item.get('headings', {}).get('h2', '')
                    headings_h3 = item.get('headings', {}).get('h3', '')
                    
                    # Clean the text fields in the JSON before comparison
                    clean_title = clean_text(title)
                    clean_paragraphs = clean_text(paragraphs)
                    clean_h1 = clean_text(headings_h1)
                    clean_h2 = clean_text(headings_h2)
                    clean_h3 = clean_text(headings_h3)
                    
                    # Log the data being checked
                    logging.info(f"Checking: Title='{title}', Paragraphs='{paragraphs}', H1='{headings_h1}', H2='{headings_h2}', H3='{headings_h3}'")

                    # Check if the cleaned question matches any of these fields
                    if (clean_question in clean_title or
                        clean_question in clean_paragraphs or
                        clean_question in clean_h1 or
                        clean_question in clean_h2 or
                        clean_question in clean_h3):
                        
                        # Log a match
                        logging.info(f"Match found for: {question}")
                        
                        # Return the relevant content and URL
                        url = item.get('url', 'No URL available')
                        content = f"Title: {title}\nParagraph: {paragraphs}\nHeading H1: {headings_h1}"
                        return content, url
                    
        else:
            logging.error(f"JSON file not found at: {json_file_path}")

        # If no match found, return None
        logging.info(f"No match found for: {question}")
        return None, None
    
    except Exception as e:
        logging.error(f"Error occurred while processing JSON: {str(e)}")
        raise