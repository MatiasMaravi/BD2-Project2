
function mostrarCampos() {
            var selectedOption = document.getElementById("options").value;
            var consult_i = document.getElementById("consult_i");
            var topk = document.getElementById("topk");

            if (selectedOption === "own" || selectedOption === "postgres" || selectedOption === "mongodb") {
                consult_i.classList.remove("hidden");
                topk.classList.remove("hidden");
            } else {
                consult_i.classList.add("hidden");
                topk.classList.add("hidden");
            }
        }



function mostrarIndice() {
    var consulta_i = document.getElementById("consult_i").value;
    var topk = document.getElementById("topk").value;
    var metodo = document.getElementById("options").value;

    var formData = new FormData();
    formData.append('consulta_i', consulta_i);
    formData.append('topk', topk);
    formData.append('metodo', metodo);

    fetch('/mostrar_indice', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultTable = document.getElementById("result-table");
        const resultBody = document.getElementById("result-body");

        // Limpia el cuerpo de la tabla
        resultBody.innerHTML = '';

        // Borra el elemento del tiempo de ejecución si existe
        const tiempoEjecucionElement = document.getElementById("tiempo-ejecucion");
        if (tiempoEjecucionElement) {
            tiempoEjecucionElement.remove();
        }

        // Crea el nuevo elemento de tiempo de ejecución
        const tiempoEjecucion = document.createElement('p');
        tiempoEjecucion.textContent = 'Tiempo de ejecución: ' + data.tiempo_ejecucion + ' segundos';
        tiempoEjecucion.id = "tiempo-ejecucion";  // Asigna un ID al elemento
        resultTable.parentNode.insertBefore(tiempoEjecucion, resultTable);  // Inserta antes de la tabla

        // Agrega las cabeceras a la tabla
        const headerRow = document.createElement('tr');
        const header1 = document.createElement('th');
        const header2 = document.createElement('th');
        const header3 = document.createElement('th');
        const header4 = document.createElement('th');

        header1.textContent = 'Track Name';
        header2.textContent = 'Playlist Name';
        header3.textContent = 'Track Artist';
        header4.textContent = 'Rank';

        headerRow.appendChild(header1);
        headerRow.appendChild(header2);
        headerRow.appendChild(header3);
        headerRow.appendChild(header4);

        resultBody.appendChild(headerRow);

        // Recorre los datos y crea filas en la tabla
        data.resultados.forEach(resultado => {
            const newRow = document.createElement('tr');
            const column1 = document.createElement('td');
            const column2 = document.createElement('td');
            const column3 = document.createElement('td');
            const column4 = document.createElement('td');

            column1.textContent = resultado.track_name;
            column2.textContent = resultado.playlist_name;
            column3.textContent = resultado.track_artist;
            column4.textContent = resultado.rank;

            newRow.appendChild(column1);
            newRow.appendChild(column2);
            newRow.appendChild(column3);
            newRow.appendChild(column4);

            resultBody.appendChild(newRow);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}





