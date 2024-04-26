import typer
from rich.table import Table
from rich.console import Console
import json


def cast_item(item:int) -> str:
    if isinstance(item, float):
        item = round(item, 4)
    return str(item)


def print_rich_table(model_name:str, title:str = None) -> None:    
       
    table = Table(title=title)
    table.add_column("Type", style="cyan")
    table.add_column("Precision", style="cyan")
    table.add_column("Recall", style="cyan")
    table.add_column("F1", style="cyan")
   
   
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/"+ model_name +"/meta.json", 'r') as f:
        model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/"+ model_name +"/metrics.json", 'r') as f:
        eval = json.load(f)
   
   #Model        
    p= model['performance']['ents_p']
    r= model['performance']['ents_r']
    f= model['performance']['ents_f']
   
    
    vals = ["Model", cast_item(p), cast_item(r), cast_item(f)]
    table.add_row(*vals)

    #Evaluate
    p= eval['ents_p']
    r= eval['ents_r']
    f= eval['ents_f']
   
    
    vals = ["Eval", cast_item(p), cast_item(r), cast_item(f)]
    table.add_row(*vals)

    console = Console()
    console.print(table)

def main():     
    
    print_rich_table("IT1/model-best-C_R_E", title="IT1 - CPU Raw - Efficiency")
    print_rich_table("All/model-best-C_R_E_F", title="All - CPU Raw - Efficiency - F1")
    print_rich_table("All/model-best-C_R_E_P", title="All - CPU Raw - Efficiency - P")
    print_rich_table("All/model-best-C_R_E_R", title="All - CPU Raw - Efficiency - R")
    
    print_rich_table("IT1/model-best-C_R_A", title="IT1 - CPU Raw - Accuracy")
    print_rich_table("All/model-best-C_R_A_F", title="All - CPU Raw - Accuracy - F1")
    print_rich_table("All/model-best-C_R_A_P", title="All - CPU Raw - Accuracy - P")
    print_rich_table("All/model-best-C_R_A_R", title="All - CPU Raw - Accuracy - R")
    
    print_rich_table("IT1/model-best-C_PT_E", title="IT1 - CPU Pretrained - Adam")
    print_rich_table("All/model-best-C_PT_E_F", title="All - CPU Pretrained - Adam - F1")
    print_rich_table("All/model-best-C_PT_E_P", title="All - CPU Pretrained - Adam - P")
    print_rich_table("All/model-best-C_PT_E_R", title="All - CPU Pretrained - Adam - R")
    
    
    print_rich_table("IT1/model-best-C_PT_E_HP", title="IT1 - CPU Pretrained - Smaller Batcher and RAdam")    
    print_rich_table("All/model-best-C_PT_E_HP_F", title="All - CPU Pretrained - Smaller Batcher and RAdam - F1")    
    print_rich_table("All/model-best-C_PT_E_HP_P", title="All - CPU Pretrained - Smaller Batcher and RAdam - P")
    print_rich_table("All/model-best-C_PT_E_HP_R", title="All - CPU Pretrained - Smaller Batcher and RAdam - R")
    
    
    #print_rich_table("IT2/model-best-C_R_E", title="IT2 - CPU Raw - Efficiency")
    #print_rich_table("IT2/model-best-C_R_A", title="IT2 - CPU Raw - Accuracy")
    #print_rich_table("IT2/model-best-C_PT_E", title="IT2 - CPU Pretrained - Adam")
    #print_rich_table("IT2/model-best-C_PT_E_HP", title="IT2 - CPU Pretrained - Smaller Batcher and RAdam")
    

if __name__ == "__main__":
    typer.run(main)