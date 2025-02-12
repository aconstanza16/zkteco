import falcon
import json
import requests

# Configuración del equipo ZKTeco
ZKTECO_IP = "10.0.0.201"  
ZKTECO_PORT = 8080       

class ZKRequestHandler:
    def on_get(self, req, resp):
        """ Captura datos de los GET enviados por el ZKTeco """
        try:
            # Capturar los parámetros enviados en la URL (si existen)
            params = req.params  

            print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

            # Guardar en un log local para ver si el dispositivo realmente envía datos
            with open("zk_logs.txt", "a") as log_file:
                log_file.write(f"GET DATA: {json.dumps(params)}\n")

            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "status": "success",
                "message": "Servidor en Railway activo y listo.",
                "received_params": params  # Muestra los parámetros recibidos
            })
        except Exception as e:
            print(f"❌ Error en GET: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"error": str(e)})

app = falcon.App()
app.add_route('/iclock/cdata', ZKRequestHandler())


