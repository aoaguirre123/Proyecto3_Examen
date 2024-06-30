$(document).ready(function() {

  // Asignar placeholders para ayudar a los usuarios
  $('#id_username').attr('placeholder', 'Ingrese un nombre de usuario');
  $('#id_first_name').attr('placeholder', 'Ingrese sus nombres');
  $('#id_last_name').attr('placeholder', 'Ingrese sus apellidos');
  $('#id_email').attr('placeholder', 'Ingrese su correo electrónico');
  $('#id_rut').attr('placeholder', 'Ingrese su RUT (sin puntos y con guión)');
  $('#id_direccion').attr('placeholder', 'Ingrese su dirección');

  // Cambiar el texto del combo de Tipo de usuario por "Seleccione un tipo de usuario"
  var select = document.querySelector('select[name="tipo_usuario"]');
  if (select) {
      var defaultOption = select.querySelector('option[value=""]');
      if (defaultOption) {
          defaultOption.text = "Seleccione un tipo de usuario";
      }
  }

  // Agregar una validación por defecto para que la imagen la exija como campo obligatorio
  $.extend($.validator.messages, {
    required: "Este campo es requerido",
  });

  $('#form').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'tipo_usuario': {
          required: true,
          inList: ['Cliente', 'Administrador'],
        },
        'first_name': {
          required: true,
          soloLetras: true,
        },
        'last_name': {
          required: true,
          soloLetras: true,
        },
        'email': {
          required: true,
          emailCompleto: true,
        },
        'rut': {
          required: true,
          rutChileno: true,
        },
        'direccion': {
          required: true,
        },
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'tipo_usuario': {
          required: 'Debe ingresar un tipo de usuario',
          inList: 'Debe ingresar un tipo de usuario',
        },
        'first_name': {
          required: 'Debe ingresar su nombre',
          soloLetras: "El nombre sólo puede contener letras y espacios en blanco",
        },
        'last_name': {
          required: 'Debe ingresar sus apellidos',
          soloLetras: "Los apellidos sólo pueden contener letras y espacios en blanco",
        },
        'email': {
          required: 'Debe ingresar su correo',
          emailCompleto: 'El formato del correo no es válido',
        },
        'rut': {
          required: 'Debe ingresar su RUT',
          rutChileno: 'El formato del RUT no es válido',
        },
        'direccion': {
          required: 'Debe ingresar su dirección',
        },
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('error-message'); // Aplica una clase al mensaje de error
      },
  });

  $('#id_generar_password').click(function() {
    $("#change_password_indicator").val("Nuevo valor del campo");
    $("#change_password_username").val("Nuevo valor del campo");
  });

});

