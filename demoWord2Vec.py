import gensim
from gensim.models import KeyedVectors

import sys

if len(sys.argv) > 1:
  positives = sys.argv[1].split(',')
else:
  print("You must define at least 1 word for positive corelation!")
  sys.exit(1)

if len(sys.argv) > 2:
  negatives = sys.argv[2].split(',')

else:
  negatives = []

#model = gensim.models.Doc2Vec.load('trmodel')  
#new_sentence = "I opened a new mailbox".split(" ")  
#model.docvecs.most_similar(positive=[model.infer_vector(new_sentence)],topn=5)

print("This demo will find suitable word that has a positive corelation with words: ", ', '.join(positives))

if len(negatives) > 0:
  print("This demo will find suitable word that has a negative corelation with words: ", ', '.join(negatives))

word_vectors = KeyedVectors.load_word2vec_format('trmodel.word2vec', binary=True)

print(word_vectors.most_similar(positives, negatives))
