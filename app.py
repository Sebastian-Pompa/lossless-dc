from flask import Flask, render_template, request, redirect, send_file, url_for, session
import os, io, json, zipfile
from Huffman.HuffmanAlgorithm import HuffmanAlgorithm

app = Flask(__name__)
app.secret_key = 'hdewe6649nfnvi66537#mk3728!@m!@*^$o'


# Página principal
@app.route('/')
def index():
    return render_template('index.html')


# Comprimir
@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return {'error': "No hay archivo"}

    file = request.files['file']

    if file.filename == '':
        return {'error': 'Archivo vacío'}

    if not (file and file.filename.endswith('.txt')):
        return {'error': 'Solo se permiten archivos .txt'}

    content = file.read().decode('utf-8')

    compression = HuffmanAlgorithm(content)

    session['compress_details'] = {
        'original_size': len(content),
        'compressed_size': len(compression.codedContent),
        'compression_percentage': round(100 * (1 - len(compression.codedContent) / len(content)), 2) if len(content) > 0 else 0,
        'compression_ratio': round(len(content) / len(compression.codedContent), 2) if len(compression.codedContent) > 0 else 0,
        'compression_time': 0.1,  # ejemplo
        'num_characters': len(content),
        'num_words': len(content.split()),
        'compression_method': 'Huffman',
        'compression_status': 'Completado',
        'generated_files': '.json y .bin'
    }

    binary_file = io.BytesIO()
    binary_file.write(compression.codedContent.encode())
    binary_file.seek(0)

    json_data = json.dumps(compression.codes)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(file.filename + '_compressed.bin', binary_file.read())
        zip_file.writestr(file.filename + '_codes.json', json_data.encode('utf-8'))
    zip_buffer.seek(0)

    # Guardar ZIP temporalmente
    temp_filename = '/tmp/compression.zip'
    with open(temp_filename, 'wb') as f:
        f.write(zip_buffer.read())

    # Guardamos detalles como parámetros temporales en URL (alternativa a session para datos no sensibles)
    return redirect(url_for('compress_details', filename='compression.zip'))


# Descomprimir
@app.route('/decompress', methods=['POST'])
def decompress():
    bin_name = "file_bin"
    codes_name = "file_codes"

    if not (bin_name in request.files and codes_name in request.files):
        return {'error': "No hay archivos"}

    file_bin = request.files[bin_name]
    file_codes = request.files[codes_name]

    if file_bin.filename == '' or file_codes.filename == '':
        return {'error': 'Archivos vacíos'}

    if not (file_bin.filename.endswith('.bin') and file_codes.filename.endswith('.json')):
        return {'error': 'Solo se permiten archivos .bin y .json'}

    try:
        content_bin = file_bin.read().decode('utf-8')
        content_codes = json.loads(file_codes.read().decode('utf-8'))
        content_decompressed = HuffmanAlgorithm.decode(content_bin, content_codes)
    except Exception as e:
        return {'error': f'Error al descomprimir: {str(e)}'}

    decompressed_file = io.BytesIO(content_decompressed.encode('utf-8'))

    return send_file(
        decompressed_file,
        as_attachment=True,
        download_name="decompressed_file.txt",
        mimetype="text/plain"
    )


# Mostrar detalles de compresión
@app.route('/compress_details')
def compress_details():
    filename = request.args.get('filename')

    details = session.get('compress_details', {})

    return render_template('compress_details.html', data=details, filename=filename)


# Ruta para descargar ZIP
@app.route('/download')
def download():
    filename = request.args.get('filename')
    filepath = f'/tmp/{filename}'

    if filename and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    else:
        return "Archivo no encontrado", 404


if __name__ == '__main__':
    app.run(debug=True)
