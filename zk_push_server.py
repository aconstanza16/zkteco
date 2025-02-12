import falcon
import json

class ZKUserHandler:
    def on_post(self, req, resp):
        """ Captura solicitudes POST del ZKTeco (ADMS) y responde como un servidor real """
        params = req.params
        print(f"📡 POST recibido de ZKTeco con parámetros: {params}")

        # Guardar en log para verificar qué está enviando el ZKTeco
        with open("/tmp/log_zkteco.txt", "a") as log_file:
            log_file.write(f"📡 POST recibido: {params}\n")

        # Respuesta en formato ADMS (simulación)
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "status": "success",
            "message": "Servidor ADMS simulado. Datos recibidos.",
            "received_data": params
        })

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())







