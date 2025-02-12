import falcon
import json

class ZKRequestHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET desde el equipo ZKTeco """
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            "status": "success",
            "message": "Servidor Gunicorn activo y listo para recibir datos."
        })

    def on_post(self, req, resp):
        """ Maneja solicitudes POST (cuando el equipo envía datos) """
        try:
            data = json.loads(req.stream.read().decode('utf-8'))
            print(f"📡 Datos recibidos desde el equipo ZKTeco: {data}")

            with open("zk_logs.txt", "a") as log_file:
                log_file.write(json.dumps(data) + "\n")

            resp.status = falcon.HTTP_200
            resp.body = json.dumps({
                "status": "success",
                "message": "Datos recibidos correctamente.",
                "received_data": data
            })
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"error": str(e)})

app = falcon.App()
app.add_route('/iclock/cdata', ZKRequestHandler())
