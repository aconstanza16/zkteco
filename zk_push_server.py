import falcon
import json

class ZKUserHandler:
    def on_get(self, req, resp):
        """ Captura y muestra todas las solicitudes GET que llegan desde el ZKTeco """
        params = req.params
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        # Guardar los datos en un archivo de log en Railway (para verlos después)
        with open("/tmp/log_zkteco.txt", "a") as log_file:
            log_file.write(f"📡 Datos recibidos: {params}\n")

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "status": "success",
            "message": "Datos recibidos correctamente",
            "received_data": params
        })

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())





