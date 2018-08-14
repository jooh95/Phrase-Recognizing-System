'''
Extract English sentences from the PDF files.
First, convert the PDF files to text files using pdfminer.
'''

'''
txt[key]를 딕셔너리로
key는 파트명 value는 문자열
'''

import glob, os
import re

import boto3
import re

s3 = boto3.resource('s3')
bucket = s3.Bucket('learningdatajchswm9')

folder = re.compile('pdfDatas/data2/.+[.]pdf')

for obj in bucket.objects.all():
    m = folder.match(obj.key)
    if m is not None: # 우리가 원하는 pdf 파일이면
        bucket.download_file(obj.key, obj.key)
        print(obj.key + ' downloaded.')

        try:
            # converting pdf files to txt files.
            txtFile = 'txtData/' + obj.key.split('/')[-1].replace('.pdf', '.txt')
            os.system('python3 pdf2txt.py -A -o %s %s' % (txtFile, obj.key))

            # importing a txt file.
            ifp = open(txtFile, 'r')
            orgTxt = ifp.read()
            ifp.close()

            # spliting abstract and contents
            txt = {'abstract': '', 'content': ''}
            Abstract_start = orgTxt.find('Abstract')
            ABSTRACT_start = orgTxt.find('ABSTRACT')
            if Abstract_start == -1 and ABSTRACT_start == -1:  # 'Abstract'를 못 찾은 경우
                txt['abstract'] = ''
                txt['content'] = orgTxt
            else:  # 'Abstract'를 찾은 경우
                if Abstract_start == -1:
                    abstract_start = ABSTRACT_start + 'ABSTRACT'.__len__()
                elif ABSTRACT_start == -1:
                    abstract_start = Abstract_start + 'Abstract'.__len__()
                else:
                    abstract_start = min(Abstract_start, ABSTRACT_start) + 'Abstract'.__len__()
                pattern = re.compile('[a-zA-Z]')
                m = pattern.search(orgTxt[abstract_start:])
                if m is None:
                    txt['abstract'] = ''
                    txt['content'] = orgTxt
                else:
                    abstract_start = abstract_start + m.start()
                    pattern = re.compile('\n\n+')
                    m = pattern.search(orgTxt[abstract_start:])
                    if m is None:
                        txt['abstract'] = ''
                        txt['content'] = orgTxt
                    else:
                        abstract_end = abstract_start + m.end()
                        txt['abstract'] = orgTxt[abstract_start:abstract_end]
                        txt['content'] = orgTxt[abstract_end:]

            keys = txt.keys()

            for key in keys:
                # deleting more than two spaces
                txt[key] = re.sub(r'\n\n+', '.', txt[key])

                # deleting other characters than ascii
                # deleting (), [], {}
                txt[key] = re.sub(r'\(.*?\)', '', txt[key], flags=re.DOTALL)
                txt[key] = re.sub(r'\[.*?\]', '', txt[key], flags=re.DOTALL)
                txt[key] = re.sub(r'\{.*?\}', '', txt[key], flags=re.DOTALL)
                txt[key] = re.sub(r'"(.*?)"', '', txt[key], flags=re.DOTALL)
                txt[key] = re.sub(r'“(.*?)”', '', txt[key], flags=re.DOTALL)
                txt[key] = re.sub(r"'(.*?)'", '', txt[key], flags=re.DOTALL)

                # spliting string
                delimiters = ".", "?", "!", ";", ":"
                regexPattern = '|'.join(map(re.escape, delimiters))
                sentences = re.split(regexPattern, txt[key])

                # output text file
                sentsFile = 'sentences/' + obj.key.split('/')[-1].replace('.pdf', key + '.txt')
                ofp = open(sentsFile, 'w')
                for sentence in sentences:
                    sentence = re.sub(r'-\s+', '', sentence).replace('\n', ' ').strip()
                    if sentence.__len__() > 20:  # length of sentence 20 above
                        ofp.write(sentence + '\n')
                ofp.close()

                # printing file name
                print(sentsFile + ' written.')

                # uploading to S3
                s3.Object('learningdatajchswm9', sentsFile).put(Body=open(sentsFile, 'rb'))
                print('Uploaded to S3.')

        except Exception as e:
            print(e)
