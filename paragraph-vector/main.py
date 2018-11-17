import boto3
import pickle
import os
from nltk import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile

bucket = boto3.resource('s3').Bucket('learningdatajchswm9')

# Set up a corpus
common_texts = []
pickle_file = 'corpus.pickle'
# pickle 파일이 이미 존재하면
if not os.path.exists(pickle_file):
    download_cnt = 0
    temp_file = 's3_download_temp.txt'
    for i in range(12876):
        try:
            bucket.download_file('sentences/HOO' + str(i) + 'abstract.txt', temp_file)
            with open(temp_file, 'r', encoding='UTF-8') as f:
                sentences = f.read().splitlines()
                common_texts += [word_tokenize(sent) for sent in sentences]
            download_cnt += 1
            print(i, 'downloaded.')

        except Exception as e:
            print(i, e)

    os.remove(temp_file)
    print('%d files downloaded. %d sentences saved.' % (download_cnt, len(common_texts)))

    with open(pickle_file, 'wb') as f:
        pickle.dump(common_texts, f, pickle.HIGHEST_PROTOCOL)
# pickle 파일이 존재하지 않으면
else:
    with open(pickle_file, 'rb') as f:
        common_texts = pickle.load(f)

# input_sent = word_tokenize(input('User typing : '))
input_sent = word_tokenize('Recognition of license number plate is an image processing technique')
print(input_sent)

model_file = get_tmpfile("my_doc2vec_model")
learning_on = input('Learning on? (y/n)...').lower()
if learning_on == 'y':
    # Initialize & train a model
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
    model = Doc2Vec(documents, vector_size=200, window=5, min_count=3, workers=4, epochs=10)

    # print('documents =', documents)

    # Persist a model to disk
    model.save(model_file)
else:
    model = Doc2Vec.load(model_file)
# Delete temporary training data
model.delete_temporary_training_data()

# Infer a vector for a new document
vector = model.infer_vector(input_sent)
# print(vector)

# Search for the most similar sentences
similar_sentences = model.docvecs.most_similar(positive=[vector], topn=5)
print('Top 5 most similar sentences are:')
for pair in similar_sentences:
    sent_num = pair[0]
    similarity = pair[1]
    print(common_texts[sent_num], similarity)
