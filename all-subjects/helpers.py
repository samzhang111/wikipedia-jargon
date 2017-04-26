import nltk
from collections import defaultdict


def text_dict_to_term_dict(d, remove_stopwords=True, ngrams=1):
    '''Transform the text document dictionary to a term document matrix
    by tokenizing, lemmatizing, lowercasing, and picking only lemmas
    that are all alphabetical. '''
    lemmatizer = nltk.WordNetLemmatizer()
    stopwords = set(nltk.corpus.stopwords.words('english'))
    stopword_lemmas = set(map(lemmatizer.lemmatize, stopwords))
    term_matrix = defaultdict(int)
    all_counts = 0
    for title in d:
        for paragraph in d[title]:
            # Tokenize lowercase words
            tokens = nltk.word_tokenize(paragraph.lower())

            # Lemmatize words
            lemmas = map(lemmatizer.lemmatize, tokens)
            for i in range(len(lemmas)-ngrams+1):

                lem = lemmas[i:i+ngrams]

                if not all([x.isalpha() for x in lem]):
                    continue

                # Remove stopwords if ngrams > 1
                if remove_stopwords:
                    if ngrams > 1 and any([x in stopwords for x in lem]):
                        continue

                    if lem[0] in stopword_lemmas:
                        continue

                lemstr = ' '.join(lem)

                term_matrix[lemstr] += 1
                all_counts += 1

    for x in term_matrix:
        term_matrix[x] /= float(all_counts)

    return term_matrix, all_counts

if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
