# Lossless DC - Compresor y Descompresor de Archivos .txt

**Lossless DC** es una aplicación web desarrollada con **Flask**, **Python 3.10+**, **HTML**, **CSS** y **JavaScript**, diseñada para **comprimir y descomprimir archivos de texto plano (.txt)**. Gracias a su compresión **sin pérdida**, puedes reducir el tamaño de tus archivos de texto sin perder ninguna información.

Además, ahora incluye **visualización de árboles de Huffman** mediante el módulo **Graphviz**, permitiendo **descargar el árbol de Huffman en formato SVG** para su visualización y análisis.

---

## Comenzando 🚀

Estas instrucciones te ayudarán a obtener una copia funcional del proyecto en tu máquina local para fines de desarrollo y pruebas. Si solo necesitas usar la aplicación, puedes instalarla directamente desde los **Releases** en GitHub.

### Pre-requisitos 📋

Necesitarás tener instalado **Python 3.10+** en tu máquina. Además, se instalarán automáticamente algunas dependencias necesarias para que la aplicación funcione correctamente.

**Dependencias principales:**

1. **Python 3.10+**
2. **Flask**
3. **Graphviz** (para visualizar el árbol de codificación)

> 💡 *Nota:* Para que Graphviz funcione correctamente, asegúrate de tener también el binario de Graphviz instalado en tu sistema si deseas generar imágenes (especialmente en entornos no virtuales).

Verifica tu versión de Python con:

```bash
python --version
```

---

## Instalación 🔧

Para instalar y ejecutar **Lossless DC** en tu máquina local, sigue estos pasos:

### 1. Clona el Repositorio (o usa Releases)

Puedes clonar el repositorio o descargar el programa directamente desde los **Releases** en GitHub.

**Clonando el repositorio:**

```bash
git clone https://github.com/Sebastian-Pompa/lossless-dc
cd lossless-dc
```

**Desde Releases:**

Si no deseas clonar el repositorio, puedes ir a la sección de *Releases* en GitHub y descargar la última versión comprimida.

### 2. Instala las Dependencias

Ejecuta el siguiente comando para instalar todas las dependencias necesarias desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

> ⚠️ Asegúrate de tener Graphviz instalado también a nivel del sistema.

### 3. Ejecuta la Aplicación

Inicia el servidor Flask ejecutando:

```bash
python app.py
```

Esto lanzará la aplicación web en `http://127.0.0.1:5000/`.

### 4. Accede a la Aplicación

Abre tu navegador y dirígete a la URL:

```
http://127.0.0.1:5000/
```

---

## Funcionalidades 🚀

Este proyecto permite la compresión y descompresión de archivos `.txt` usando técnicas sin pérdida. Además, la última versión incluye nuevas características:

* **Descarga del árbol de Huffman en formato SVG**: Ahora, al comprimir un archivo, podrás descargar el árbol de Huffman generado en formato **SVG**.
* **Compresión sin pérdida**: Utiliza el algoritmo de Huffman para reducir el tamaño del archivo de texto sin perder ningún dato.
* **Descompresión eficiente**: Recupera el archivo original sin pérdidas tras aplicar la compresión.

---

## Sobre el Proyecto 🎓

Este proyecto fue desarrollado como parte de la asignatura **Matemática Computacional** en la **Universidad Peruana de Ciencias Aplicadas (UPC)**. Se trata de una solución para comprimir y descomprimir archivos `.txt` utilizando técnicas de compresión **sin pérdida**, realizado durante el **tercer ciclo de la carrera de Ingeniería de Software, año 2025**.

Ahora con soporte de **Graphviz**, también puedes visualizar el **árbol de Huffman** utilizado en el proceso de compresión, y descargarlo en formato **SVG** para su análisis.

---

## Expresiones de Gratitud 🎁

¡Gracias por usar Lossless DC! Aquí algunas maneras en las que puedes expresar tu gratitud:

* Deja una estrella ⭐ en el repositorio de GitHub si te ha gustado el proyecto.
* Sigue el proyecto y compártelo con quienes estén interesados en compresión sin pérdida.