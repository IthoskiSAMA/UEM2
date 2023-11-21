$('#form-datos-generales-docente').on('submit', function (e) { 
    e.preventDefault();
    eliminarEspacios();
    var formData = new FormData(this);
    $.ajax({
        type: "POST",
        url: "/doc-editar-info-general-docente/",
        data: formData,
        dataType: "json",
        cache: false,
        contentType: false,
        processData: false
    })
    .done(function (response) {
        abrirModalInformativo(icon_success, "¡Felicitaciones!", "Se ha modificado correctamente los datos del estudiante");
    })
    .fail(function (response) {
        abrirModalInformativo(icon_error, "Error", "No se ha podido editar los datos del estudiante");
    });
});

var btn_cambiar_foto = document.getElementById('btnCambiarFoto');
var input_foto_perfil = document.getElementById('inputFotoPerfilDocente');
var img_subida = document.getElementById('imgSubida');

btn_cambiar_foto.onclick = function (e) {
    e.preventDefault();
    input_foto_perfil.click();
    input_foto_perfil.onchange = function() {
        var archivos = input_foto_perfil.files;
        if (!archivos || !archivos.length) {
            abrirModalInformativo(icon_warning, "¡Aviso!", "No se pudo agregar la imagen");
            return false;
        }
        else {
            var primerArchivo = archivos[0];
            var objectURL = URL.createObjectURL(primerArchivo);
            img_subida.src = objectURL;

            var btnSubmitFotoPerfil = document.getElementById('btnSubmitFotoPerfil');
            btnSubmitFotoPerfil.hidden = false;
        }
    };
}

$('#form-foto-perfil-docente').on('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(this);
    formData.append('docente_id', document.getElementById('docente_id').value);
    $.ajax({
        type: "POST",
        url: "/doc-editar-foto-perfil-docente/",
        data: formData,
        dataType: "json",
        cache: false,
        contentType: false,
        processData: false
    })
    .done(function (response) {
        abrirModalInformativo(icon_success, "¡Felicitaciones!", "Foto editada exitosamente");
    })
    .fail(function (response) {
        abrirModalInformativo(icon_error, "¡Error!", "No se ha podido editar la foto del docente");
    });
});
