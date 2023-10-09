from src.classes.InvertIndex import InvertIndex

# textos = ["libro1.txt","libro2.txt","libro3.txt","libro4.txt","libro5.txt","libro6.txt"]
A1 = InvertIndex("indice_invertido.json")
# A1.building(textos)

valores = A1.retrieval("Frodo viaja a obtener los anillos", 6)
print(valores)