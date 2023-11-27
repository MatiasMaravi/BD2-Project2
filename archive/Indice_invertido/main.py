from invert_index import InvertIndex

textos = ["doc1.txt","doc2.txt","doc3.txt","doc4.txt","doc5.txt","doc6.txt"]
A1 = InvertIndex("indice_invertido.json")
A1.building(textos)

