import falcon
import json
import requests

ZK_IP = "10.0.0.201"  # Cambia esto por la IP del dispositivo ZKTeco
ZK_PORT = "8080"  # Puerto del dispositivo
DEVICE_SN = "5430244500365"  # Número de serie del dispositivo

class GetUsers:
    def on_get(self, req, resp):
        """Solicita la lista de usuarios al ZKTeco"""
        try:
            url = f"http://{ZK_IP}:{ZK_PORT}/iclock/devicecmd?SN={DEVICE_SN}"
            payload = "QUERY USERINFO"

            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            print(f"📡 Enviando solicitud al dispositivo: {url} con payload: {payload}")

            response = requests.post(url, data={"CMD": payload}, headers=headers)

            if response.status_code == 200:
                print(f"📡 Respuesta del ZKTeco: {response.text}")

                # Guardar la respuesta en un archivo
                with open("/tmp/zkteco_users.txt", "w") as file:
                    file.write(response.text)

                resp.status = falcon.HTTP_200
                resp.text = json.dumps({
                    "status": "success",
                    "message": "Usuarios almacenados correctamente",
                    "file": "/tmp/zkteco_users.txt"
                })

            else:
                print(f"❌ Error en la solicitud: {response.status_code} - {response.text}")
                resp.status = response.status_code
                resp.text = json.dumps({
                    "status": "error",
                    "message": f"Error al obtener usuarios: {response.text}"
                })

        except Exception as e:
            print(f"❌ Error al obtener usuarios: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/get_users', GetUsers())






