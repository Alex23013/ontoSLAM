from sklearn.feature_extraction.text import TfidfVectorizer

text_files = ["../input_ontologies/ontoSLAM.owl", "../input_ontologies/fortesRey.owl", "../input_ontologies/knowrob.owl"]
documents = [open(f).read() for f in text_files]
tfidf = TfidfVectorizer().fit_transform(documents)
# no need to normalize, since Vectorizer will return normalized tf-idf
pairwise_similarity = tfidf * tfidf.T
print("pairwise_similarity")
print(pairwise_similarity.toarray())

'''
Expected answer:
[
 [1.         0.6495376  0.57146972]
 [0.6495376  1.         0.55364934]
 [0.57146972 0.55364934 1.        ]
]

Values for copy on LinguisticSim file
0.6495376 ==> FR2013/OntoSLAM
0.57146972 ==> KnowRob/OntoSLAM
0.55364934 ==> FR2013/Knoworb
'''
