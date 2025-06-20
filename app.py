from flask import Flask, render_template, request, redirect, send_file, url_for, session
import os, io, json, zipfile
from Huffman.HuffmanAlgorithm import HuffmanAlgorithm, Node
from graphviz import Digraph

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

    # Archivo original
    file = request.files['file']

    if file.filename == '':
        return {'error': 'Archivo vacío'}

    if not (file and file.filename.endswith('.txt')):
        return {'error': 'Solo se permiten archivos .txt'}

    content = file.read().decode('utf-8')
    file.seek(0)

    compression = HuffmanAlgorithm(content)

    binary_file = io.BytesIO()
    binary_file.write(compression.codedContent.encode())
    binary_file.seek(0)

    # Tamaño en bytes
    file_size = len(content.encode('utf-8'))
    binary_file_size = len(binary_file.read()) / 8.0

    # Porcentaje de compresión
    percentage = (file_size / binary_file_size) * 100.0

    # Tamaños en MB
    file_size_mb = file_size / (1024 ** 2)
    binary_file_size_mb = binary_file_size / (1024 ** 2)

    # Reiniciar los punteros de los archivos
    file.seek(0)
    binary_file.seek(0)

    # Guardar los resultados en la sesión
    session['compress_summary'] = {
        'original_size': file_size,
        'original_size_mb': round(file_size_mb, 2),
        'compressed_size': round(binary_file_size, 2),
        'compressed_size_mb': round(binary_file_size_mb, 2),
        'compression_percentage': round(percentage, 2),
        'compression_method': 'Algoritmo de Huffman'
    }
 
    # Archivo con la tabla de codificación
    json_data = json.dumps(compression.codes)

    rr = compression.root
    rr.print_node()

    # Imagen del árbol de huffman
    img_tree_buffer = generate_img_huffman_tree(compression.root)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(file.filename + '_compressed.bin', file.read())
        zip_file.writestr(file.filename + '_codes.json', json_data.encode('utf-8'))
        zip_file.writestr(file.filename + '_huff_tree.svg', img_tree_buffer)

    zip_buffer.seek(0)

    # Guardar el archivo ZIP temporalmente
    temp_filename = '/tmp/compression.zip'
    with open(temp_filename, 'wb') as f:
        f.write(zip_buffer.read())

    return redirect(url_for('compress_summary', filename='compression.zip'))


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


@app.route('/compress_summary')
def compress_summary():
    """
    Muestra los detalles de la compresión.
    """
    filename = request.args.get('filename')

    details = session.get('compress_summary', {})

    return render_template('compress_summary.html', data=details, filename=filename)


@app.route('/download')
def download():
    filename = request.args.get('filename')
    filepath = f'/tmp/{filename}'

    if filename and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    else:
        return "Archivo no encontrado", 404


def traverse_tree(node: Node, graph: Digraph, parent: str = None, id = [0]):
    """
    Función recursiva para recorrer el árbol de Huffman y agregar los nodos y aristas al grafo de Graphviz.
    """
    if node is None:
        return

    # Formato para la etiqueta del nodo: mostrar tanto el carácter como la frecuencia
    label = f'{node.char} ({node.freq})' if node.char else f'{node.freq}'

    # Crear un identificador único para cada nodo, mediante un contador global
    id[0] += 1
    node_id = f"{id[0]}"

    # Agregar el nodo al grafo (si no existe)
    graph.node(node_id, label=label)

    # Si hay un nodo padre, agregamos la arista
    if parent:
        graph.edge(parent, node_id)

    # Recursivamente agregamos los nodos izquierdo y derecho
    traverse_tree(node.left, graph, node_id, id)
    traverse_tree(node.right, graph, node_id, id)


def generate_img_huffman_tree(root: Node):
    """
    Genera y retorna la imagen del árbol de Huffman como un buffer en formato SVG.
    """
    # Crear un nuevo gráfico dirigido (Digraph)
    dot = Digraph(comment='Árbol de Huffman')

    # Recorrer el árbol y construir el grafo
    traverse_tree(root, dot)

    # Renderizar el gráfico y guardarlo en un buffer
    svg_buffer = dot.pipe(format='svg')

    return svg_buffer


if __name__ == '__main__':
    app.run(debug=True)
