import aws
import os
from pdfConverter import convert_pdf_to_txt, trim_txt
from txt2sent import extract_sents

if not os.path.exists('pdfExample'):
    os.makedirs('pdfExample')
if not os.path.exists('txtExample'):
    os.makedirs('txtExample')

random = [1739,
          11345,
          7095,
          10328,
          2293,
          3047,
          6777,
          7595,
          7824,
          12392]

file_paths = ['pdfDatas/data2/HOO%d.pdf' % num for num in random]
print(file_paths)  # ['pdfDatas/data2/HOO1739.pdf', ...]

for file_path in file_paths:
    pdf_path = 'pdfExample/' + file_path.split('/')[-1]
    aws.bucket.download_file(file_path, pdf_path)

    try:
        text = trim_txt(convert_pdf_to_txt(pdf_path))
        print(text)
        result = extract_sents(text)['abstract']
    except Exception:
        result = ''

    fp = open(pdf_path.replace('pdf', 'txt'), 'w', encoding='UTF-8')
    fp.write(result)
    fp.close()

'''
Download the selected pdf files from S3.

'''