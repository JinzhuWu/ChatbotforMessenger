import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet


def sentence_tokens(text):
	sens = nltk.sent_tokenize(text.lower())
	return sens

def preprocessing(text):
	lancaster_stemmer = LancasterStemmer() #stem
	
	sr = stopwords.words('english')
	english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']

	tags = []
	words = nltk.word_tokenize(text)
	tag = nltk.pos_tag(words)
	tags.append(tag)

	new_tag = []
	new_words = []
	# synonyms = []
	access_list = set({'VB','VBD','VBG','VBP','VBZ','VBN','NN','NNS','NNP','NNPS'})
	tags = tags[0]
	for items in tags:
		# one_synonyms = []
		if items[0] not in sr:
			if items[0] not in english_punctuations:
				if items[1] in access_list:
					single_word = lancaster_stemmer.stem(items[0])
					if len(single_word) > 2:
						new_words.append(single_word)
						new_tag.append(items)
						# for syn in wordnet.synsets(single_word):
						# 	for lemma in syn.lemmas():
						# 		one_synonyms.append(lemma.name())
						# synonyms.append(one_synonyms)

	return new_words

