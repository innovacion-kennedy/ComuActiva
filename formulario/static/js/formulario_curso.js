console.log("✅ JS cargado correctamente");

// Esperar que el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
  const tipoCursoSelect = document.getElementById("id_tipo_curso");
  const disciplinaSelect = document.getElementById("id_disciplina");

  const disciplinasPorTipo = {
    Deporte: ["Microfútbol", "Baloncesto", "Atletismo", "Natación", "Fútbol"],
    Cultura: ["Danza", "Pintura", "Música", "Teatro", "Artesanía"]
  };

  function actualizarDisciplinas() {
    const tipoSeleccionado = tipoCursoSelect.value;
    const disciplinas = disciplinasPorTipo[tipoSeleccionado] || [];

    // Limpiar opciones anteriores
    disciplinaSelect.innerHTML = "";

    // Agregar nuevas opciones
    disciplinas.forEach(function (disciplina) {
      const option = document.createElement("option");
      option.value = disciplina;
      option.textContent = disciplina;
      disciplinaSelect.appendChild(option);
    });
  }

  // Inicializar con el valor por defecto
  actualizarDisciplinas();

  // Cambiar dinámicamente al cambiar el tipo de curso
  tipoCursoSelect.addEventListener("change", actualizarDisciplinas);
});
