import falcon
import json

class ZKUserHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET del ZKTeco """
        params = req.params
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        # Guardar en log para verificar qué está enviando el ZKTeco
        with open("/tmp/log_zkteco.txt", "a") as log_file:
            log_file.write(f"📡 GET recibido: {params}\n")

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "status": "success",
            "message": "GET recibido",
            "received_data": params
        })

    def on_post(self, req, resp):
        """ Maneja solicitudes POST del ZKTeco """
        try:
            raw_json = req.bounded_stream.read().decode("utf-8")
            print(f"📡 POST recibido de ZKTeco con datos: {raw_json}")

            # Guardar en log
            with open("/tmp/log_zkteco.txt", "a") as log_file:
                log_file.write(f"📡 POST recibido: {raw_json}\n")

            # Responder en formato ADMS si el ZKTeco está esperando algo específico
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "status": "success",
                "message": "POST recibido correctamente",
                "received_data": raw_json
            })

        except Exception as e:
            print(f"❌ Error procesando POST: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())




