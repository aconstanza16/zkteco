import falcon
import json

class ZKUserHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET del ZKTeco con respuesta ADMS """
        params = req.params
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        # Guardar en log
        with open("/tmp/log_zkteco.txt", "a") as log_file:
            log_file.write(f"📡 GET recibido: {params}\n")

        # Respuesta en formato ADMS
        resp.status = falcon.HTTP_200
        resp.text = "OK"

    def on_post(self, req, resp):
        """ Maneja solicitudes POST del ZKTeco """
        try:
            raw_json = req.bounded_stream.read().decode("utf-8")
            print(f"📡 POST recibido de ZKTeco con datos: {raw_json}")

            # Guardar en log
            with open("/tmp/log_zkteco.txt", "a") as log_file:
                log_file.write(f"📡 POST recibido: {raw_json}\n")

            # Respuesta en formato ADMS
            resp.status = falcon.HTTP_200
            resp.text = "OK"

        except Exception as e:
            print(f"❌ Error procesando POST: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())




