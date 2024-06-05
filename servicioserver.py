
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import os
import webbrowser
from time import sleep

# Crear la instancia de la aplicación Flask
app = Flask(__name__, static_folder='front')
CORS(app)

# Variable global para almacenar los datos recibidos del formulario
datos_recibidos = {}

@app.route('/submit', methods=['POST'])
def handle_form():
    """
    Recibe datos de un formulario y los almacena en una variable global.
    """
    global datos_recibidos
    if request.is_json:
        datos_recibidos = request.get_json()
        return jsonify({"status": "success", "message": "Datos recibidos correctamente"}), 200
    return jsonify({"status": "error", "message": "Esperado contenido JSON"}), 400

@app.route('/verificar', methods=['GET'])
def verify_data():
    """
    Devuelve los datos almacenados para verificación.
    """
    global datos_recibidos
    if datos_recibidos:
        return jsonify(datos_recibidos), 200
    return jsonify({"status": "error", "message": "No hay datos almacenados"}), 404

@app.route('/inicio.html')
def serve_inicio():
    """
    Sirve la página de inicio desde el directorio específico.
    """
    return send_from_directory(app.static_folder, 'inicio.html')

@app.route('/usuario.html')
def serve_usuario():
    """
    Sirve la página de configuración del usuario.
    """
    return send_from_directory(app.static_folder, 'usuario.html')

@app.route('/imagenes/<filename>')
def serve_image(filename):
    """
    Sirve imágenes desde el subdirectorio 'imagenes' dentro del directorio 'front'.
    """
    return send_from_directory(os.path.join(app.static_folder, 'imagenes'), filename)

# Función para abrir automáticamente la página en un navegador al iniciar la aplicación
def open_browser():
    sleep(1)
    webbrowser.open_new("http://127.0.0.1:5000/inicio.html")
# Corre el streamlit en segundo plano
def run_streamlit():
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.system("streamlit run app.py")

if __name__ == '__main__':
    # Iniciar un hilo para abrir el navegador automáticamente
    threading.Thread(target=open_browser).start()
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.start()

    # Iniciar la aplicación Flask
    app.run(debug=False, port=5000)
