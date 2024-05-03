import re
import json
import os
import pypdf as PyPDF

# Get the path of the current directory
package_dir = os.path.dirname(os.path.abspath(__file__))

# Load abbreviation mappings
abbreviation_file_path = os.path.join(package_dir, "abbreviation_mappings.json")
with open(abbreviation_file_path, "r") as json_file:
    abbreviation_mappings = json.load(json_file)


def fix(text: str, mode: str = 'slim'):
    
    """
    Fixes the abbreviated input text by replacing abbreviations, removing punctuations and hashtag terms.

    Parameters:
    text (str): The input abbreviated text to be fixed.
    
    Returns:
    str: The fixed text.

	
    """
    if mode == 'full':
        # Remove punctuations, emojis and hashtags
        text_punc = re.sub(r' *[<3#][^ ]* *', '', text)
        text_punc = re.sub(r'[^a-zA-Z0-9\']+', ' ', text_punc).strip()
    else:
        text_punc = text

    # Split text into words    
    words = text_punc.split()

    # Convert words to lowercase
    normalized_words = [word.lower() for word in words]
    
    # Replace abbreviations with their full forms
    words_fixed = [abbreviation_mappings.get(word, word) for word in normalized_words]
    
    text_fixed = ' '.join(words_fixed)

    
    # Return processes string
    return text_fixed

def read_PDF(file_path: str) -> str:
    
    fFileObj = open(file_path, 'rb')
    pdfReader = PyPDF.PdfReader(fFileObj)
    #print("Total Pages : {} ".format(len(pdfReader.pages))

    file_content = ""
    for page in pdfReader.pages:
        file_content += page.extract_text()       

    fFileObj.close()
    return file_content