

function verificarDocente(cedula) {
    var csrftoken = getCookie('csrftoken');
         $.ajax({
             type: "POST",
             url: "/doc-verificar-existe/",
             data: {"cedula": cedula, csrfmiddlewaretoken: csrftoken },
             dataType: "json"
         })
         .done(function (response) {
             if (response["resultado"] === 1) {
                 inputCedula.className = "form-control input-success";
                 document.getElementById('btnGuardarInfoGeneral').disabled = false;
             }
             else if (response["resultado"] === 0) {
                 inputCedula.className = "form-control input-error";
                 document.getElementById('btnGuardarInfoGeneral').disabled = true;
                abrirModalInformativo(icon_info, "¡Información!", "Ya existe un docente registrado con el mismo número de cédula");
             }
         })
         .fail(function (response) {
             abrirModalInformativo(icon_error, "¡Error!", "Ha ocurrido un error al intentar eliminar el docente");
         });
}
// Función para ELIMINAR ESTUDIANTE
function eliminarDocente (docente_id) {
    abrirModalDeAcciones(icon_warning, "Eliminar Docente", "¿Está usted seguro de eliminar este Docente?", "Eliminar", "danger");
    document.getElementById("btnAccion").onclick = function(e) {
        e.preventDefault();
        cerrarModalDeAcciones();
        abrirModalInformativo(icon_info, "Permisos de SuperUsuario", "Se ha enviado una solicitud de permisos para borrar el estudiante.");
        /*var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: "/est-eli-estudiante/",
            data: {"estudiante_id": estudiante_id, csrfmiddlewaretoken: csrftoken },
            dataType: "json"
        })
        .done(function (response) {
            document.getElementById('estudiante-' + estudiante_id).remove();
            abrirModalInformativo(icon_info, "¡Información!", "Estudiante eliminado correctamente");
        })
        .fail(function (response) {
            abrirModalInformativo(icon_error, "¡Error!", "Ha ocurrido un error al intentar eliminar el estudiante");
        });*/
    };
};

