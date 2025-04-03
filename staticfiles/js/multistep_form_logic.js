document.addEventListener("DOMContentLoaded", function () { 
  const form = document.querySelector("form");

  // Al enviar, enfoca el primer campo inválido si hay errores
  form.addEventListener("submit", function (e) {
    const invalidFields = form.querySelectorAll(":invalid");
    if (invalidFields.length > 0) {
      invalidFields[0].scrollIntoView({ behavior: "smooth", block: "center" });
      invalidFields[0].focus();
    }
  });

  // Marcar campos válidos/incorrectos dinámicamente y mostrar icono + tooltip
  const inputs = form.querySelectorAll("input, select, textarea");

  inputs.forEach((input) => {
    const icon = document.createElement("span");
    icon.innerHTML = "❗";
    icon.style.marginLeft = "8px";
    icon.style.color = "red";
    icon.style.display = "none";
    icon.setAttribute("title", "Por favor corrija este campo");
    input.parentNode && input.parentNode.appendChild(icon);

    const updateValidation = () => {
      if (input.checkValidity()) {
        input.classList.add("is-valid");
        input.classList.remove("is-invalid");
        icon.style.display = "none";
      } else {
        input.classList.add("is-invalid");
        input.classList.remove("is-valid");
        icon.style.display = "inline";
      }
    };

    input.addEventListener("input", updateValidation);
    input.addEventListener("blur", updateValidation);
  });

  // ✅ Calcular edad automáticamente al cambiar la fecha de nacimiento
  const fechaNacimientoInput = document.getElementById("id_fecha_nacimiento");
  const edadInput = document.getElementById("id_edad");

  function calcularEdad(fechaNacimiento) {
    const hoy = new Date();
    const nacimiento = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const m = hoy.getMonth() - nacimiento.getMonth();

    if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }
    return edad;
  }

  if (fechaNacimientoInput && edadInput) {
    fechaNacimientoInput.addEventListener("change", function () {
      const fechaSeleccionada = this.value;
      if (fechaSeleccionada) {
        edadInput.value = calcularEdad(fechaSeleccionada);
      }
    });
  }
});
