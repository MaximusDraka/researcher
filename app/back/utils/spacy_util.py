import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.tokens import DocBin
import json
import pandas as pd
import string

def remove_punctuation(input_string: str) -> str:
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result


def print_spacy(nlp: spacy, db: DocBin):
    
    docs = list(db.get_docs(nlp.vocab))
    for doc in docs:
        displacy.render(doc, style="ent", jupyter=True)


def from_ner_annotator_to_spacy(nlp: spacy, filename: str) -> DocBin:
    
    with open(filename, 'r') as f:
        data = json.load(f)
            
    db = DocBin()
    for text, annotations in data:
        print(text)
        doc = nlp(text)
        ents = []
        if len(annotations["entities"]) > 0:
            for start, end, label in annotations["entities"]:
                span = doc.char_span(start, end, label=label)
                ents.append(span)
            doc.ents = ents
            db.add(doc)
    
    return db


def CSV_to_NER_annotator(nlp: spacy, matcher: Matcher, input_file: str, data_column: str,delimiter: str='|', output_file: str='output.json'):
    
    data = {"classes":[],"annotations":[]}    
    
    if input_file.split(".")[-1] == "txt":
        
        with open(input_file,'r',encoding='utf-8') as f:
            lines = f.readlines()   
        
        
        for line in lines:        
            line = line.strip()
            if line == "":
                continue
            else:
                text = line            
                doc = nlp(line)   
                matches = matcher(doc, as_spans=True)
                filtered_spans = spacy.util.filter_spans(matches)     
                
                entities = {"entities":[]}
                for span in filtered_spans:                
                                    
                    entities["entities"].append([span.start_char,span.end_char,span.label_])                        
                
                if span.label_ not in data["classes"]:
                    data["classes"].append(span.label_)
                
                data["annotations"].append([text,entities])
    else:
        print("The input file is a CSV file")
                
        df = pd.read_csv(input_file,delimiter=delimiter,dtype={'data': str})
        
        
        print(df.columns)      
    
        for index,row in df.iterrows():   
                      
            text = row[data_column]
            
            print(index,text)     
            
            doc = nlp(text)   
            matches = matcher(doc, as_spans=True)
            filtered_spans =spacy.util.filter_spans(matches)     
            
            entities = {"entities":[]}
            for span in filtered_spans:                
                                
                entities["entities"].append([span.start_char,span.end_char,span.label_])                        
            
                if span.label_ not in data["classes"]:
                    data["classes"].append(span.label_)
            
            data["annotations"].append([text,entities])
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
        
    


def CSV_to_TXT(input_file: str, data_column: int=0,delimiter: str='|', output_file: str='output.txt'):
    
    output_txt = []
    df = pd.read_csv(input_file,delimiter='|')
    for index,row in df.iterrows():                
        output_txt.append(row[data_column]+'\n')
    
    with open(output_file, 'w') as f:
        for line in output_txt:
            f.write(line)   