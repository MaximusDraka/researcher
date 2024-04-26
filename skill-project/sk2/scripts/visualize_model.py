import typer
import sys  
sys.path.insert(1, 'C:/Users/tom/projects/skill-skeleton/utils')
import spacy
import spacy_streamlit


def main(models: str, default_text: str):
   models = [name.strip() for name in models.split(",")]
   spacy_streamlit.visualize(models, default_text, visualizers=["ner"], ner_labels=["SKILL"])

    #nlp = spacy.load("training/model-ruler")
    #doc = nlp(default_text)
    #spacy_streamlit.visualize_ner(doc, labels=nlp.get_pipe("entity_ruler").labels)


if __name__ == "__main__":
    try:
        typer.run(main)
    except SystemExit:
        pass