import falcon
import json
import requests

# 📡 Clase para manejar las solicitudes GET y POST de ZKTeco
class ZKRequestHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET desde el equipo ZKTeco """
        params = req.params  # Captura los parámetros enviados en GET
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        # Respuesta exitosa
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "status": "success",
            "message": "GET recibido correctamente.",
            "received_params": params
        })

    def on_post(self, req, resp):
        """ Maneja solicitudes POST desde el equipo ZKTeco (Envío de registros de asistencia, usuarios, etc.) """
        try:
            raw_data = req.stream.read().decode('utf-8')
            data = json.loads(raw_data) if raw_data else {}

            if not data:
                raise ValueError("No se enviaron datos en el POST.")

            print(f"📡 POST recibido de ZKTeco con datos: {data}")

            # Guardar datos en un archivo de logs
            with open("zk_logs.txt", "a") as log_file:
                log_file.write(json.dumps(data) + "\n")

            # Responder éxito al dispositivo
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "status": "success",
                "message": "Datos POST recibidos correctamente.",
                "received_data": data
            })

        except Exception as e:
            print(f"❌ Error en POST: {e}")
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKRequestHandler())



