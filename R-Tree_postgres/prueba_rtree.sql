
-- Creamos la tabla de acuerdo a los datos que tenemos

create extension cube;

create table if not exists Ropa(
    id integer,
    vector_caracteristico cube
);

-- Insertamos los datos

insert into Ropa(id, vector_caracteristico)
    select id,
    cube(ARRAY[(random()*1000),
				(random()*1000),
				(random()*1000),
				(random()*1000),
			  	(random()*1000),
				(random()*1000),
				(random()*1000),
				(random()*1000)])
    from generate_series(1, 1000) id;

-- Creamos el indice GIST

create index idx_ropa_vector on Ropa using gist(vector_caracteristico);

-- Realizamos una consulta para obtner las prendas mas parecidas sobre un determinado vector

SELECT id,
        cube_distance(vector_caracteristico, '(636, 616, 699, 338, 69 ,7 ,9 , 20)') as D
FROM Ropa
ORDER BY vector_caracteristico <-> '(636, 616, 699, 338, 69 ,7 ,9 , 20)'
LIMIT 10;