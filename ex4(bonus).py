import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim import corpora, models
import pyLDAvis.gensim_models
import pyLDAvis


nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download('punkt')


alice_text = gutenberg.raw('carroll-alice.txt')
sentences = sent_tokenize(alice_text)


stop_words = set(nltk.corpus.stopwords.words('english'))
texts = [[word.lower() for word in word_tokenize(sentence) if word.isalpha() and word.lower() not in stop_words] for sentence in sentences]


dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]


lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)


topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)


lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)
pyLDAvis.save_html(lda_display, 'lda_visualization.html')
