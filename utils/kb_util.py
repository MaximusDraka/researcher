import pickle
import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.matcher import PhraseMatcher
import re
import json
import os


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


def update_abbreviations(new_mappings: dict):

    """
    Updates the abbreviation mappings dictionary with new key-value pairs.

    Parameters:
    new_mappings (dict): The new key-value pairs to add to the abbreviation mappings.

    Returns:
    None
    """

    # Update mappings	
    abbreviation_mappings.update(new_mappings)

    # Save the updated mappings back to the file
    with open(abbreviation_file_path, "w") as json_file:
        json.dump(abbreviation_mappings, json_file, indent=4)


def get_abbreviations() -> list:

    """
    Returns the abbreviation mappings dictionary.

    Returns:
    dict: The abbreviation mappings dictionary.
    """

    return [key for key in abbreviation_mappings.keys()]


def create_pattern(skill: str) -> list:    
    
    splits = skill.split(' ')    
    pattern = [{'LOWER':word} for word in splits]    
    return pattern


def create_ruler_from_db(model_file_path: str, ruler_filename: str, skill_without_duplicates: list, save: bool=True) -> PhraseMatcher:
    
    nlp = English()    
    ruler = nlp.add_pipe("entity_ruler")    
    ruler.add_patterns([{'label': 'SKILL', 'pattern': create_pattern(skill)}  for skill in skill_without_duplicates])
                
    if save:   
        
        nlp.to_disk(model_file_path)
        
        if os.path.exists(ruler_filename):
            os.remove(ruler_filename)  
        
        ruler.to_disk(ruler_filename)
    return ruler


def create_matcher_from_db(matcher_filename: str, skill_without_duplicates: list, save: bool=True) -> PhraseMatcher:
    
    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = list(nlp.pipe(skill_without_duplicates))
    matcher.add("SKILL", patterns) 
    
    
            
    if save:        
        
        if os.path.exists(matcher_filename):
            os.remove(matcher_filename)  
        
        pickle.dump(matcher, open(matcher_filename, 'wb'), protocol=5)
                
        
    return matcher


def load_matcher_from_file(filename: str) -> PhraseMatcher:
    
    loaded_matcher = pickle.load(open(filename, 'rb'))
    
    return loaded_matcher


def read_vocabulary(filename: str) -> list:
    
    with open(filename, 'r') as file:
        lines = file.read().splitlines() 

    new_list = []

    for item in lines:
        if item.lower() not in new_list:
            new_list.append(item.lower().strip())
            
    return new_list


def create_patterns(vocabulary: list, label: str) -> list:
    
    patterns = []
  
    for item in vocabulary:
        data_item = {"label": label, "pattern":item}
        if data_item not in patterns:       
            patterns.append(data_item)
    return patterns


def get_vocabulary() -> list:
    
    voc_1 = read_vocabulary('C:/Users/tom/projects/skill-skeleton/data/kb/hot_skills.txt')
    voc_2 = read_vocabulary('C:/Users/tom/projects/skill-skeleton/data/kb/cold_skills.txt')
    voc_3 = read_vocabulary('C:/Users/tom/projects/skill-skeleton/data/kb/linkedin-skills.txt')

    return voc_1 + voc_2 + voc_3 
 

def get_ict_list() -> list:
    
    return [x.lower() for x in ['sql server analysis services','sql server integration services','sql server reporting services','critical thinking','dashboarding','use cases','prototyping','functiona requirements','business requirements','user acceptance testing','business process modeling','quality assurance','resource allocation','graphic design','prototyping','data-driven decision-making',
            'social media marketing','risk assessment and mitigation','cybersecurity','threat detection measures','Adobe Creative Suite',
            'project planning','RESTful APIs','UX/UI','data governance','data warehousing','time series forecasting','sentiment analysis',
            'data storytelling','data blending','data querying','data cleaning','Kubernetes','Shell','Big data','Business Intelegence',
            'Latex','Algorithms','Reasearch analytics','Data mining','regression analysis','statistical analysis',
            'data transformation techniques','machine learning','deep learning','computer vision','Natural Language Processing', 'optimization', 
            'linear algebra','calculus','statistics','probability','mathematics','data analysis', 'data visualization','modeling','data structures' ,
            'Blockchain','Cryptography','Smart contracts','Networking','DML','Rest Web Services','Windows','technical assistance','UNIX',
            'Citrix Xen Server','Web Application testing','Cyara','Linux','Nagios','Software Testing','Eclipse','Sonar Qube','C#.net',
            'Apache','Data Modeling','java servlet','Selenium Webdriver','Web Development','Internet Of Things',
            'R Studio','MS Project','MS Outlook','MS Office','CCNA','ipsec','Android','HSRP','CPP','Application Designer',
            'NetBeans','Cloud Computing','OpenShit','Web Designing','Jdeveloper','computer and firesafety',
            'CISCO','SQL developer','Computer Networks','Ansible','Ansible','Bootstrap','APPLICATION SOFTWARE','Micro Services',
            'Putty','SPUFI','Agile','Hacking','bgp','AMDP','Artificial Intelligence',
            'mpls','Program Management','Kibana','Maven','Open VZ','Hibernate','cricket','Automation','Lithium','JSON',
            'Socket Programming','EJB','Nexus','Html5','Hyper-','Servlet','JMS','multicast','Windows Services','Hardware & Networking','SAPUI5',
            'Gephi','Object Oriented Programming','Struts','active directory',
            'Postman','VB',' SAPUI5 (Primary Skill)','Market Basket Analysis',
            'Web Authoring Tools HTML 5','Vportal','Network Management','Inversion of Control',
            'Ajax & JQuery','programming','problem solving','Functional Testing','Octopus','PL/SQL Developer','Windows XP','ospf',
            'work devotee','APACHE','Android Studio','Exchange','Predictive Modelling','KVM','CRM',
            'RESOURCE PLANNING','STL','Domain Name System','Mac','kannada','IT Literacy','SIEM','Highly Dedicated towards work','Ansys',
            'Bid management','Wireshark','Adobe Flex','XML','Tally','TestNG',
            'Data Driven','Marathi','SVN','wsus','Oracle System upgrades',
            'Mobile Applications','Page Object model','Design Patterns','Typewriting','Network Security','Project management','D3js','Automation Testing',
            'Bamboo','Scrum','Service Virtualization','WAF','Relay server','Sauce Labs','Java & J2EE',
            'Computer Hardware','Catia V6','Mobile Testing','McAfee ESM',
            'putty','R studio','Microsoft Visual Studio','Ubuntu Linux','Ajax','ADF','Syslog sender','tcl',
            'Adobe Photoshop','Database Management System','HttpClient',
            'RADTool','Jenkins','Cisco Monitoring Tools: EM7','Sublime','Mockito',
            'Creative Team Leadership','WinSCP','l3vpn','Clustering','Metalogix','Sharegate','Iterative Development','Data Structures & Algorithms',
            'Jackson-2','SDET','Cucumber','Inside Sales','jdbc','Oracle PeopleSoft','DHCP','E-commerce','SOAP Web Services','SOAP UI',
            'Tomcat','ESXi','Programming','GitLab','Windows 7','Salesforce','Multimedia','Analytical and logical skills','Windows 8',
            'Software Development Life Cycle','JSP','REST','Junit','Power Center','Spring MVC','Sentimental Analysis','FlexBuilder',
            'Middleware MVC and WCF','Tortoise SVN','Waterfall','Oracle SQL Developer','kabbadi','SOAP','QMF','MS Visio',
            'ABAP/4','o365','ClouStack','Jira','ORM Eclipse Link','Xpeditor','MainView','software integration','Apache Nifi','SAP ABAP','SAP HANA','QTP','Copilot','Large Language Model','Grafical Neural Network']] 


def get_profiles() -> list:
    
    return ['Data Engineer','Data Scientist','Data Analyst','Business Analyst','Software Engineer','Machine Learning Engineer','Cloud Engineer']

def get_skill_categories() -> list:
    
    return ['Languages','Tools','Databases','Cloud','Libraries','Frameworks']


def get_skill_languages() -> list:
    
    return [x.lower() for x in ['SQL','Python','R','C','C#','JavaScript','JS','Java','Scala','SAS','MATLAB','C++','C / C++','Perl','TypeScript','Bash','HTML','CSS','PHP','Powershell','Rust', 'Kotlin','Ruby','Dart','Assembly','Swift','VBA','Lua','Groovy','Delphi','Objective-C','Haskell','Elixir','Julia','Clojure','Solidity','Lisp','F#','Fortran','Erlang','APL','COBOL','OCaml','Crystal','Golang','NoSQL','Transact-SQL','No-SQL','Visual Basic','Pascal', 'Mongo', 'PL/SQL','Sass','VB.NET','MSSQL']]


def get_skill_tools() -> list:
    
    return [x.lower() for x in ['ETL','GIT','Docker','Tableau','MS Excel','Power BI','MS Word','MS PowerPoint','SAP','SSIS','Looker','Qlik','Alteryx','SPSS','SSRS','DAX','SharePoint','Splunk','Cognos','Visio','Google Sheets','Spreadsheets','MS Access','DataRobot','Nuix','Esquisse']]
    

def get_skill_databases() -> list:
    
    return [x.lower() for x in ['MS SQL Server','MYSQL','Cassandra','PostgreSQL','MongoDB','Elasticsearch','DynamoDB','Redis','DB2','Neo4j','MariaDB','Firebase','Firestore','CouchDB','SQLite','HBase','Teradata','Oracle','Hive','Redshift','Snowflake','RDBMS']]
    
    
def get_skill_cloud() -> list:
    
    return [x.lower() for x in ['Azure','Google Cloud Platform','AWS Cloud','Amazon Web Services','Databricks','BigQuery','Aurora','VMware','IBM Cloud','Watson','Openstack','Heroku','Colocation','OVH','Linode']]


def get_skill_libraries() -> list:
    
    return [x.lower() for x in ['Spark','Hadoop','Kafka','Airflow','PySpark','Pandas','TensorFlow','PyTorch','Numpy','Scikit-learn','Keras','Jupyter','React','Matpltlib','Spring','GDPR','Plotly','Seaborn','GraphQL','NLTK','OpenCV','ggplot2','Selenium','MXNet','Tidyverse','RShiny','Hugging Face','Spacy','NetworkX']]


def get_skill_frameworks() -> list:
    
    return [x.lower() for x in ['Scrum framework','Express.js','Node.js','Angular','Flask','Django','Vue.js','Phoenix','FASTAPI','jQuery','ASP.NET','Ruby on Rails','React.js','Laravel','Next.js','Angular.js','Drupal','Svelte','Symfony','Blazor','Gatsby','Fastify','Ember.js','Nuxt.js','Deno']]


def get_all_skills() -> list:
    
    return list(dict.fromkeys(get_ict_list() + get_skill_languages() + get_skill_tools() + get_skill_databases() + get_skill_cloud() + get_skill_libraries() + get_skill_frameworks()))

