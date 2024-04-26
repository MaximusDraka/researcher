import sys  
sys.path.insert(1, 'C:/Users/tom/projects/skill-skeleton/utils')

import spacy_streamlit

models = ["en_core_web_sm", "en_core_web_md"]
default_text = "Sundar Pichai is the CEO of Google."
spacy_streamlit.visualize(models, default_text)


#streamlit run demo.py