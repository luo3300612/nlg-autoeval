import pysnooper
from functools import reduce
from operator import add

candidate = "the the the the the the the."
reference1 = "The cat is on the mat."
reference2 = "There is a cat on the mat."
reference = [reference1, reference2]

punctuations = ['.', '?']


def preprocess(sentence):
    # ? how to deal with punctuation?
    sentence = sentence[:len(sentence) - 1] if sentence[-1] in punctuations else sentence
    return ' '.join([word.lower() for word in sentence.split(' ') if word not in punctuations])


# @pysnooper.snoop()
def unigram_precision(candidate, references):
    candidate = preprocess(candidate)
    references = [preprocess(reference) for reference in references]
    c_words = candidate.split(' ')
    r_words = reduce(add, [reference.split(' ') for reference in references])
    p = 0
    for c_word in c_words:
        p += 1 if c_word in r_words else 0
    return p / len(c_words)


def count_presence(p_sentence, n):
    count = {}
    s_words = p_sentence.split(' ')
    for i in range(len(s_words) - n + 1):
        n_gram = ' '.join(s_words[i:i + n])
        count[n_gram] = count.get(n_gram, 0) + 1
    return count


# @pysnooper.snoop()
def count_references_presence(p_references, n):
    counts = [count_presence(reference, n) for reference in p_references]
    return reduce(merge_count, counts)


def merge_count(count1, count2):
    return {key: max(count1.get(key, 0), count2.get(key, 0)) for key in set(count1.keys()) | set(count2.keys())}


# @pysnooper.snoop(watch_explode=['count_r','count_c'])
def modified_ngram_precision(candidate, references, n=1):
    candidate = preprocess(candidate)
    references = [preprocess(reference) for reference in references]
    count_r = count_references_presence(references, n)
    count_c = count_presence(candidate, n)
    p = sum([min(count_c.get(word, 0), count_r.get(word, 0)) for word in set(count_c.keys()) & set(count_r.keys())])
    return p / len(count_c)


print("Unigram example2")
print(unigram_precision(candidate, reference))
print(modified_ngram_precision(candidate, reference, 1))

ex1_candidate1 = "It is a guide to action which ensures that the military always obeys the commands of the party."
ex1_candidate2 = "It is to insure the troops forever hearing the activity guidebook that party direct."

ex1_reference1 = "It is a guide to action that ensures that the military will forever heed Party commands."
ex1_reference2 = "It is the guiding principle which guarantees the military forces always being under " \
                 "the command of the Party."
ex1_reference3 = "It is the practical guide for the army always to heed the directions of the party."
ex1_references = [ex1_reference1, ex1_reference2, ex1_reference3]

print("unigram example1")
print(modified_ngram_precision(ex1_candidate1, ex1_references, 1))
print(modified_ngram_precision(ex1_candidate2, ex1_references, 1))

print("bigram example1")
print(modified_ngram_precision(ex1_candidate1, ex1_references, 2))
print(modified_ngram_precision(ex1_candidate2, ex1_references, 2))

print("tritram example1")
print(modified_ngram_precision(ex1_candidate1, ex1_references, 3))
print(modified_ngram_precision(ex1_candidate2, ex1_references, 3))