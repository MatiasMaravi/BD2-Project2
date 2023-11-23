# Maldición de la dimensionalidad
En resumidas palabras, Richard Bellman en el año 1956 acuñó esta frase para referirse a los problemas que pueden conllevar trabajar con el exceso de variables independientes. Cabe resaltar que esta terminología se utiliza en el campo de Ciencia de Datos, específicamente en Machine Learning.

El problema surge cuando se requiere trabajar con muchas dimensiones. Como se mencionó anteriormente, por lo general es un problema relacionado a Machine Learning. Esto conlleva a que un modelo no pueda ser lo más preciso posible ya que se pueden obtener variables poco importantes, además de los tipos de estas variables.

En la página de Rubén Fernández y compañía, se menciona un ejemplo con los *k-vecinos más cercanos (KNN)* y explica completamente el funcionamiento de este método. Al final de este subtema, llega a la conclusión de que va a ser más difícil hallar los vecinos más cercanos cuando el valor de *k* es pequeño.

Una de las posibles soluciones es la descomposición de estas características. Esto se logra separando aquellas variables que sean ortogonales, es decir, que no dependan de otras. Por lo visto en curso, lo podemos relacionar directamente con el tema de *"Fragmentación"* o *"Formas Normales"*. Otra solución propuesta, en el ámbito de Machine Learning, es aumentar los datos de entrenamiento para evitar el sobreajuste de datos.

# Fuentes
- Bellman, R. (1961). *Adaptive Control Processes: a guided tour*. Princeton University Press.
- Fernández, R., Costa, J., Oviedo, M. (10 de febrero de 2021). *1.4 La maldición de la dimensionalidad*. Aprendizaje Estadístico. Recuperado el 22 de noviembre de 2023 de https://rubenfcasal.github.io/aprendizaje_estadistico/dimen-curse.html
- Arrioja, N. (11 de octubre de 2021). *La maldición de la dimensionalidad*. Medium. https://medium.com/@nicolasarrioja/la-maldici%C3%B3n-de-la-dimensionalidad-f7a6248cf9a