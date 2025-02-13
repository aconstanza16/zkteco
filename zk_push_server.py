import falcon
import json

class ZKUserHandler:
    def on_post(self, req, resp):
        """ Captura solicitudes POST del ZKTeco y almacena los registros """
        try:
            raw_data = req.bounded_stream.read().decode("utf-8")
            print(f"📡 POST recibido de ZKTeco con datos: {raw_data}")

            # Guardar en un archivo de logs separado
            with open("/tmp/zkteco_data.txt", "a") as log_file:
                log_file.write(f"{raw_data}\n")

            # Responder al ZKTeco con "OK"
            resp.status = falcon.HTTP_200
            resp.text = "OK"

        except Exception as e:
            print(f"❌ Error procesando POST: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())





