import nltk
from collections import defaultdict

stopwords = set(nltk.corpus.stopwords.words('english'))

def text_dict_to_term_dict(d, ngrams=1):
    '''Transform the text document dictionary to a term document matrix
    by tokenizing, lemmatizing, lowercasing, and picking only lemmas
    that are all alphabetical. '''
    lemmatizer = nltk.WordNetLemmatizer()
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
                if ngrams > 1 and any([x in stopwords for x in lem]):
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
