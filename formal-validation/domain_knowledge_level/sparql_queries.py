#SparQL Queries

from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL, RDFS, URIRef
from rdflib.plugins.sparql import prepareQuery

from time import time 

nameOntology1 = "../input_ontologies/frTurtle.owl" #[1]
nameOntology2 = "../input_ontologies/knTurtle.owl" #[2]
nameOntology3 = "../input_ontologies/propuestaTurtle.owl" #[3]

os = Namespace("OS:")
cora =Namespace("http://www.semanticweb.org/ontologies/2013/7/RobotsAutomation.owl")
dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")

###also: cat2_b1, cat2_c1 and cat2_c2
def cat1_a1(g): #[1,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s 
                                    .FILTER regex(str(?s), "Part") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

def cat1_a2(g): #[0,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Axis") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

##also: cat2_c3
def cat1_a3(g):#[0,0,1]
    qpro = prepareQuery("""SELECT ?s
                                WHERE {
                                    ?s a owl:Class ;
                                     .FILTER regex(str(?s), "Joint") .
                                    }""",
                                    initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

def cat1_b1(g): #[0,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Sensor") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro


### cat2_b2
def cat1_c1(g): #[0,1,1] 
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Pose") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

## also: cat2_b3
def cat1_c2(g): #[0,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    VALUES ?rel { <OS:hasRelativePosition> dul:hasLocation }
                                    ?s a owl:ObjectProperty  ;                                    
                                    rdfs:subPropertyOf ?rel ;
                        }""",
                        initNs= {"owl": OWL, "dul":dul} )
    pro = g.query(qpro)
    return pro

def cat1_d1(g): #[1,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Position") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

## also: cat2_d1
def cat1_e1(g): #[0,0,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Probability") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

def cat2_a1(g): #[1,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Region") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro
##cat3_b2
def cat3_b1(g): #[1,0,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:ObjectProperty  ;
                                    .FILTER regex(str(?s), "posAtTime") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

def cat4_a1(g): #[0,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Dimension") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro

def cat4_b1(g): #[0,1,1]
    qpro = prepareQuery("""SELECT ?s 
                               WHERE { 
                                    ?s a owl:Class ;
                                    .FILTER regex(str(?s), "Thing") .
                        }""",
                        initNs= {"owl": OWL } )
    pro = g.query(qpro)
    return pro


def eval_ontology(nameOntology):
    print("evaluating ", nameOntology)
    g = Graph()
    g.parse(nameOntology, format="turtle")

    classes = [i for i in g.subjects(RDF.type, OWL.Class)]
    print("classes: ", len(classes))
    tiempo_inicial = time() 
    #replace the next line to run differents sparql queries
    pro = cat1_a3(g)

    tiempo_final = time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
 
    print( 'execution time :',tiempo_ejecucion) #in seconds
    '''
    #if you want to see the rows of result
    for row in pro:
            print (row)
            print("-----------------------------")
    '''
    print("triplets found: " )
    print( len(pro))

eval_ontology(nameOntology1)
eval_ontology(nameOntology2)
eval_ontology(nameOntology3)
