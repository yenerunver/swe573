from os import listdir
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
#import nltk
from nltk.tokenize import word_tokenize
import pandas as pd

#nltk.download('punkt')

# BEGIN Load data as array of sentences
docLabels = [f for f in listdir("ttc3600") if f.endswith(".txt")]
data = []

for doc in docLabels:
    sentences = open("ttc3600/" + doc, encoding="utf-8").read().replace('"', '').replace("'", "").split(".")
    for sentence in sentences:
        words = [word for word in sentence.strip().split(" ")
                 if word.isspace() is False
                 and word != ''
                 and word.isupper() is False]
        words_to_be_appended = [word for word in words
                                if word.startswith("(") is False]
        sentence_to_be_appended = " ".join(words_to_be_appended)
        if sentence_to_be_appended != '' and '/' not in sentence_to_be_appended and "\\" not in sentence_to_be_appended:
            data.append(sentence_to_be_appended.replace("\n", "").replace("\t", ""))
# END Load data as array of sentences

# Tokenize data
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

# BEGIN Save tokenized data
d = {'id': [int(vector.tags[0]) for vector in tagged_data], 'sentence': [" ".join(vector.words) for vector in tagged_data]}
df = pd.DataFrame(data=d)
df.to_csv("sentences.csv", sep=',', encoding='utf-8', index=False, header=True)
# END Save tokenized data

# BEGIN training
max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(vector_size=vec_size,
                alpha=alpha,
                min_alpha=0.00025,
                min_count=1,
                dm=1)

model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)

    model.alpha -= 0.0002

    model.min_alpha = model.alpha
# END training

# Save model
model.save("trmodel.doc2vec")

print("Model Saved")
