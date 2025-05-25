// Variables de los elementos
const dropAreas = document.querySelectorAll('.drop-area');
const fileInputs = document.querySelectorAll('input[type="file"]');

// Función para manejar eventos de drag sobre las áreas
dropAreas.forEach((dropArea, index) => {
    // Prevenir comportamiento por defecto en los eventos dragenter y dragover
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropArea.classList.add('hover');
        });
    });

    // Eliminar estilo hover cuando el archivo sale del área
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            dropArea.classList.remove('hover');
        });
    });

    // Cuando se suelta el archivo en el área
    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];  // Solo tomamos el primer archivo

        if (file && file.name.endsWith('.txt')) {
            // Subir el archivo al servidor correspondiente
            uploadFile(file, index);
        } else {
            alert('Solo se permiten archivos .txt');
        }
    });

    // Hacer clic sobre el área para activar el selector de archivos
    dropArea.addEventListener('click', () => {
        fileInputs[index].click();
    });
});

// Subir archivo usando AJAX
function uploadFile(file, index) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            alert(data);
            location.reload();  // Recargar la página para mostrar el archivo subido
        })
        .catch(error => {
            alert('Error al subir el archivo.');
        });
}

// Si un archivo es seleccionado desde el explorador de archivos, subirlo
fileInputs.forEach((fileInput, index) => {
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file && file.name.endsWith('.txt')) {
            uploadFile(file, index);
        } else {
            alert('Solo se permiten archivos .txt');
        }
    });
});
