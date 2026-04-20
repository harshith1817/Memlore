import spacy

nlp=spacy.load("en_core_web_sm")

#Simple in-memory graph
graph={}

def extract_entities(text):
    doc=nlp(text)
    return [ent.text for ent in doc.ents]


def add_edge(a,b):
    if a not in graph:
        graph[a]=set
    if b not in graph:
        graph[b]=set
    graph[a].add(b)
    graph[b].add(a)
    

def build_graph(text):
    entities=extract_entities(text)
    for i in range(len(entities)):
        for j in range(i+1, len(entities)):
            add_edge(entities[i], entities[j])
            

def expand_query(query):
    entities=extract_entities(query)
    related=[]
    for e in entities:
        if e in graph:
            related.extend(list(graph[e]))
    return query+" "+" ".join(related)