from pathlib import Path
import pandas as pd
import PyPDF2

file_path = Path('.\\output\\')
pdf_files = list(file_path.glob('*.pdf'))


def clean_book():
    #Clean txt.file
    with open('./output/text_pdf.txt', 'w', encoding="utf-8") as f:
        f.close()


def create_txt():
    #Creating txt file with first page data pdf_files
    for pdf in pdf_files:
        open_file = open(pdf, 'rb')
        pdfreader = PyPDF2.PdfFileReader(open_file)
        page = pdfreader.getPage(0)
        text = page.extractText()
        with open('./output/text_pdf.txt', 'a+',  encoding="utf-8") as f:
            f.writelines(str(text))
            f.close()


#Getting values
list_investment = []
list_UII = []


def get_values():
   with open('./output/text_pdf.txt', encoding='utf-') as f:
        word_name_investment = '1. Name of this Investment:'
        word_UII = '2. Unique Investment Identifier (UII):'
        lines = "".join(line for line in f if not line.isspace())
        list = lines.split('\n')
        length = len(list)
        i = 0
        while i < length:
            if list[i] == word_name_investment:
                list_investment.append(list[i+1])
            if list[i] == word_UII:
                list_UII.append(list[i+1])
            i += 1


def field_comprasion():
    #Field comparison
    dictionary_investment_from_pdf = dict(zip(list_investment, list_UII))
    xl_file = pd.read_excel('./output/National Science Foundation_Individual_investments.xlsx', sheet_name='Sheet1')
    Investment_Title = xl_file['Investment Title'].tolist()
    UII = xl_file['UII'].tolist()
    dictionary_investment_from_exel = dict(zip(Investment_Title, UII))


    for key, value in dictionary_investment_from_exel.items():
        if not dictionary_investment_from_pdf.get(key):
            print(f'In {value} no attached pdf file')
        elif dictionary_investment_from_pdf.get(key) == value:
            print(f'The value of the fields is present in the table and they match with pdf file.{key}:{value}')
        else:
            print('Name of this Investment equal Investment Title')
            print('Unique Investment Identifier (UII) not equal value in column UII')



def task():
    clean_book()
    create_txt()
    get_values()
    field_comprasion()


if __name__ == '__main__':
    task()