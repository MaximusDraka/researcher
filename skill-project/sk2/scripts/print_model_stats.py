import typer
from rich.table import Table
from rich.console import Console
import json


def cast_item(item:int) -> str:
    if isinstance(item, float):
        item = round(item, 4)
    return str(item)


def print_rich_table(data:list, title:str = None) -> None:    
       
    table = Table(title=title)
    table.add_column("Model", style="cyan")
    table.add_column("Precision", style="cyan")
    table.add_column("Recall", style="cyan")
    table.add_column("F1", style="cyan")
    
   
    for d in data:
        
        p= d['performance']['ents_p']
        r= d['performance']['ents_r']
        f= d['performance']['ents_f']
       
        
        vals = [d['model'], cast_item(p), cast_item(r), cast_item(f)]
        table.add_row(*vals)

    console = Console()
    console.print(table)


def main():
        
      
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT1/model-best-C_R_E/meta.json", 'r') as f:
        C_R_E_data_IT1_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT1/model-best-C_R_A/meta.json", 'r') as f:
        C_R_A_data_IT1_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT1/model-best-C_PT_E/meta.json", 'r') as f:
        C_PT_E_data_IT1_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT1/model-best-C_PT_E_HP/meta.json", 'r') as f:
        C_PT_E_HP_data_IT1_model = json.load(f)
     
      
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT2/model-best-C_R_E/meta.json", 'r') as f:
        C_R_E_data_IT2_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT2/model-best-C_R_A/meta.json", 'r') as f:
        C_R_A_data_IT2_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT2/model-best-C_PT_E/meta.json", 'r') as f:
        C_PT_E_data_IT2_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/IT2/model-best-C_PT_E_HP/meta.json", 'r') as f:
        C_PT_E_HP_data_IT2_model = json.load(f)
    
    
    
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_R_E_F/meta.json", 'r') as f:
        C_R_E_F_data_ALL_model = json.load(f)
        
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_R_E_P/meta.json", 'r') as f:
        C_R_E_P_data_ALL_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_R_E_R/meta.json", 'r') as f:
        C_R_E_R_data_ALL_model = json.load(f)
        
        
    
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_R_A_F/meta.json", 'r') as f:
        C_R_A_F_data_ALL_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_R_A_P/meta.json", 'r') as f:
        C_R_A_P_data_ALL_model = json.load(f)
        
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_R_A_R/meta.json", 'r') as f:
        C_R_A_R_data_ALL_model = json.load(f)
    
    
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_PT_E_F/meta.json", 'r') as f:
        C_PT_E_F_data_ALL_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_PT_E_P/meta.json", 'r') as f:
        C_PT_E_P_data_ALL_model = json.load(f)
        
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_PT_E_R/meta.json", 'r') as f:
        C_PT_E_R_data_ALL_model = json.load(f)
    
    
    
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_PT_E_HP_F/meta.json", 'r') as f:
        C_PT_E_HP_F_data_ALL_model = json.load(f)
        
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_PT_E_HP_P/meta.json", 'r') as f:
        C_PT_E_HP_P_data_ALL_model = json.load(f)
    
    with open("C:/Users/tom/projects/skill-skeleton/skill-project/sk2/training/ALL/model-best-C_PT_E_HP_R/meta.json", 'r') as f:
        C_PT_E_HP_R_data_ALL_model = json.load(f)
        
        
    
    C_PT_E_HP_data_IT1_model['model']="IT1 - CPU Pretrained - Smaller Batcher and RAdam"
    C_PT_E_data_IT1_model['model']="IT1 - CPU Pretrained - Adam"
    C_R_A_data_IT1_model['model']="IT1 - CPU Raw - Accuracy"
    C_R_E_data_IT1_model['model']="IT1 - CPU Raw - Efficiency"
   
    
    C_PT_E_HP_data_IT2_model['model']="IT2 - CPU Pretrained - Smaller Batcher and RAdam"
    C_PT_E_data_IT2_model['model']="IT2 - CPU Pretrained - Adam"
    C_R_A_data_IT2_model['model']="IT2 - CPU Raw - Accuracy"
    C_R_E_data_IT2_model['model']="IT2 - CPU Raw - Efficiency"
   
    
    C_PT_E_HP_F_data_ALL_model['model']="ALL - CPU Pretrained - Smaller Batcher and RAdam - F1"
    C_PT_E_HP_P_data_ALL_model['model']="ALL - CPU Pretrained - Smaller Batcher and RAdam - P"
    C_PT_E_HP_R_data_ALL_model['model']="ALL - CPU Pretrained - Smaller Batcher and RAdam - R"
    
    C_PT_E_F_data_ALL_model['model']="ALL - CPU Pretrained - Adam - F1"
    C_PT_E_P_data_ALL_model['model']="ALL - CPU Pretrained - Adam - P"
    C_PT_E_R_data_ALL_model['model']="ALL - CPU Pretrained - Adam - R"
    
    C_R_A_F_data_ALL_model['model']="ALL - CPU Raw - Accuracy - F1"
    C_R_A_P_data_ALL_model['model']="ALL - CPU Raw - Accuracy - P"
    C_R_A_R_data_ALL_model['model']="ALL - CPU Raw - Accuracy - R"
    
    C_R_E_F_data_ALL_model['model']="ALL - CPU Raw - Efficiency - F1"
    C_R_E_P_data_ALL_model['model']="ALL - CPU Raw - Efficiency - P"
    C_R_E_R_data_ALL_model['model']="ALL - CPU Raw - Efficiency - R"
   
    full_data = [C_PT_E_data_IT1_model, C_R_A_data_IT1_model, C_R_E_data_IT1_model, C_PT_E_HP_data_IT1_model, C_PT_E_F_data_ALL_model, C_PT_E_P_data_ALL_model, C_PT_E_R_data_ALL_model, C_R_A_F_data_ALL_model, C_R_A_P_data_ALL_model, C_R_A_R_data_ALL_model, C_R_E_F_data_ALL_model, C_R_E_P_data_ALL_model, C_R_E_R_data_ALL_model, C_PT_E_HP_F_data_ALL_model,C_PT_E_HP_P_data_ALL_model,C_PT_E_HP_R_data_ALL_model]
   
    print_rich_table(full_data, title="Model Stats")
   

if __name__ == "__main__":
    typer.run(main)