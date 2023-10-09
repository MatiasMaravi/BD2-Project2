from src.classes.InvertIndex import InvertIndex

textos = ["libro1.txt","libro2.txt","libro3.txt","libro4.txt","libro5.txt","libro6.txt"]
A1 = InvertIndex("indice_invertido.json")
A1.building(textos)

valores = A1.retrieval("Frodo viaja a obtener los anillos", 6)
print(valores)

valores = A1.retrieval("""La obra comienza con la noticia de la celebración del 111º cumpleaños de Bilbo Bolsón en la Comarca. Sin embargo, para Bilbo esta gran fiesta tenía como motivo principal su partida hacia su último viaje, producto del deseo de terminar sus días en paz y tranquilidad. El mago Gandalf, amigo de Bilbo y quien estaba informado de la decisión del hobbit, también acudió a la fiesta. Tras el discurso pronunciado por Bilbo, este se puso su anillo mágico y desapareció ante los sorprendidos hobbits. Gandalf, que sabía bien lo que acababa de hacer Bilbo, le encontró en Bolsón Cerrado y allí tuvo una pequeña discusión con él, ya que se negaba a dejar el anillo junto con el resto de la herencia a su sobrino Frodo; sin embargo, el mago acabó convenciéndole y Bilbo al fin partió. Entonces, debido a las dudas que le estaba ocasionando el anillo, Gandalf parte en busca de información sobre él, no sin antes informar a Frodo de que lo guarde y no lo toque.


Casi veinte años después, Gandalf regresa a Bolsón Cerrado y le cuenta a Frodo lo que había descubierto sobre el Anillo: que se trataba del mismo que el Rey Isildur de Arnor le había arrebatado al Señor oscuro Sauron y que muchos años después había sido encontrado por la criatura Gollum tras haberse perdido en el río Anduin durante el Desastre de los Campos Gladios. Ambos quedaron entonces en reunirse de nuevo en la aldea de Bree con el fin de llevar luego el Anillo Único a Rivendel, donde los sabios decidirían sobre su destino. Junto con su jardinero Samsagaz Gamyi, Frodo traza un plan para salir de la Comarca con el pretexto de irse a vivir a Los Gamos; pero el plan acaba siendo descubierto por otros dos amigos, Pippin y Merry, que deciden acompañarle también.

Tras adentrarse en el Bosque Viejo con el fin de evitar los caminos, los hobbits son atrapados por el Viejo Hombre-Sauce, un ucorno, que les tiende una trampa; sin embargo, son salvados por un misterioso personaje llamado Tom Bombadil. Tras pasar unos días en su casa, los hobbits parten de nuevo hacia Bree, pero acaban perdidos debido a la niebla y llegan a las Quebradas de los Túmulos. Allí son capturados por los Tumularios, pero de nuevo, tras cantar Frodo una canción que Tom Bombadil le enseñó, este acude en su ayuda y les salva, dándoles unas armas tumularias para que pudieran defenderse en su viaje.

Una vez en Bree, los hobbits acuden a la posada «El Póney Pisador» donde Frodo había quedado con Gandalf. Accidentalmente, el hobbit se pone el Anillo y alerta así a los Nazgûl, los servidores de Sauron que le persiguen para arrebatárselo. Gracias a un amigo de Gandalf, llamado Aragorn, y al hobbit Nob, logran salvarse cuando los Nazgûl atacan la posada esa noche. Al día siguiente, acompañados por Aragorn, los hobbits parten hacia Rivendel. En su parada en Amon Sûl, los Nazgûl les atacan de nuevo, esta vez hiriendo a Frodo de gravedad. Tras combatirles, logran escapar y llegar cerca del vado de Bruinen, donde se encuentran con Glorfindel, un elfo de la casa de Elrond, que les acompaña hasta Rivendel. De nuevo perseguidos, Glorfindel ordena a su caballo Asfaloth que se adelante llevando a Frodo montado y, al llegar al río, los Nazgûl son arrastrados por su corriente gracias al poder de Rivendel.""",6)

print(valores)