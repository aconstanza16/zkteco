import falcon
import json
import csv
import os

USER_DATA_FILE = "/tmp/zkteco_users.csv"

class ZKUserHandler:
    def on_post(self, req, resp):
        """ Captura datos de usuarios enviados automáticamente por el ZKTeco y los almacena en un archivo CSV """
        try:
            raw_data = req.bounded_stream.read().decode("utf-8")
            print(f"📡 POST recibido de ZKTeco con datos: {raw_data}")

            # Guardar el log general
            with open("/tmp/log_zkteco.txt", "a") as log_file:
                log_file.write(f"{raw_data}\n")

            # Verificar si es un mensaje de usuario
            if raw_data.startswith("USER"):
                user_info = {}
                for field in raw_data.split("\t"):
                    key_value = field.split("=")
                    if len(key_value) == 2:
                        user_info[key_value[0].strip()] = key_value[1].strip()

                # Extraer valores específicos
                pin = user_info.get("PIN", "N/A")
                name = user_info.get("Name", "N/A")
                card = user_info.get("Card", "N/A")
                start_date = user_info.get("StartDatetime", "N/A")
                end_date = user_info.get("EndDatetime", "N/A")

                # Guardar los datos en un CSV
                file_exists = os.path.isfile(USER_DATA_FILE)
                with open(USER_DATA_FILE, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(["PIN", "Name", "Card", "Start Date", "End Date"])
                    writer.writerow([pin, name, card, start_date, end_date])

                print(f"✅ Usuario guardado en {USER_DATA_FILE}")

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





