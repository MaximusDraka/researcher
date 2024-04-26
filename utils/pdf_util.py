import pypdf as PyPDF
import numpy as np
import matplotlib.pyplot as plt


def read_PDF(file_path: str) -> str:
    
    fFileObj = open(file_path, 'rb')
    pdfReader = PyPDF.PdfReader(fFileObj)
    #print("Total Pages : {} ".format(len(pdfReader.pages))

    file_content = ""
    for page in pdfReader.pages:
        file_content += page.extract_text()       

    fFileObj.close()
    return file_content


def show_PDF_as_bar_chart(labels: list, values: list):    
    
    fig, ax = plt.subplots()
    y_pos = np.arange(len(labels))
    ax.barh(y_pos, values, align='center')
    ax.set_yticks(y_pos, labels=labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Occurence of labels')
    ax.set_title('Number of labels found in PDF')
    plt.show()