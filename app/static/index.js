
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
    console.log(consulta_i,topk,metodo);

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
        document.getElementById("result").innerHTML = data.distancia ;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

