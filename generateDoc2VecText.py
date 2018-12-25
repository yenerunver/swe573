from gensim.models import Doc2Vec
import pandas as pd

model = Doc2Vec.load('trmodel.doc2vec')


def generatesimilartext(sentence, topn=5):
    new_sentence = sentence.split(" ")

    suggestions = model.docvecs.most_similar(positive=[model.infer_vector(new_sentence)], topn=topn)

    rows = [int(suggestion[0]) for suggestion in suggestions]

    sentences = pd.read_csv('sentences.csv')

    return [target_row.iloc[0]['sentence'].capitalize()+"."
            for target_row in [sentences.loc[sentences['id'] == index]
                               for index in rows]]
