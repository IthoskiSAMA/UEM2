var inputCedula = document.getElementById('inputCedula');
inputCedula.onblur = function(e) {
    e.preventDefault();
    verificarDocente(this.value);
};
// agregarDocente
$('#form-datos-generales-docente').on('submit', function (e) {
    e.preventDefault();
    eliminarEspacios();
    var formData = new FormData(this);
    $.ajax({
        type: "POST",
        url: "/doc-agg-info-general-docente/",
        data: formData,
        dataType: "json",
        cache: false,
        contentType: false,
        processData: false
    })
    .done(function (response) {
        insertar_alerta("Información registrada exitosamente", "div-informacion-general", "success");
        var docente_id = document.getElementById('docente_id');
        docente_id.value = response['docente_id'];
        document.getElementById('btnGuardarInfoGeneral').className = "btn btn-primary disabled";
        mostrarSecciones();
    })
    .fail(function (response) {
        //insertar_alerta("Ocurrió un error al registrar", "div-informacion-general", "danger");
        abrirModalInformativo(icon_error, "Aviso", "No se ha podido registrar al estudiante");
    });
});

var btn_subir_foto = document.getElementById('btnSubirFoto');
var input_foto_perfil = document.getElementById('inputFotoPerfilDocente');
var img_subida = document.getElementById('imgSubida');

btn_subir_foto.onclick = function (e) {
    if (document.getElementById('docente_id').value !== "0") {
        input_foto_perfil.click();
        input_foto_perfil.onchange = function() {
            var archivos = input_foto_perfil.files;
            if (!archivos || !archivos.length) {
                abrirModalInformativo(icon_warning, "¡Aviso!", "No se pudo agregar la imagen");
                return;
            }
            else {
                var primerArchivo = archivos[0];
                var objectURL = URL.createObjectURL(primerArchivo);
                img_subida.src = objectURL;

                var btnSubmitFotoPerfil = document.getElementById('btnSubmitFotoPerfil');
                btnSubmitFotoPerfil.hidden = false;
            }
        };
    } else {
        abrirModalInformativo(icon_info, "¡Información!", "Registre primero un Docente");
    }
    
}



$('#form-foto-perfil-docente').on('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(this);
    formData.append('docente_id', document.getElementById('docente_id').value);
    $.ajax({
        type: "POST",
        url: "/doc-agg-foto-perfil/",
        data: formData,
        dataType: "json",
        cache: false,
        contentType: false,
        processData: false
    })
    .done(function (response) {
        insertar_alerta("Foto guardada exitosamente", "div-informacion-general", "success");
        document.getElementById('btnSubmitFotoPerfil').className = "btn btn-primary w-100 disabled";
    })
    .fail(function (response) {
        insertar_alerta("Ocurrió un error al guardar la foto", "div-informacion-general", "danger");
    });
});

///
//$('#form-datos-generales-docente').on('submit', function (e) {
//    e.preventDefault();
//    eliminarEspacios();
//    var formData = new FormData(this);
//    $.ajax({
//        type: "POST",
//        url: "/doc-agg-info-general-docente/",
//        data: formData,
//        dataType: "json",
//        cache: false,
//        contentType: false,
//        processData: false
//    })
//    .done(function (response) {
//        insertar_alerta("Información registrada exitosamente", "div-informacion-general", "success");
//        var docente_id = document.getElementById('docente_id');
//        docente_id.value = response['docente_id'];
//        document.getElementById('btnGuardarInfoGeneral').className = "btn btn-primary disabled";
//        mostrarSecciones();
//    })
//    .fail(function (response) {
//        //insertar_alerta("Ocurrió un error al registrar", "div-informacion-general", "danger");
//        abrirModalInformativo(icon_error, "Aviso", "No se ha podido registrar al estudiante");
//    });
//});

///