from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL

def convertOWL(nameOntology):    
    g = Graph()
    g.parse(nameOntology, format="xml")
    namefile = '../input_ontologies/propuestaTurtle.owl'
    g.serialize(destination=namefile,format='turtle')
    
convertOWL("../input_ontologies/ontoSLAM.owl")

