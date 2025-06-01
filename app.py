from flask import Flask, render_template, request, send_from_directory, send_file
import os, io, json, zipfile
from Huffman.HuffmanAlgorithm import HuffmanAlgorithm

app = Flask(__name__)

# Directorio donde se guardarán los archivos subidos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Comprimir
@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return { 'error' : "No hay archivo" }
    
    file = request.files['file']
    
    if file.filename == '':
        return { 'error' : 'Archivo vacio' }
    
    if not (file and file.filename.endswith('.txt')):
        return { 'error': 'Solo se permiten archivos .txt' }
    
    content: str = file.read().decode('utf-8')

    compression = HuffmanAlgorithm(content)

    binary_file = io.BytesIO()

    binary_file.write(compression.codedContent.encode())
    binary_file.seek(0)

    json_data = json.dumps(compression.codes)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(file.filename + '_compressed.bin', binary_file.read())  # Agregar el archivo binario
        zip_file.writestr(file.filename + '_codes.json', json_data.encode('utf-8'))  # Agregar el archivo JSON
    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="compression.zip",
        mimetype="application/zip"
    )

# Descomprimir
@app.route('/decompress', methods=['POST'])
def decompress():
    bin_name = "file_bin"
    codes_name = "file_codes"

    if not (bin_name in request.files and codes_name in request.files):
        return { 'error' : "No hay archivos" }
    
    file_bin = request.files[bin_name]
    file_codes = request.files[codes_name]
    
    if file_bin.filename == '' and file_codes.filename == '':
        return { 'error' : 'Archivos vacios' }
    
    if not (file_bin and file_bin.filename.endswith('.bin') and file_codes and file_codes.filename.endswith('.json')):
        return { 'error': 'Solo se permiten archivos .bin y .json' }
    
    content_bin: str = file_bin.read().decode('utf-8')
    content_codes: str = file_codes.read().decode('utf-8')
    
    try:
        content_decompressed: str = HuffmanAlgorithm.decode(content_bin, json.loads(content_codes))
    except:
        return { 'error' : 'Eror en conversion del archivo de codificacion (.json)' }
    
    decompressed_file = io.BytesIO(content_decompressed.encode('utf-8'))

    return send_file(
        decompressed_file,
        as_attachment=True,
        download_name="decompressed_file.txt",
        mimetype="text/plain"
    )

if __name__ == '__main__':
    app.run(debug=True)