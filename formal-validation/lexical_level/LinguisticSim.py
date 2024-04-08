from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL
import numpy as np
import editdistance as ed
import math
#from scikit-learn.feature_extraction.text import TfidfVectorizer


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
    g.parse(nameOntology, format="turtle")
    #print("Analizing ",part, " in file ", nameOntology)

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

#variables from the tfidf.py file
doc_sim_seas_ssn = 0.3727961
doc_sim_seas_colpri = 0.2346912
doc_sim_seas_ds4iot = 0.1967611
doc_sim_ssn_colpri = 0.2346912
doc_sim_ssn_ds4iot = 0.2064308
doc_sim_colpri_ds4iot = 0.6278204

folderName = "iot_ontologies"

text_files = [
    "../"+folderName+"/seas_final.ttl",
    "../"+folderName+"/ssn_sosa_final.ttl",
    "../"+folderName+"/colpri.ttl",
    "../"+folderName+"/ds4iot.ttl"
    ]

#validate proccess
extracted_entities = {}
numberOfEntities = {}

for document in text_files:
    ontology = document.split("/")[-1].split(".")[0]
    extracted_entities[ontology]  = getTotalEntities(document)
    numberOfEntities[ontology]  = len(getTotalEntities(document))

#{'seas_final': 44, 'ssn_sosa_final': 35, 'colpri': 18, 'ds4iot': 15}

fin_sim_seas_ssn = calcStringSim(extracted_entities['seas_final'], extracted_entities['ssn_sosa_final'], ro_value)
fin_sim_seas_colpri = calcStringSim(extracted_entities['seas_final'], extracted_entities['colpri'], ro_value)
fin_sim_seas_ds4iot = calcStringSim(extracted_entities['seas_final'], extracted_entities['ds4iot'], ro_value)

fin_sim_ssn_colpri = calcStringSim(extracted_entities['ssn_sosa_final'], extracted_entities['colpri'], ro_value)
fin_sim_ssn_ds4iot = calcStringSim(extracted_entities['ssn_sosa_final'], extracted_entities['ds4iot'], ro_value)
fin_sim_colpri_ds4iot = calcStringSim(extracted_entities['colpri'], extracted_entities['ds4iot'], ro_value)

print("StringSimm seas_ssn:", fin_sim_seas_ssn)
print("StringSimm seas_colpri:", fin_sim_seas_colpri)
print("StringSimm seas_ds4iot:", fin_sim_seas_ds4iot)
print("StringSimm ssn_colpri:",    fin_sim_ssn_colpri)
print("StringSimm ssn_ds4iot:",    fin_sim_ssn_ds4iot)
print("StringSimm colpri_ds4iot:", fin_sim_colpri_ds4iot)

sim1 = alfa* doc_sim_seas_ssn + beta*fin_sim_seas_ssn
print ("\nLinguisticSimm[seas, ssn]: "+str(sim1))

sim2 = alfa* doc_sim_seas_colpri + beta*fin_sim_seas_colpri
print ("LinguisticSimm[seas, colpri]: "+str(sim2))

sim3 = alfa* doc_sim_seas_ds4iot + beta*fin_sim_seas_ds4iot
print ("LinguisticSimm[seas, ds4iot]: "+str(sim3))

sim4 = alfa* doc_sim_ssn_colpri + beta*fin_sim_ssn_colpri
print ("LinguisticSimm[ssn, colpri]: "+str(sim4))

sim5 = alfa* doc_sim_ssn_ds4iot + beta*fin_sim_ssn_ds4iot
print ("LinguisticSimm[ssn, ds4iot]: "+str(sim5))

sim6 = alfa* doc_sim_colpri_ds4iot + beta*fin_sim_colpri_ds4iot
print ("LinguisticSimm[colpri, ds4iot]: "+str(sim6))

'''
#validate proccess
entities_from_seas  = getTotalEntities("../iot_ontologies/seas.ttl")
print("Sosa total entities: ")
print(len(onto)) 

resFR = getTotalEntities("../iot_ontologies/ssn.ttl")
print("SSN total entities: ")
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
'''

