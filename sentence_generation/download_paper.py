import random
import os
import boto3
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

CORPUS_SIZE = 12000

bucket = boto3.resource('s3').Bucket('learningdatajchswm9')


# n개의 논문에 있는 문장을 반환하는 함수.
def download_paper(n):
    if not os.path.exists('pdfData'):
        os.makedirs('pdfData')
    if not os.path.exists('txtData'):
        os.makedirs('txtData')

    # random.seed()
    paper_nums = [None] * n
    for i in range(n):
        paper_nums[i] = random.randint(1, CORPUS_SIZE)

    # 논문 다운로드
    pdf_file_dirs = [None] * n
    for i in range(n):
        s3_pdf_file_dir = 'pdfDatas/data2/HOO' + str(paper_nums[i]) + '.pdf'
        pdf_file_dirs[i] = 'pdfData/paper' + str(paper_nums[i]) + '.pdf'
        bucket.download_file(s3_pdf_file_dir, pdf_file_dirs[i])

    # pdf2txt
    result = ''
    for i in range(n):
        try:
            text = convert_pdf_to_txt(pdf_file_dirs[i])  # time limit 필요
            f = open('txtData/paper' + str(paper_nums[i]) + '.txt', 'w', encoding='UTF-8')
            f.write(text)
            f.close()
            result += text
        except Exception:
            pass

    return result


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.all_texts = True
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
