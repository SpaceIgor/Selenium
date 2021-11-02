from pathlib import Path
import pandas as pd
import PyPDF2

file_path = Path('.\\output\\')
pdf_files = list(file_path.glob('*.pdf'))

#Clean txt.file
with open('./output/text_pdf.txt', 'w', encoding="utf-8") as f:
    f.close()

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


#Field comparison
dictionary_investment_from_pdf = dict(zip(list_investment, list_UII))
xl_file = pd.read_excel('./output/National Science Foundation_Individual_investments.xlsx', sheet_name='Sheet1')
Investment_Title = xl_file['Investment Title'].tolist()
UII = xl_file['UII'].tolist()
dictionary_investment_from_exel = dict(zip(Investment_Title, UII))

for key, value in dictionary_investment_from_pdf.items():
    for key_1, value_1 in dictionary_investment_from_exel.items():
        if key in dictionary_investment_from_exel:
            if key == key_1:
                if value == value_1:
                    print('The value of the fields is present in the table and they match')
                else:
                    print('Name of this Investment equal Investment Title')
                    print('Unique Investment Identifier (UII) not equal value in column UII')
        else:
            print('Name of this Investment not in column')














