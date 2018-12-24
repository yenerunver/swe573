from gensim.models import Doc2Vec

model = Doc2Vec.load('trmodel.doc2vec')

new_sentence = "Dün okula gittim".split(" ")

suggestions = model.docvecs.most_similar(positive=[model.infer_vector(new_sentence)], topn=5)

print(suggestions)

'''
for suggestion in suggestions:
    print(model.docvecs[suggestion[0]])
'''