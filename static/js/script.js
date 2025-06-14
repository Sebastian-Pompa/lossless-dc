const dropAreas = document.querySelectorAll('.drop-area');

const fileInputs = document.querySelectorAll('input[type="file"]');

const dropAreaCompression = document.getElementById('input_compression');
const dropAreaDecompressionBin = document.getElementById('input_decompression_file');
const dropAreaDecompressionCodes = document.getElementById('input_decompression_codes');

//  Buttons
const btnCompression = document.getElementById('btn_compression');
const btnDecompression = document.getElementById('btn_decompression');

//  Captions
const captionCompress = document.getElementById('caption_compress');
const captionDecompressBin = document.getElementById('caption_decompress_bin');
const captionDecompressCodes = document.getElementById('caption_decompress_codes');



let file_compression = null;
let file_decompression_bin = null;
let file_decompression_codes = null;

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

    // Hacer clic sobre el área para activar el selector de archivos
    dropArea.addEventListener('click', () => {
        fileInputs[index].click();
    });
});

// Cuando se suelta el archivo en el área de compresion
dropAreaCompression.addEventListener('drop', (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];

    if (file && file.name.endsWith('.txt')) {
        file_compression = file;
        dropAreaCompression.classList.add('uploaded');
        captionCompress.innerHTML = "archivo de texto cargado";
        btnCompression.classList.add('active');
    } else {
        alert('Solo se permiten archivos .txt');
    }
});

// Cuando se suelta el archivo binario en el área de descompresion
dropAreaDecompressionBin.addEventListener('drop', (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];

    if (file && file.name.endsWith('.bin')) {
        file_decompression_bin = file;
        dropAreaDecompressionBin.classList.add('uploaded');
        captionDecompressBin.innerHTML = "archivo binario cargado";
        if (file_decompression_bin && file_decompression_codes) {
            btnDecompression.classList.add('active');
        }
    } else {
        alert('Solo se permiten archivos .bin');
    }
});

// Cuando se suelta el archivo json en el área de descompresion
dropAreaDecompressionCodes.addEventListener('drop', (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];

    if (file && file.name.endsWith('.json')) {
        file_decompression_codes = file;
        dropAreaDecompressionCodes.classList.add('uploaded');
        captionDecompressCodes.innerHTML = "tabla de codificacion cargada";
        if (file_decompression_bin && file_decompression_codes) {
            btnDecompression.classList.add('active');
        }
    } else {
        alert('Solo se permiten archivos .json');
    }
});

// Cuando se pulsa en el boton de compresion
// Envia el archivo al servidor para la compresion
btnCompression.addEventListener('click', (event) => {
    event.preventDefault();

    if (file_compression && file_compression.name.endsWith('.txt')) {
        const formData = new FormData();
        formData.append('file', file_compression); 

        fetch('/compress', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (response.redirected) {
                    // Redirige automáticamente a la página de resultados
                    window.location.href = response.url;
                } else {
                    throw new Error('Error al comprimir el archivo');
                }
            })
            .catch(error => {
                alert('Error al subir el archivo: ' + error.message);
            });
    } else {
        alert('Solo se permiten archivos .txt');
    }
});

// Cuando se pulsa en el boton de compresion
// Envia el archivo al servidor para la compresion
btnDecompression.addEventListener('click', (event) => {
    event.preventDefault();

    if (
        file_decompression_bin && file_decompression_bin.name.endsWith('.bin') &&
        file_decompression_codes && file_decompression_codes.name.endsWith('.json')
    ) {
        const formData = new FormData();
        formData.append('file_bin', file_decompression_bin);
        formData.append('file_codes', file_decompression_codes);

        fetch('/decompress', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (response.ok) {
                    return response.blob();
                } else {
                    throw new Error('Error al comprimir el archivo');
                }
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');

                a.href = url;
                a.download = 'decompressed.txt';

                document.body.appendChild(a);

                a.click();

                document.body.removeChild(a);

                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                alert('Error al subir el archivo: ' + error.message);
            });
    } else {
        alert('Solo se permiten archivos .bin y .json');
    }
});

// Si un archivo es seleccionado desde el explorador de archivos, subirlo
document.getElementById('file_txt').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.txt')) {
        file_compression = file;
    } else {
        alert('Solo se permiten archivos .txt');
    }
});

document.getElementById('file_bin').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.bin')) {
        file_decompression_bin = file;
    } else {
        alert('Solo se permiten archivos .bin');
    }
});

document.getElementById('file_codes').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.json')) {
        file_decompression_codes = file;
    } else {
        alert('Solo se permiten archivos .json');
    }
});