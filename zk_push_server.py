import falcon
import json

class ZKUserHandler:
    def on_post(self, req, resp):
        """ Maneja solicitudes POST del ZKTeco y guarda datos de usuarios si los envía """
        try:
            raw_data = req.bounded_stream.read().decode("utf-8")
            print(f"📡 POST recibido de ZKTeco con datos: {raw_data}")

            # Guardar todos los eventos en log general
            with open("/tmp/log_zkteco.txt", "a") as log_file:
                log_file.write(f"📡 POST recibido: {raw_data}\n")

            # Detectar si el mensaje contiene datos de usuario y guardarlos aparte
            if "USER" in raw_data or "PIN=" in raw_data:
                with open("/tmp/zkteco_users.txt", "a") as user_file:
                    user_file.write(f"{raw_data}\n")
                print("✅ Datos de usuarios guardados en /tmp/zkteco_users.txt")

            # Respuesta al dispositivo
            resp.status = falcon.HTTP_200
            resp.text = "OK"

        except Exception as e:
            print(f"❌ Error procesando POST: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())





