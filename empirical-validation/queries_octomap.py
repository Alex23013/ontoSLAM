#SparQL Queries

from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL, RDFS, URIRef
from rdflib.plugins.sparql import prepareQuery
from time import time 

#variables
nameOntology = "out_pepper_onto_0.owl"
num_test = 11  # one extra test because we don't count the first test due cache time

os = Namespace("OS:")
cora =Namespace("http://www.semanticweb.org/ontologies/2013/7/RobotsAutomation.owl")
dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")

def mapa_octomap_1(g): 
    qpro = prepareQuery("""
    PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?link ?rel ?o
           WHERE {    
             VALUES ?rel { ns1:cartesianX ns1:cartesianY ns1:cartesianZ }.
              ?link  a ns2:BasePart .  
              ?link ns2:hasPosition ?pos .  
              ?pos ns2:hasTranslation ?t .
              ?t a ns3:cartesianPositionPoint .
              ?t ?rel ?o 
    }""" )
    pro = g.query(qpro)
    for row in pro:
        print(row[1])
        p = row[1]
        o = p[ p.find('#')+1: len(p)]
        if o == "cartesianX":
            px=float(row[2])
        if o == "cartesianY":
            py=float(row[2])
        if o == "cartesianZ":
            pz=float(row[2])
    return [px,py,pz]


def mapa_octomap_2(g, marker_id): 
    qpro = prepareQuery("""
    PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?obj  ?val
           WHERE {    
             ?obj  a  ns2:AtomicPart .
             ?joint ns2:hasChild  ?obj .
             ?joint ns2:hasParent ?id .
             ?obj ns2:hasVisual ?vi .
             ?vi  ns2:hasColor ?color .
             ?color ns2:hasRGBValue ?val .
             FILTER regex(str(?val), "(0.753846168518,0.0,1.0,1.0)") 
    }""" )
    pro = g.query(qpro, initBindings={'id': marker_id})
    return pro

def mapa_octomap_3(g, marker_id): 
    qpro = prepareQuery("""
    PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?obj  ?val
           WHERE {    
             ?obj  a  ns2:AtomicPart .
             ?joint ns2:hasChild  ?obj .
             ?joint ns2:hasParent ?id .
             ?obj ns2:hasVisual ?vi .
             ?vi  ns2:hasColor ?color .
             ?color ns2:hasRGBValue ?val .
             FILTER (?val != "(0.753846168518,0.0,1.0,1.0)")
    }""" )
    pro = g.query(qpro, initBindings={'id': marker_id})
    return pro

def mapa_octomap_4(g, marker_id): 
    qpro = prepareQuery("""
    PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?obj  ?rel ?o
           WHERE {   
              VALUES ?rel {  ns1:cartesianX ns1:cartesianY ns1:cartesianZ} . 
             ?obj  a  ns2:AtomicPart .
             ?joint ns2:hasChild  ?obj .
             ?joint ns2:hasParent ?id .
             ?obj ns2:hasPosition ?pos .
             ?pos ns2:hasTranslation ?t .
             ?t ?rel ?o   
    }""" )
    pro = g.query(qpro, initBindings={'id': marker_id})
    return pro

def mapa_octomap_5(g): 
    qpro = prepareQuery("""
    PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?obj ?t ?stamp
           WHERE {    
             ?obj  a  ns2:AtomicPart .
             ?env a ns1:Environment .   
             ?joint ns2:hasChild  ?obj .
             ?joint ns2:hasParent ?env  .                                 
             ?obj ns2:hasPosition ?s .   
             ?s ns2:hasTranslation ?t .
             ?s ns2:posAtTime ?st .
             ?st ns2:hasStamp ?stamp  .
             FILTER regex(str(?obj), "mk_") 
                        }""" )
    pro = g.query(qpro)
    return pro

def mapa_7(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?obj ?val
           WHERE {    
             ?obj  a  ns1:AtomicPart .
             ?env a ns2:Environment .   
             ?joint ns1:hasChild  ?obj .
             ?joint ns1:hasParent ?env  .
             ?obj ns1:hasProbability ?prob .
            ?prob ns1:hasNumberValue ?val
                        }""" )
    pro = g.query(qpro)
    return pro

def eval_ontology(nameOntology):
    print("evaluating ", nameOntology)
    g = Graph()
    g.parse(nameOntology, format="turtle")      
    result = 0
    for i in range(num_test):
        init_time = time() 
        marker_id=URIRef("http://github.com/Alex23013/slam-up/individual/obj/mk_16")
        pro = mapa_octomap_4(g, marker_id)#depends of the question to analize
        #pro = mapa_octomap_1(g) #depends of the question to analize
        final_time = time() 
        execution_time = (final_time - init_time)
        if i != 0:
            result+= execution_time
            print ('test ', i, ": ",execution_time) #in seconds

    prom = result/num_test
    print ('average time execution:',prom) #in seconds
    ''' 
    #To see the triplets found
    for row in pro:
            print (row)
            print("-----------------------------")
    
    print("len de answer: " )
    print( len(pro))
    '''

eval_ontology(nameOntology)

#### buscar propuestas de sistema contable para una empresa
####pcornejo@isur.edu.pe


