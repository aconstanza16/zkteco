import falcon
import json
import os

# Rutas para guardar logs
LOG_FILE = "/tmp/log_zkteco.txt"
USER_FILE = "/tmp/zkteco_users.txt"

class ZKUserHandler:
    def on_post(self, req, resp):
        """ Captura todos los datos enviados por el ZKTeco y separa los datos de usuario """
        try:
            raw_data = req.bounded_stream.read().decode("utf-8")
            print(f"📡 POST recibido de ZKTeco con datos: {raw_data}")

            # Guardar todos los eventos en el log general
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"{raw_data}\n")

            # Depuración: Guardar todos los mensajes en un solo archivo sin filtrar
            with open("/tmp/debug_all_zkteco.txt", "a") as debug_file:
                debug_file.write(f"{raw_data}\n")

            # Si contiene "USER PIN=", guardarlo en un archivo separado
            if "USER PIN=" in raw_data:
                with open(USER_FILE, "a") as user_file:
                    user_file.write(f"{raw_data}\n")
                print(f"✅ Datos de usuario guardados en {USER_FILE}")

            # Responder al dispositivo
            resp.status = falcon.HTTP_200
            resp.text = "OK"

        except Exception as e:
            print(f"❌ Error procesando POST: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())






