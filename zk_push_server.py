import falcon
import json

class ZKUserHandler:
    def on_get(self, req, resp):
        """ Captura todas las solicitudes GET y responde con datos de prueba """
        params = req.params
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        # Guardar en log
        with open("/tmp/log_zkteco.txt", "a") as log_file:
            log_file.write(f"📡 Datos recibidos: {params}\n")

        # Responder con datos de prueba si el equipo espera algo específico
        fake_users = [
            {"id": "1", "name": "Usuario1", "role": "admin"},
            {"id": "2", "name": "Usuario2", "role": "user"}
        ]

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "status": "success",
            "message": "Datos de prueba enviados",
            "users": fake_users
        })

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())






