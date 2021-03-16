#FILENAME: queries_gmapping.py
from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL, RDFS, URIRef
from rdflib.plugins.sparql import prepareQuery
from time import time 

#variables
num_test = 11 # one extra test because we don't count the first test due cache time
nameOntology = "out_turtlebot_example.owl" #name of the ontology instance to evaluate

os = Namespace("OS:")
cora =Namespace("http://www.semanticweb.org/ontologies/2013/7/RobotsAutomation.owl")
dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")

def p1(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    SELECT ?s ?dim ?val
           WHERE {                                     
              ?s  a ns1:BasePart .
              ?s ns1:hasVisual ?v .
              ?v ns1:hasDimension ?dim .
              ?dim ns1:hasValue ?val  
    }""" )
    pro = g.query(qpro)
    return pro

def p2(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#>
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#>  
    SELECT ?robot ?s 
           WHERE {      
              ?robot a ns2:Robot .
              ?robot ns1:hasModel ?model .
              ?model ns1:hasPart ?s  .
              ?s  a ns1:BasePart 
    }""" )
    pro = g.query(qpro)
    return pro


def p3(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#>  
    SELECT ?s 
           WHERE {         
              ?robot a ns2:Robot .
              ?robot ns1:hasModel ?model .
              ?model ns1:hasPart ?s  .                            
              ?s  a ns1:Sensor
    }""" )
    pro = g.query(qpro)
    return pro

def p4(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?link ?pos ?rel ?o
           WHERE {    
             VALUES ?rel { ns2:cartesianX ns2:cartesianY ns2:cartesianZ }.
              ?link  a ns1:BasePart .  
              ?pos  a  ns1:Position .
              ?link ns1:hasPosition ?pos .  
              ?s ns1:hasTranslation ?t .
              ?t a ns3:cartesianPositionPoint .
              ?t ?rel ?o 
    }""" )
    pro = g.query(qpro)
    return pro

def p5(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?s ?cmp ?o 
           WHERE {    
             VALUES ?rel {ns1:hasTranslation ns1:hasOrientation}                                
             VALUES ?cmp { ns2:cartesianX ns2:cartesianY ns2:cartesianZ ns1:componentX ns1:componentY ns1:componentZ ns1:componentW }.
              ?s  a  ns1:Position .
              ?s ?cmp ?o 
    }""" )
    pro = g.query(qpro)
    return pro


def p6(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?s ?coord ?o ?stamp
           WHERE {    
             VALUES ?coord { ns2:cartesianX ns2:cartesianY ns2:cartesianZ } .
              ?s  a  ns1:Position .
              ?s ns1:hasTranslation ?t .
              ?t a ns3:cartesianPositionPoint .
              ?t ?coord ?o .
             ?s ns1:posAtTime ?st .
             ?st ns1:hasStamp ?stamp
    }""" )
    pro = g.query(qpro)
    return pro



def p7(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?pos ?mat ?row ?col ?val
           WHERE {    
             VALUES ?rel {  ns1:hasMatrixValue ns1:hasNumberValue} .
             ?pos  a  ns1:Position .
             ?pos ns1:hasProbability ?prob . 
             ?prob ?rel ?mat .
             ?cell ns1:belongs_to ?mat .
             ?cell ns1:componentRow ?row .
             ?cell ns1:componentCol ?col .   
             ?cell ns1:componentValue   ?val
              
    }""" )
    pro = g.query(qpro)
    return pro

def mapa_1(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?robot ?obj
           WHERE {    
            ?obj  a  ns1:AtomicPart .
            ?env a ns2:Environment .
            ?robot a ns2:Robot .
            ?robot ns1:hasModel ?model .
            ?model ns1:hasPart ?s  .
            ?s  ns1:near ?obj
    }""" )
    pro = g.query(qpro)
    return pro

def mapa_2(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?obj
           WHERE {    
             ?obj  a  ns2:AtomicPart .
             ?env a ns1:Environment .   
             ?joint ns2:hasChild  ?obj .
             ?joint ns2:hasParent ?env  .
             ?obj ns2:hasProbability ?prob .
            ?prob ns2:hasNumberValue "0"
    }""" )
    pro = g.query(qpro)
    return pro

def mapa_3(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    SELECT ?obj
           WHERE {    
             ?obj  a  ns1:AtomicPart .
             ?env a ns2:Environment .   
             ?joint ns1:hasChild  ?obj .
             ?joint ns1:hasParent ?env  .
    }""" )
    pro = g.query(qpro)
    return pro

def mapa_4(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?obj ?rel ?o
           WHERE {    
             ?obj  a  ns1:AtomicPart .
             ?env a ns2:Environment .   
             ?joint ns1:hasChild  ?obj .
             ?joint ns1:hasParent ?env  .                                 
             ?obj ns1:hasPosition ?s .   
             ?s ns1:hasTranslation ?t .
             ?t a ns3:cartesianPositionPoint .
             ?t ?rel ?o 
    }""" )
    pro = g.query(qpro)
    return pro


def mapa_5(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?obj ?t ?stamp
           WHERE {    
             ?obj  a  ns1:AtomicPart .
             ?env a ns2:Environment .   
             ?joint ns1:hasChild  ?obj .
             ?joint ns1:hasParent ?env  .                                 
             ?obj ns1:hasPosition ?s .   
             ?s ns1:hasTranslation ?t .
             ?t a ns3:cartesianPositionPoint .
             ?s ns1:posAtTime ?st .
             ?st ns1:hasStamp ?stamp   
    }""" )
    pro = g.query(qpro)
    return pro

def mapa_6(g): 
    qpro = prepareQuery("""
    PREFIX ns1:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
    PREFIX ns2: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
    PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
    SELECT ?obj  ?other
    WHERE {
        ?obj  a  ns1:AtomicPart .
        ?env a ns2:Environment .
        ?joint ns1:hasChild  ?obj .
        ?joint ns1:hasParent ?env  .
        ?obj  ns1:near ?other
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
        pro = p3(g)
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



