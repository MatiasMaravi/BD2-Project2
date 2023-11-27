
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


 function obtenerToken() {
  const clientId = '6e1e00e04e804167834f5aac05e5279f';
  const clientSecret = 'ea872997f65241b5a0523a4db217fd3f';
  const authURL = 'https://accounts.spotify.com/api/token';
  const authString = btoa(`${clientId}:${clientSecret}`);

  const data = new URLSearchParams();
  data.append('grant_type', 'client_credentials');

  return fetch(authURL, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${authString}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: data,
  })
  .then(response => response.json())
  .then(tokenData => tokenData.access_token)
  .catch(error => {
    console.error('Error al obtener el token de acceso:', error);
    return null;
  });
}


function mostrarIndice() {
    var consulta_i = document.getElementById("consult_i").value;
    var topk = document.getElementById("topk").value;
    var metodo = document.getElementById("options").value;
    var selectedLanguage= document.getElementById("language").value;


    var formData = new FormData();
    formData.append('consulta_i', consulta_i);
    formData.append('topk', topk);
    formData.append('metodo', metodo);
    formData.append('language',selectedLanguage)

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
        const tiempoEnSegundos = data.tiempo_ejecucion * 1000;  // Convierte milisegundos a segundos
        tiempoEjecucion.textContent = 'Tiempo de ejecución: ' + tiempoEnSegundos + ' ms';
        tiempoEjecucion.id = "tiempo-ejecucion";  // Asigna un ID al elemento
        resultTable.parentNode.insertBefore(tiempoEjecucion, resultTable);  // Inserta antes de la tabla

        // Agrega las cabeceras a la tabla
        const headerRow = document.createElement('tr');
        const header1 = document.createElement('th');
        const header2 = document.createElement('th');
        const header3 = document.createElement('th');
        const header4 = document.createElement('th');
        const header5 = document.createElement('th');
        const header6 = document.createElement('th');

        header1.textContent = 'Track Name';
        header2.textContent = 'Playlist Name';
        header3.textContent = 'Track Artist';
        header4.textContent = 'Lyrics';
        header5.textContent= 'Rank';
        header6.textContent = 'Audio';

        headerRow.appendChild(header1);
        headerRow.appendChild(header2);
        headerRow.appendChild(header3);
        headerRow.appendChild(header4);
        headerRow.appendChild(header5);
        headerRow.appendChild(header6);

        resultBody.appendChild(headerRow);

        // Recorre los datos y crea filas en la tabla
        data.resultados.forEach(resultado => {
            const newRow = document.createElement('tr');
    const column1 = document.createElement('td');
    const trackButton = document.createElement('button');

    const modal = document.getElementById('modal');

    trackButton.textContent = resultado.track_name;
    // Establecer el texto del botón




trackButton.addEventListener('click', function() {
  modal.style.display = 'block';

  fetch('/obtener_datos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ song_id: resultado.track_id })
        })
    .then(response => response.json())
    .then(data => {

        console.log(resultado.track_id);
        console.log('Datos recibidos desde Flask:', data);
      const trackIds = data.map(item => item.track_id);

      fetch('./static/spotify_songs.csv')
        .then(response => response.text())
        .then(csvData => {
          const parsedData = Papa.parse(csvData, { header: true }).data;
          const filteredSongs = parsedData.filter(song => trackIds.includes(song.track_id));

          const dataTable = document.getElementById('data-body');
          dataTable.innerHTML = '';



filteredSongs.forEach(song => {
  obtenerToken().then(accessToken => {
    if (accessToken) {
      fetch(`https://api.spotify.com/v1/tracks/${song.track_id}`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      })
      .then(response => response.json())
      .then(trackData => {
        const dataTable = document.getElementById('data-body');

        const row = document.createElement('tr');
        const cell1 = document.createElement('td');
        const cell2 = document.createElement('td');
        const cell3 = document.createElement('td');
        const cell4 = document.createElement('td');

        cell1.textContent = song.track_id;
        cell2.textContent = song.track_name;

        if (trackData.album && trackData.album.images && trackData.album.images.length > 0) {
          const image = document.createElement('img');
          image.src = trackData.album.images[0].url; // Obtener el URL de la primera imagen
          image.alt = 'Track Image'; // Añadir un texto alternativo para la imagen
          image.width = 100; // Definir un ancho (opcional)
          cell3.appendChild(image);
        } else {
          cell3.textContent = 'No image available';
        }


        const audioPlayer = document.createElement('audio');
        audioPlayer.controls = true;
        audioPlayer.src = `./static/audios/${song.track_id}.mp3`;

        cell4.appendChild(audioPlayer);

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);

        dataTable.appendChild(row);
      })
      .catch(error => {
        console.error('Error al obtener datos de la pista:', error);
      });
    }
  });
});


        })
        .catch(error => {
          console.error('Error al cargar spotify.csv:', error);
        });
    })
    .catch(error => {
      console.error('Error al cargar datos.json:', error);
    });
});







    const closeBtn = document.querySelector('.close');
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    const column2 = document.createElement('td');
    const column3 = document.createElement('td');


    const column4 = document.createElement('td');
    const LyricsButton = document.createElement('button');

    const modal2 = document.getElementById('modal2');
    const modal2content = document.getElementById('modal2content');

    LyricsButton.textContent = resultado.track_name;


LyricsButton.addEventListener('click', function() {
    modal2.style.display = 'block';

    const cell1 = document.createElement('p');
    const lyrics = resultado.lyrics;

    // Palabra específica a resaltar (cambiar 'palabra' por la palabra deseada)
    const palabraEspecifica = consulta_i;

    // Dividir el texto en palabras individuales
    const palabras = lyrics.split(/\s+/);

    // Crear un nuevo fragmento para almacenar el contenido con las palabras resaltadas
    const fragment = document.createDocumentFragment();

    palabras.forEach(palabra => {
        // Eliminar signos de puntuación alrededor de la palabra para la comparación
        const palabraLimpia = palabra.replace(/[.,\/#!$¡%\^&\*;:{}=\-_`~()]/g, '');

        // Comparar la palabra con la palabra específica (ignorando mayúsculas y minúsculas)
        if (palabraLimpia.toLowerCase() === palabraEspecifica.toLowerCase()) {
            const strong = document.createElement('strong');
            strong.textContent = palabra + ' '; // Agregar espacio después de la palabra
            fragment.appendChild(strong);
        } else {
            const textNode = document.createTextNode(palabra + ' ');
            fragment.appendChild(textNode);
        }
    });

    // Agregar el fragmento con las palabras resaltadas al elemento cell1
    cell1.appendChild(fragment);

    // Agregar cell1 al modal (modal2)
    modal2content.appendChild(cell1);
});




    const closeBtn2 = document.querySelector('.close2');
    closeBtn2.addEventListener('click', function() {
        modal2.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal2) {
            modal2.style.display = 'none';
        }
    });





    const column5 = document.createElement('td');
    const column6 = document.createElement('td');

    const audioPlayer2 = document.createElement('audio');
    audioPlayer2.controls = true;
    audioPlayer2.src = `./static/audios/${resultado.track_id}.mp3`;

    column6.appendChild(audioPlayer2);

    column2.textContent = resultado.playlist_name;
    column3.textContent = resultado.track_artist;

    column5.textContent = resultado.rank;

            column1.appendChild(trackButton);
            column4.appendChild(LyricsButton);
            newRow.appendChild(column1);
            newRow.appendChild(column2);
            newRow.appendChild(column3);
            newRow.appendChild(column4);
            newRow.appendChild(column5);
            newRow.appendChild(column6);

            resultBody.appendChild(newRow);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}








