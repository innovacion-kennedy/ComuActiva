const cursosPorArea = {
  Deporte: ["Microfutbol", "Fútbol", "Basketball", "Voleibol"],
  Cultura: ["Danza", "Baile", "Fotografía", "Pintura"],
};

function actualizarCursos() {
  const areaSeleccionada = document.querySelector('input[name="area_encargada"]:checked');
  const selectCursos = document.getElementById("id_cursos");

  if (!areaSeleccionada || !selectCursos) return;

  const area = areaSeleccionada.value;
  const cursos = cursosPorArea[area] || [];

  // Limpiar opciones anteriores
  selectCursos.innerHTML = '<option value="">Seleccione un curso</option>';

  // Agregar nuevas opciones
  cursos.forEach((curso) => {
    const option = document.createElement("option");
    option.value = curso;
    option.textContent = curso;
    selectCursos.appendChild(option);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const deporteRadio = document.getElementById("deporte");
  const culturaRadio = document.getElementById("cultura");

  if (deporteRadio) deporteRadio.addEventListener("change", actualizarCursos);
  if (culturaRadio) culturaRadio.addEventListener("change", actualizarCursos);

  actualizarCursos(); // Ejecutar al cargar la página
});
