import nltk
from gensim.models import Word2Vec
from download_paper import download_paper

# define training data
text = download_paper(50)
sentences = []
for sentence in nltk.sent_tokenize(text):
    if len(sentence) >= 4:
        sentences.append(nltk.word_tokenize(sentence))
print(sentences)
'''
sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
             ['this', 'is', 'the', 'second', 'sentence'],
             ['yet', 'another', 'sentence'],
             ['one', 'more', 'sentence'],
             ['and', 'the', 'final', 'sentence']]
'''
# train model
model = Word2Vec(sentences, min_count=3, iter=1000)
print(model)

# summarize vocabulary
# words = list(model.wv.vocab)
# print(words)

# access vector for one word
# print(model['importance'])

# save model
model.save('model.bin')
'''
# load model
model = Word2Vec.load('model.bin')
# print(new_model)
'''
result = model.most_similar(positive=['correct'], topn=10)
print(result)

# 그리기
'''
from sklearn.decomposition import PCA
from matplotlib import pyplot
# fit a 2d PCA model to the vectors
X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
    pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()
'''
