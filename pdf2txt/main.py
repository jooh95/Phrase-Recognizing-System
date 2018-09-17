import boto3
import re
import os
from pdfConverter import convert_pdf_to_txt
from pdfConverter import trim_txt
from txt2sent import extract_sents
import aws
from timeLimit import time_limit
from txt2sent import parts

rewrite = False  # 덮어쓰기
folder = re.compile('pdfDatas/data2/.+[.]pdf')  # Files to download from S3

# 폴더 생성
if not os.path.exists('pdfData'):
    os.makedirs('pdfData')
if not os.path.exists('txtData'):
    os.makedirs('txtData')
if not os.path.exists('sents'):
    os.makedirs('sents')

for obj in aws.bucket.objects.all():
    try:
        time_limit(15)

        # 우리가 원하는 pdf 파일이면
        if folder.match(obj.key) is not None:
            pdf_file_dir = 'pdfData/' + obj.key.split('/')[-1]
            txt_file_dir = pdf_file_dir.replace('pdf', 'txt')

            # s3에 변환된 문장이 이미 있는지 확인
            go = False
            for key in parts:
                file_dir = 'sents/' + txt_file_dir.split('/')[-1].split('.')[-2] + key + '.txt'
                if not aws.exists(file_dir) or rewrite:
                    go = True
                    break
            if not go:
                continue

            # pdf file이 local에 존재하는지 확인하고 없으면 다운로드
            if not os.path.exists(pdf_file_dir):
                aws.bucket.download_file(obj.key, pdf_file_dir)

            # pdf2txt 변환
            if not os.path.exists(txt_file_dir) or rewrite:
                text = convert_pdf_to_txt(pdf_file_dir)
                text = trim_txt(text)
                f = open(txt_file_dir, 'w', encoding='UTF-8')
                f.write(text)
                f.close()
            else:
                f = open(txt_file_dir, 'r', encoding='UTF-8')
                text = f.read()
                f.close()

            # txt2sent 변환
            sents = extract_sents(text)

            # S3에 쓰기
            for key in sents.keys():
                file_dir = 'sents/' + txt_file_dir.split('/')[-1].split('.')[-2] + key + '.txt'
                # sents/HOO10000abstract.txt
                if not aws.exists(file_dir) or rewrite:
                    f = open(file_dir, 'w', encoding='UTF-8')
                    f.write(sents[key])
                    f.close()
                    aws.s3.Object(aws.bucket_name, file_dir).put(Body=open(file_dir, 'rb'))

            print(pdf_file_dir + ' extracted.')

    except Exception as e:
        print(e)
