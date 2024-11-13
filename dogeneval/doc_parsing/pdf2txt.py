import PyPDF2
import pypandoc
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal
from tqdm import tqdm
import re


def parse_pdf_v1(input_path, output_path):
    pdf_file = open(input_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    pdf_file.close()
    text = pypandoc.convert_text(text, 'md', format='html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)


def parse_pdf(input_path, output_path, show_progress=False):
    manager = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(manager, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, device)

    text_content = ''
    with open(input_path, 'rb') as f:
        for page in tqdm(PDFPage.get_pages(f), desc="Processing pages", disable=not show_progress):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text_content += element.get_text()

    lines = text_content.split('\n')
    new_lines = []
    for line in lines:
        if re.search('[。！.!]$', line):
            new_lines.append(line + '\n\n')
        else:
            new_lines.append(line + '')
    text = ''.join(new_lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    input_path = '/home/junetheriver/codes/qa_generation/huawei/data/zabbix/Zabbix_Documentation_4.0.zh.pdf'
    output_path = '/home/junetheriver/codes/qa_generation/huawei/data/zabbix/Zabbix_Documentation_4.0.zh.txt'
    parse_pdf(input_path, output_path, show_progress=True)