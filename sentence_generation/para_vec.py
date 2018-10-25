from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
print(documents)

model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)

# Persist a model to disk
from gensim.test.utils import get_tmpfile
fname = get_tmpfile("my_doc2vec_model")
model.save(fname)
model = Doc2Vec.load(fname)
print(model.docvecs.)

# If you’re finished training a model (=no more updates, only querying, reduce memory usage), you can do:
model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

# Infer vector for a new document
input_sent = ["human", "interface", "computer"]
input_vector = model.infer_vector(input_sent)
print(input_vector)

# Find the most similar vector in the sentences
sims = model.docvecs.most_similar([input_vector])
print(sims, '\n')
for sim in sims:
    print('%+f' % sim[1], documents[sim[0]])
