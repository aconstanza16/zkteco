import falcon
import json

class ZKUserHandler:
    def on_get(self, req, resp):
        """ Captura todas las solicitudes GET del equipo ZKTeco y las maneja correctamente """
        params = req.params
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        # Verificar si el equipo envía un número de serie (SN)
        if 'SN' in params:
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "status": "success",
                "message": "Datos recibidos correctamente",
                "received_data": params
            })
        else:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({
                "status": "error",
                "message": "Solicitud no válida. Falta el número de serie (SN)."
            })

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())







