from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL
import numpy as np
import editdistance as ed
import math
from sklearn.feature_extraction.text import TfidfVectorizer


#defining functions

def stringSim(str1,str2):
    #print("str1:",str1," str2:",str2)
    edVal = ed.eval(str1,str2)
    #print("edit distance",edVal)
    mod = np.absolute(len(str1)+len(str2) - edVal)
    return 1/(math.exp(edVal/mod))

def calcStringSim(list1, list2, ro):
    dupEnt = 0
    simEnt = 0
    for i in range(0,len(list1)):
        for j in range(0,len(list2)):
            if list1[i] == list2[j]:
                dupEnt = dupEnt+1
            if stringSim(list1[i],list2[j]) > ro:
                simEnt = simEnt+1
    #print("similarEntities ",simEnt)
    #print("duplicatedEntities ",dupEnt)
    simm = simEnt / (len(list1)+len(list2)-dupEnt)
    return simm

def getEntities(nameOntology, prefix, part):
    g = Graph()
    g.parse(nameOntology, format="xml")
    print("Analizing ",part, " in file ", nameOntology)

    subjects =[]
    
    for subj, pred, obj in g:
        if (subj, pred, obj) not in g:
           raise Exception("It better be!")
        else:           
            if part == "subjects":
                evaluatedString = subj          
            elif part == "predicates":
                evaluatedString = pred
            elif part == "objects":
                evaluatedString = obj
            start = evaluatedString.find(prefix)
            if start != -1:
                osubj = evaluatedString[start+1:]
            else:
                osubj = "0"
                
            if  osubj.isalpha():
                subjects.append(osubj)
            else :
                if osubj.find(':') != -1 and osubj.find('http') == -1 :
                    newStart =osubj.find(':')
                    subjects.append(osubj[newStart+1:])
    only = list(set(subjects))
    return only

def getTotalEntities (ontologyName):
    entCora = []
    subjCora = getEntities(ontologyName, '#', "subjects")
    predCora = getEntities(ontologyName, '#', "predicates")
    objCora = getEntities(ontologyName, '#', "objects")
    entCora.extend([element for element in subjCora if element not in entCora])
    entCora.extend([element for element in predCora if element not in entCora])
    entCora.extend([element for element in objCora if element not in entCora])
    return entCora

#defining parameters to validate
ro_value = 0.75
alfa = 0.5
beta = 0.5


#variables from the tfidf.py file
DocSim1 = 0.64 #FR2013/OntoSLAM
DocSim2 = 0.56 #KnowRob/OntoSLAM
DocSim3 = 0.54 #FR2013/Knoworb

#validate proccess
onto = getTotalEntities("../input_ontologies/ontoSLAM.owl")
print("ontoSLAM total entities: ")
print(len(onto)) 

resFR = getTotalEntities("../input_ontologies/fortesRey.owl")
print("FR2013 total entities: ")
print(len(resFR)) 

resKNOW = getTotalEntities("../input_ontologies/knowrob.owl")
print("KNOWROB total entities: ")
print(len(resKNOW)) 

finSimm1 = calcStringSim(resFR, onto, ro_value )
print("StringSimm [FR2013, ontoSLAM]:", finSimm1)
finSimm2 = calcStringSim(onto, resKNOW, ro_value  )
print("StringSimm [ontoSLAM, knowrob] :", finSimm2)
finSimm3 = calcStringSim(resFR, resKNOW, ro_value  )
print("StringSimm [FR2013, knowrob] :", finSimm3)

sim1 = alfa* DocSim1 + beta*finSimm1
print ("\nLinguisticSimm[FR2013, ontoSLAM]: "+str(sim1))

sim2 = alfa* DocSim2 + beta*finSimm2
print ("LinguisticSimm[ontoSLAM, knowrob]: "+str(sim2))

sim3 = alfa* DocSim3 + beta*finSimm3
print ("LinguisticSimm[FR2013, knowrob] : "+str(sim3))


