# Import all the dependencies
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import boto3
import os
import pickle

'''
data = ["I love coding in python",
        "I love building chatbots",
        "I love chatbots",
        "I love machine learning. Its awesome."]
'''

data = ''
download = input('다운로드(y/n)...')

if download.lower() == 'y' or not os.path.exists('data.pickle') or not os.path.exists('d2v.model'):
    num_paper = int(input('논문 개수...'))
    max_epochs = int(input('Epochs...'))
    # Download data from S3
    bucket = boto3.resource('s3').Bucket('learningdatajchswm9')
    if not os.path.exists('sentences'):
        os.makedirs('sentences')
    data = []
    cnt_paper = 0
    for i in range(10000, 10000+num_paper):
        try:
            file_dir = 'sentences/HOO' + str(i) + 'content.txt'
            if not os.path.exists(file_dir):
                bucket.download_file(file_dir, file_dir)
                # Show download
                print(file_dir + ' 다운로드 완료.')
            f = open(file_dir, 'r', encoding='UTF-8')
            sentences = f.read()
            f.close()
            data += sentences.splitlines()
            cnt_paper += 1
        except Exception as e:
            print(e)
    print('%d개의 논문 다운로드 완료' % cnt_paper)
    print('%d개의 문장 추출 성공.' % len(data))

    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]
    # print(tagged_data)
    with open('data.pickle', 'wb') as f:
        pickle.dump(tagged_data, f, pickle.HIGHEST_PROTOCOL)

    vec_size = 100
    alpha = 0.025

    model = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1,
                    workers=4)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    model.save("d2v.model")
    print("Model Saved")

else:
    with open('data.pickle', 'rb') as f:
        tagged_data = pickle.load(f)

    model = Doc2Vec.load("d2v.model")

# to find the vector of a document which is not in training data
test_data = word_tokenize("In fact, the proposed architecture provides".lower())
v1 = model.infer_vector(test_data)
print("V1_infer", v1)

# to find most similar doc using tags
# which_sent = 205000
# print(tagged_data[which_sent])
similar_doc = model.docvecs.most_similar([v1], topn=10)
# print(similar_doc)
for pair in similar_doc:
    print(pair[1], tagged_data[int(pair[0])])
