import falcon
import requests

ZK_IP = "10.0.0.201"  # IP del dispositivo ZKTeco
ZK_PORT = "8080"  # Puerto del dispositivo
DEVICE_SN = "5430244500365"  # Número de serie del dispositivo

class GetUsers:
    def on_get(self, req, resp):
        """Solicita la lista de usuarios al ZKTeco y muestra errores en caso de fallo"""
        try:
            url = f"http://{ZK_IP}:{ZK_PORT}/iclock/cdata?SN={DEVICE_SN}&type=QUERY USERINFO"
            print(f"📡 Enviando solicitud al dispositivo: {url}")

            response = requests.get(url)

            if response.status_code == 200:
                print(f"📡 Respuesta del ZKTeco: {response.text}")

                if not response.text.strip():  # Si la respuesta está vacía
                    resp.status = falcon.HTTP_204
                    resp.text = "El dispositivo no devolvió usuarios."

                else:
                    with open("/tmp/zkteco_users.txt", "w") as file:
                        file.write(response.text)

                    resp.status = falcon.HTTP_200
                    resp.text = "Usuarios guardados en /tmp/zkteco_users.txt"

            else:
                print(f"❌ Error en la solicitud: {response.status_code} - {response.text}")
                resp.status = response.status_code
                resp.text = f"Error al obtener usuarios: {response.text}"

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            resp.status = falcon.HTTP_500
            resp.text = f"Error en el servidor: {e}"

# 🛠️ Agregar la ruta a Falcon
app = falcon.App()
app.add_route('/get_users', GetUsers())





