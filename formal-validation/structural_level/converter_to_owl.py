from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL

def convertOWL(nameOntology):    
    g = Graph()
    g.parse(nameOntology, format="turtle")
    namefile = '../iot_ontologies/ssn.rdf'
    g.serialize(destination=namefile,format='xml')
    
convertOWL("../iot_ontologies/ssn.ttl")
