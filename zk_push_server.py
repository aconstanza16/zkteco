import falcon
import json

class ZKRequestHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET desde el equipo ZKTeco """
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({  # ← Cambiado de resp.body a resp.text
            "status": "success",
            "message": "Servidor Gunicorn activo y listo para recibir datos."
        })

    def on_post(self, req, resp):
        """ Maneja solicitudes POST (cuando el equipo envía datos) """
        try:
            raw_data = req.stream.read().decode('utf-8')
            data = json.loads(raw_data) if raw_data else {}

            if not data:
                raise ValueError("No se enviaron datos.")

            print(f"📡 Datos recibidos desde el equipo ZKTeco: {data}")

            with open("zk_logs.txt", "a") as log_file:
                log_file.write(json.dumps(data) + "\n")

            resp.status = falcon.HTTP_200
            resp.text = json.dumps({  # ← Cambiado de resp.body a resp.text
                "status": "success",
                "message": "Datos recibidos correctamente.",
                "received_data": data
            })
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})  # ← Cambiado de resp.body a resp.text

app = falcon.App()
app.add_route('/iclock/cdata', ZKRequestHandler())

