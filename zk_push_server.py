import falcon
import json
import requests  # Necesario para comunicarse con el dispositivo

# Configuración del equipo ZKTeco
ZKTECO_IP = "10.0.0.201"  # 🔹 Reemplaza con la IP del equipo en tu red
ZKTECO_PORT = 4370        # 🔹 Puerto de comunicación del dispositivo

class ZKRequestHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET desde el equipo ZKTeco """
        try:
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "status": "success",
                "message": "Servidor en Railway activo y listo para enviar datos al dispositivo."
            })
        except Exception as e:
            print(f"❌ Error en GET: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"error": "Fallo en GET, pero el servidor sigue activo."})

    def on_post(self, req, resp):
        """ Maneja solicitudes POST para recibir datos y enviarlos al ZKTeco """
        try:
            raw_data = req.stream.read().decode('utf-8')
            data = json.loads(raw_data) if raw_data else {}

            if not data:
                raise ValueError("No se enviaron datos.")

            print(f"📡 Datos recibidos en Railway para enviar a ZKTeco: {data}")

            # 🔹 Intentar enviar los datos al dispositivo
            envio_exitoso = self.enviar_usuario_a_zkteco(data)

            if envio_exitoso:
                resp.status = falcon.HTTP_200
                resp.text = json.dumps({
                    "status": "success",
                    "message": "Usuario enviado correctamente al dispositivo.",
                    "sent_data": data
                })
            else:
                resp.status = falcon.HTTP_500
                resp.text = json.dumps({
                    "status": "error",
                    "message": "No se pudo enviar el usuario al dispositivo."
                })

        except Exception as e:
            print(f"❌ Error en POST: {e}")
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})

    def enviar_usuario_a_zkteco(self, data):
        """
        Función para enviar usuarios al dispositivo ZKTeco desde Railway.
        """
        try:
            # 🔹 Ajusta la URL para que coincida con la API del equipo (si tiene una)
            url = f"http://zkteco-production.up.railway.app:8080/iclock/cdata"

            # 🔹 Datos que enviamos al equipo
            payload = {
                "PIN": data.get("PIN"),    # ID del usuario
                "Name": data.get("Name"),  # Nombre del usuario
                "Card": data.get("Card", ""),  # Tarjeta (opcional)
                "Priv": data.get("Priv", 0),   # Nivel de privilegio (0 = usuario normal)
                "Passwd": data.get("Passwd", "")  # Contraseña (opcional)
            }

            # 🔹 Enviar datos al equipo desde Railway
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                print(f"✅ Usuario {data.get('Name')} enviado correctamente al ZKTeco.")
                return True
            else:
                print(f"❌ Error al enviar usuario: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ No se pudo comunicar con ZKTeco: {e}")
            return False

app = falcon.App()
app.add_route('/iclock/cdata', ZKRequestHandler())

