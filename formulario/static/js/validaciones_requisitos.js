document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (e) {
        const inputs = form.querySelectorAll('input[type="file"]');
        for (let input of inputs) {
            if (!input.files.length) {
                alert("Todos los documentos deben estar adjuntos.");
                e.preventDefault();
                return;
            }
        }
    });
});
