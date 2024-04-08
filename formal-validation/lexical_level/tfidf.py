from sklearn.feature_extraction.text import TfidfVectorizer

folderName = "iot_ontologies"

text_files = [
    "../"+folderName+"/seas_final.ttl",
    "../"+folderName+"/ssn_sosa_final.ttl",
    "../"+folderName+"/colpri.ttl",
    "../"+folderName+"/ds4iot.ttl"
    ]
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

'''
pairwise_similarity
|   seas    | ssn       | colpri    | ds4iot
[[1.         0.37279614 0.20946242 0.19676114]
 [0.37279614 1.         0.23469121 0.20643083]
 [0.20946242 0.23469121 1.         0.6278204 ]
 [0.19676114 0.20643083 0.6278204  1.        ]]

Values for copy on LinguisticSim file
0.37279614 ==> seas/ssn
0.23469121 ==> seas/colpri
0.19676114 ==> seas/ds4iot
0.23469121 ==> ssn/colpri
0.20643083 ==> ssn/ds4iot
0.6278204  ==> colpri/ds4iot
'''
