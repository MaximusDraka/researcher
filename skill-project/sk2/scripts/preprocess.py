import typer
import spacy
from pathlib import Path
import sys  
sys.path.insert(1, 'C:/Users/tom/projects/skill-skeleton/utils/')
import spacy_util


def main(
    input_path: str = typer.Argument(..., exists=True, dir_okay=False),
    output_path: str = typer.Argument(..., dir_okay=False),
):
   
   nlp = spacy.blank("en")
   db = spacy_util.from_ner_annotator_to_spacy(nlp,input_path)
   db.to_disk(output_path)


if __name__ == "__main__":
    typer.run(main)
