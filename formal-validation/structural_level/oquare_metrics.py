#Metricas OQuaRE

from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL, RDFS, URIRef
from rdflib.plugins.sparql import prepareQuery
import queue

os = Namespace("OS:")
fr = Namespace("http://www.semanticweb.org/ontologies/2013/7/RobotsAutomation.owl#SUMO:")
kn = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
sosa = Namespace("http://www.w3.org/ns/sosa/#")
class Metricas:

    def __init__(self, file):
        self.g = Graph()
        self.getEntities(file)
        self.ecrm = Namespace("http://github.com/Alex23013/slam-up/") #ontoSLAM
#        self.ecrm = Namespace("http://www.semanticweb.org/ontologies/2013/7/") #fr2013
#        self.ecrm = Namespace("http://www.ontologydesignpatterns.org/ont/dul/") #kn
        self.g.bind("os", self.ecrm)
#        self.g.bind("fr", self.ecrm) #fr2013
#        self.g.bind("kn", self.ecrm)  #kn
        self.g.bind("rdfs", RDFS)
        self.level_dic = {}
        self.leaves = []
        self.classes = []

        self.getClasses() #create list of classes
        self.levelConcept() #Create level_dic
        self.leavesConcept() #Create leaves

    def getEntities(self, nameOntology):
        self.g.parse(nameOntology, format="turtle")
        print("Analizing :", nameOntology)

    def levelConcept(self):
        #Create a dictionary concept-level
        ##print("root: ",sosa.FeatureOfInterest)
        print("root", OWL.Thing)
        current = [] #current list to iterate
        prox = [] #next list
        current = [OWL.Thing] # OntoSLAM
        #current = [fr.Entity] # fr2013
        ##current = [sosa.FeatureOfInterest] #sosa
        level = 0
        while ( len(current) != 0):
            for child in current:
                temp = [i for i in self.g.subjects(RDFS.subClassOf, child)]
                #print(temp)
                prox.extend(temp)
                try:
                    self.level_dic[child].append(level)
                except:
                    self.level_dic[child] = [level]
            current.clear()
            current, prox = prox, current
            level += 1
        print("len de level_dic:")
        #print(self.level_dic)
        print(len(self.level_dic))
    
    def getClasses(self):
        self.classes = [i for i in self.g.subjects(RDF.type, OWL.Class)]


    def numberRelationship(self, concept):
        #Return number of relationships (objectproperties) of a concept
        #concept = URIRef(self.ecrm + concept)
        qpro = prepareQuery("""SELECT ?p
                        WHERE {
                            VALUES ?rel { rdfs:domain rdfs:range }
                            ?p a owl:ObjectProperty ;
                                ?rel ?c ;                                
                            }""",
                            initNs= {"ecrm" : self.ecrm,
                                "owl": OWL} )

        pro = self.g.query(qpro, initBindings={'c': concept})
        return len(pro)

    def numberDataProperties(self, concept):
        #Return number of datatype properties of a concept
        #concept = URIRef(self.ecrm + concept)
        qpro = prepareQuery("""SELECT ?p
                        WHERE {
                            VALUES ?rel { rdfs:domain rdfs:range }
                            ?p a owl:DatatypeProperty ;
                                ?rel ?c ;                                
                            }""",
                            initNs= {"ecrm" : self.ecrm,
                                "owl": OWL} )

        pro = self.g.query(qpro, initBindings={'c': concept})
        return len(pro)

    def numberDirectSuperclass(self, concept):
        #Return parents of concept
        #concept = URIRef(self.ecrm + concept)
        qpar = prepareQuery( """ SELECT ?p
                        WHERE {
                            ?c rdfs:subClassOf ?p .
                            FILTER (!isBlank(?p)) 
                        }
                        """,
                        initNs= {"ecrm" : self.ecrm})

        par = self.g.query(qpar, initBindings={'c': concept})
        parent = []
        for i in par:
            parent.append(i[0])
        return len(par), parent

    def numberDirectSubclass(self, concept):
        #Return childs of concept
        #concept = URIRef(self.ecrm + concept)
        qchi = prepareQuery( """ SELECT ?p
                        WHERE {
                            ?p rdfs:subClassOf ?c .
                            FILTER (!isBlank(?p)) 
                        }
                        """,
                        initNs= {"ecrm" : self.ecrm})

        chi = self.g.query(qchi, initBindings={'c': concept})
        children = []
        for i in chi:
            children.append(i[0])
        return len(chi)

    def numberRestrictions(self, concept):
        #Return property restrictions
        #(owl:someValuesFrom, owl:allValuesFrom, owl:hasValue,
        # owl:minCardinality, owl:maxCardinality) nested inside of rdfs:subClassOf
        qres = prepareQuery("""SELECT ?p
                        WHERE {
                            VALUES ?t { 
                                owl:someValuesFrom owl:allValuesFrom
                                owl:hasValue owl:minCardinality 
                                owl:maxCardinality}
                            ?c rdfs:subClassOf [ ?t ?p ] .                               
                            }""",
                            initNs= {"ecrm" : self.ecrm,
                                "owl": OWL} )

        res = self.g.query(qres, initBindings={'c': concept})
        #for i in res:
        #    print(i)
        return len(res)

    def numberAnnotation(self, concept):
        #Return property annotations
        #(existing in OWL: owl:versionInfo, rdfs:comment,
        # rdfs:label, rdfs:seeAlso, rdfs:isDefinedBy)
        qann = prepareQuery("""SELECT ?p
                        WHERE {
                            VALUES ?t { 
                                owl:versionInfo rdfs:comment
                                rdfs:label rdfs:seeAlso 
                                rdfs:isDefinedBy}
                            ?c a owl:Class ;
                                ?t ?p .
                            }""",
                            initNs= {"ecrm" : self.ecrm,
                                "owl": OWL} )

        ann = self.g.query(qann, initBindings={'c': concept})
        return len(ann)


    def leavesConcept(self):
        #Return all leaves concepts
        ql = prepareQuery( """ SELECT ?c
                            WHERE {
                                ?c a owl:Class .
                                MINUS 
                                {
                                    ?child rdfs:subClassOf ?c .
                                }
                            }
                            """,
                            initNs= {"ecrm" : self.ecrm,
                                    "owl" : OWL})
        
        leaf = self.g.query(ql)
        self.leaves = [i[0] for i in leaf]
        print("leaves:::")
        print(len(self.leaves))

    def LenPath(self):
        #Return Sum Length of path from leaves to Thing and Total Path
        #Auxiliar function to LCOMOnto y WMCOnto
        #Sum Length of path from leaves to Thing
        '''
        print("self.level_dic")
        print(self.level_dic)
        print("self.leaves")
        print(self.leaves)
        '''
        sum_len_path = 0
        total_path = -1 # discount thing
        for i in self.leaves:
            if i in self.level_dic:
                for path in self.level_dic[i]:            
                    total_path += 1
                    sum_len_path += path
        '''
        print("sum_len_path")
        print(sum_len_path)
        print("total_path")
        print(total_path)
        '''
        return sum_len_path, total_path

    def LCOMOnto(self):
        #Lack of Cohesion in Methods
        sum_len_path , total_path = self.LenPath()
        return sum_len_path/ total_path
            
    def WMCOnto2(self):
        #Weight method per class
        sum_len_path , dummy = self.LenPath()
        total_leaves = len(self.leaves)
        return sum_len_path/total_leaves
        
    def DITOnto(self):
        #Depth of subsumption hierarchy
        who = OWL.Thing
        depth = 0
        for i in self.leaves:
            if i in self.level_dic:
                for path in self.level_dic[i]:
                    if (path > depth):
                        who = i
                        depth = path
        return depth

    def NACOnto(self):
        #Number of Ancestor Classes
        ancestor = 0
        for i in self.leaves:
            anc, dummy = self.numberDirectSuperclass(i)
            ancestor += anc
        return ancestor / len(self.leaves)

    def NOCOnto(self):
        #Number of Children Concepts  
        sum_subclasses = 0 #Number of SubClasses for each Concept
        for i in self.classes:
            sum_subclasses += self.numberDirectSubclass(i)
        return sum_subclasses / (len(self.classes) - len(self.leaves))

    def CBOOnto(self):
        #Coupling between objects
        ancestor = 0 #number of ancestor per class
        ances_not_thing = 0 #number of classes which ancestor is not owl:Thing
        for i in self.classes:
            anc, who = self.numberDirectSuperclass(i)
            ancestor += anc
            if (OWL.Thing  in who):
                ances_not_thing += 1
        return ancestor / (len(self.classes) - ances_not_thing)

    def numberProperties(self):
        #Auxiliar for RFCOnto, NOMOnto
        sum_prop = 0 #number of direct object properties
        sum_data = 0 #number of direct data properties
        for i in self.classes:
            sum_prop += self.numberRelationship(i)
            sum_data += self.numberDataProperties(i)
        print("relations",sum_prop)
        return sum_prop + sum_data

    def numberSubconcepts(self):
        #Auxiliar for RROnto, PROnto, INROnto
        subconcepts = 0 #number of subconcepts per class
        for i in self.classes:
            sub = self.numberDirectSubclass(i)
            subconcepts += sub
        return subconcepts

    def numberAllAncestors(self):
        #Auxiliar for RFCOnto , TMOnto2
        ancestor = 0 #number of ancestors per class
        for i in self.classes:
            anc, dummy = self.numberDirectSuperclass(i)
            ancestor += anc
        return ancestor

    def RFCOnto(self):
        #Response for a concept
        ancestor = self.numberAllAncestors() #number of ancestors per class
        return (ancestor + self.numberProperties()) / len(self.classes)

    def NOMOnto(self):
        #Number of properties
        return self.numberProperties() / len(self.classes)

    def RROnto(self):
        #Relationship richness
        subconcepts = self.numberSubconcepts() #number of subconcepts per class
        return subconcepts / (subconcepts + self.numberProperties())

    def PROnto(self):
        #Properties Richness
        subconcepts = self.numberSubconcepts() #number of subconcepts per class
        properties = self.numberProperties()
        return properties / (subconcepts + properties)

    def AROnto(self):
        #Attribute Richness
        #Number of property restrictions 
        restrictions = 0 #number of restrictions per class
        for i in self.classes:
            restrictions += self.numberRestrictions(i)
        return restrictions / len(self.classes)
    
    def INROnto(self):
        #Relationships per concept
        subconcepts = self.numberSubconcepts() #number of subconcepts per class
        return subconcepts/ len(self.classes)

    def ANOnto(self):
        #Annotation Richness
        annotations = 0 #number of annotations per class
        for i in self.classes:
            annotations += self.numberAnnotation(i)
        print ("number ",len(self.classes))
        print ("number ann",annotations)
        return 32 / len(self.classes)

    def TMOnto2(self):
        #Tangledness
        ancestor = self.numberAllAncestors() #number of ancestors per class
        return ancestor/ len(self.classes)

import math
#oquare_value = math.floor(float(value) * 10 ** 2) / 10 ** 2  


class ScaledMetrics:
    def __init__(self, raw_metrics):
        self.scaled = {}
        self.raw_metrics = raw_metrics
    
    def evaluate_pair_thresholds(self, list_thresholds, raw_value):
        if raw_value > list_thresholds[0]:
            return 1
        if raw_value > list_thresholds[1] and raw_value <= list_thresholds[0]:
            return 2
        if raw_value > list_thresholds[2] and raw_value <= list_thresholds[1]:
            return 3
        if raw_value > list_thresholds[3] and raw_value <= list_thresholds[2]:
            return 4
        if raw_value > list_thresholds[4] and raw_value <= list_thresholds[3]:
            return 5
        return 0
    
    def evaluate_last_single_thresholds(self, list_thresholds, raw_value):
        if raw_value > list_thresholds[0]:
            return 1
        if raw_value > list_thresholds[1] and raw_value <= list_thresholds[0]:
            return 2
        if raw_value > list_thresholds[2] and raw_value <= list_thresholds[1]:
            return 3
        if raw_value > list_thresholds[3] and raw_value <= list_thresholds[2]:
            return 4
        if raw_value <= list_thresholds[3]:
            return 5
        return 0

    def evaluate_percentage(self, raw_value):
        if raw_value <= 0.2:
            return 1
        if raw_value <= 0.4 and raw_value > 0.2:
            return 2
        if raw_value <= 0.6 and raw_value > 0.4:
            return 3
        if raw_value <= 0.8 and raw_value > 0.6:
            return 4
        if raw_value > 0.8:
            return 5

    
    def LCOMOnto(self):
        #Lack of Cohesion in Methods
        raw_value = self.raw_metrics["LCOMOnto"]
        return self.evaluate_last_single_thresholds([8,6,4,2], raw_value)
            
    def WMCOnto2(self):
        #Weight method per class
        raw_value = self.raw_metrics["WMCOnto2"]
        return self.evaluate_last_single_thresholds([15,11,8,5], raw_value)

    def DITOnto(self):
        #Depth of subsumption hierarchy
        raw_value = self.raw_metrics["DITOnto"]
        return self.evaluate_pair_thresholds([8, 6, 4, 2, 1], raw_value)

    def NACOnto(self):
        #Number of Ancestor Classes
        raw_value = self.raw_metrics["NACOnto"]
        return self.evaluate_pair_thresholds([8, 6, 4, 2, 1], raw_value)

    def NOCOnto(self):
        #Number of Children Concepts
        raw_value = self.raw_metrics["NOCOnto"]
        return self.evaluate_pair_thresholds([12, 8, 6, 3, 1], raw_value)
    
    def CBOOnto(self):
        #Coupling between objects
        raw_value = self.raw_metrics["CBOOnto"]
        return self.evaluate_pair_thresholds([8, 6, 4, 2, 1], raw_value)

    def RFCOnto(self):
        raw_value = self.raw_metrics["RFCOnto"]
        return self.evaluate_pair_thresholds([12, 8, 6, 3, 1], raw_value)
    
    def NOMOnto(self):
        raw_value = self.raw_metrics["NOMOnto"]
        return self.evaluate_last_single_thresholds([8,6,4,2], raw_value)

    def TMOnto2(self):
        raw_value = self.raw_metrics["TMOnto2"]
        return self.evaluate_pair_thresholds([8, 6, 4, 2, 1], raw_value)

    #Percetage driven metrics
    def RROnto(self):
        raw_value = self.raw_metrics["RROnto"]
        return self.evaluate_percentage(raw_value)

    def PROnto(self):
        raw_value = self.raw_metrics["PROnto"]
        return self.evaluate_percentage(raw_value)

    def AROnto(self):
        raw_value = self.raw_metrics["AROnto"]
        return self.evaluate_percentage(raw_value)
    
    def INROnto(self):
        raw_value = self.raw_metrics["INROnto"]
        return self.evaluate_percentage(raw_value)

    def ANOnto(self):
        raw_value = self.raw_metrics["ANOnto"]
        return self.evaluate_percentage(raw_value)

    def scalate_raw_metrics(self):
        self.scaled["LCOMOnto"] = self.LCOMOnto()
        self.scaled["WMCOnto2"] = self.WMCOnto2()
        self.scaled["DITOnto"] = self.DITOnto()
        self.scaled["NACOnto"] = self.NACOnto()
        self.scaled["NOCOnto"] = self.NOCOnto()
        self.scaled["CBOOnto"] = self.CBOOnto()
        self.scaled["RFCOnto"] = self.RFCOnto()
        self.scaled["NOMOnto"] = self.NOMOnto()
        self.scaled["TMOnto2"] = self.TMOnto2()
        self.scaled["RROnto"] = self.RROnto()
        self.scaled["PROnto"] = self.PROnto()
        self.scaled["AROnto"] = self.AROnto()
        self.scaled["INROnto"] = self.INROnto()
        self.scaled["ANOnto"] = self.ANOnto()
        return self.scaled

if __name__ == "__main__":

    #replace this path for other ontologies in Turtle format
    nameOntology = "ioto-protege"
    M = Metricas("../iot_ontologies/"+nameOntology+".ttl")
    
    raw_metrics = {
    "LCOMOnto": M.LCOMOnto(),
    "WMCOnto2": M.WMCOnto2(),
    "DITOnto": M.DITOnto(),
    "NACOnto": M.NACOnto(),
    "NOCOnto": M.NOCOnto(),
    "CBOOnto": M.CBOOnto(),
    "RFCOnto": M.RFCOnto(),
    "NOMOnto": M.NOMOnto(),
    "RROnto": M.RROnto(),
    "PROnto": M.PROnto(),
    "AROnto": M.AROnto(),
    "INROnto": M.INROnto(),
    "ANOnto": M.ANOnto(),
    "TMOnto2": M.TMOnto2(),
    }

    print("raw values")
    print(raw_metrics)

    print("scaled values")
    S = ScaledMetrics(raw_metrics)
    print(S.scalate_raw_metrics())
    
    

    


