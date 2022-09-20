import nltk
from collections import Counter


sample = "This is a sentence to be tokenised. This one too!"
tokens = nltk.word_tokenize(sample)
print(tokens)

print(Counter(tokens))
