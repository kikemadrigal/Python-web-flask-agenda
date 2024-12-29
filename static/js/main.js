ruta_base = "http://127.0.0.1:3000/";
//ruta_base = "https://agenda-ai2z.onrender.com/";

window.onload = function () {
    // Ocultamos los checkbox pagados si no está marcado el activado
    // Enl marcado de los checkbox asistenca es lo 1 que se ha hecho en php
    marcar_checkbox_deportes_asignados_usuario();
}

/**
 Existen 3 formas de hacer peticiones GET, POST; PUT y DELETE sin tener que recgargar la página
 1. Con el objeto XMLHttpRequest
 2 COn la aAPI fecth. con el objeto https://developer.mozilla.org/es/docs/Web/API/fetch
 3 Utilizando una librería externa, en nuestro caso utilizamos axios: https://axios-http.com/docs/intro, axios trabaja con promesas o .then(reponse...)
 */



function checkbox_deporte_click(checkbox) {
    var id_checkbox=checkbox.id;
    var nombre_usuario=document.getElementById("nombre_usuario").value;
    console.log("Checkbox activado: " + id_checkbox);
    const deporte_usuario = {
        nombre_deporte: id_checkbox,
        nombre_usuario: nombre_usuario
    };
    if (checkbox.checked) {  
        //Se añade en la tabla deporte_usuario el deporte
        enviar_peticion_post(ruta_base + "api/add_deporte_usuario", deporte_usuario);
    }else{
        //Se elimina en la tabla deporte_usuario el deporte
        enviar_peticion_post(ruta_base + "api/delete_deporte_usuario", deporte_usuario); 
    }
}

//Esta forma es utilizando fetch+async+await
/*
async function enviar_peticion_post(url, data) {
    try {
        const response = await fetch(url, {
            method: "POST", // Cambia a "PUT" si tu API lo requiere
            headers:  {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify(data), // Convierte el objeto a una cadena JSON
        });
        // Verifica si la respuesta fue exitosa
        if (response.ok) {
            const result = await response.json(); // Convierte la respuesta a JSON            
            console.log("Actualizado con éxito:", result);
            document.location.reload();
        } else {
            console.error("Error al actualizar:", response.status, response.statusText);
        }
    } catch (error) {
        console.error("Hubo un error con la solicitud:", error);
    }
}
*/
// Esta es la forma sin utilizar axios
async function enviar_peticion_post(url, data) {
    axios.post(url, data, {headers: {'Access-Control-Allow-Origin': 'https://agenda-ai2z.onrender.com'}})
    .then(response => {
        console.log("Actualizado con mínimo:", response.data);
        document.location.reload();
    })
    .catch(error => {
        console.error("Hubo un error con la solicitud:", error);
    });

}

//Esta forma es con fetch+async+await
/*
async function marcar_checkbox_deportes_asignados_usuario () {
    var nombre_usuario=document.getElementById("nombre_usuario").value;
    const deportes_usuario = {
        nombre_usuario: nombre_usuario
    };
    //Obtenemos todos los deportes de un usuario
    try {
        //a través de post    
        const response = await fetch(ruta_base + "api/obtener_deportes_usuario", {
            method: "POST", // Cambia a "PUT" si tu API lo requiere
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify(deportes_usuario), // Convierte el objeto a una cadena JSON
        });
        //A través de GET
        //const response = await fetch(ruta_base + "api/obtener_deportes_usuario?nombre_usuario="+nombre_usuario, {
        //    method: "GET",
        //    headers: {
        //        'Content-Type': 'application/json',
        //        'Access-Control-Allow-Origin': '*'
        //    }
        //});
        // Verifica si la respuesta fue exitosa
        if (response.ok) {
            const results = await response.json(); // Convierte la respuesta a JSON            
            console.log("obtenidos los deportes de un usuario:", results);
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            for(let i=0; i<results.length; i++){
                var result=results[i];
                checkboxes.forEach(checkbox => {
                    if (checkbox.id==result[0]){
                        checkbox.checked = true;
                    }
                });
            }
        } else {
            console.error("Error al actualizar:", response.status, response.statusText);
        }
    } catch (error) {
        console.error("Hubo un error con la solicitud:", error);
    }
}
*/

//Esta forma es utilizando la librería axios
async function marcar_checkbox_deportes_asignados_usuario () {
    var nombre_usuario=document.getElementById("nombre_usuario").value;
    const deportes_usuario = {
        nombre_usuario: nombre_usuario
    };
    //Obtenemos todos los deportes de un usuario
    axios.post(ruta_base + "api/obtener_deportes_usuario", deportes_usuario, {headers: {'Access-Control-Allow-Origin': 'https://agenda-ai2z.onrender.com'}})
    //Con axios trabajamos con promesas
    .then(response => {
        console.log("obtenidos los deportes de un usuario:", response.data);
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        for(let i=0; i<response.data.length; i++){
            var result=response.data[i];
            checkboxes.forEach(checkbox => {
                if (checkbox.id==result[0]){
                    checkbox.checked = true;
                }
            });
        }
    })
    .catch(error => {
        console.error("Hubo un error con la solicitud:", error);
    });
}