import falcon
import json
import requests

ZK_IP = "10.0.0.201"  # IP del dispositivo ZKTeco
ZK_PORT = "8080"  # Puerto del dispositivo
DEVICE_SN = "5430244500365"  # Número de serie del dispositivo

class AddUser:
    def on_post(self, req, resp):
        """ Agrega un usuario al ZKTeco usando HTTPS """
        try:
            user_data = json.load(req.bounded_stream)

            # Verificar que los datos mínimos están presentes
            if "id" not in user_data or "nombre" not in user_data:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"status": "error", "message": "Faltan datos obligatorios (id y nombre)"})
                return

            # Construir la solicitud con los datos del usuario
            payload = f"DATA UPDATE USERINFO PIN={user_data['id']}\tName={user_data['nombre']}"

            if "contraseña" in user_data:
                payload += f"\tPasswd={user_data['contraseña']}"
            if "numero_de_tarjeta" in user_data:
                payload += f"\tCard={user_data['numero_de_tarjeta']}"
            if "fecha_expiracion" in user_data:
                payload += f"\tExpireDate={user_data['fecha_expiracion']}"

            url = f"http://{ZK_IP}:{ZK_PORT}/iclock/devicecmd?SN={DEVICE_SN}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            print(f"📡 Enviando usuario al ZKTeco: {payload}")
            response = requests.post(url, data={"CMD": payload}, headers=headers)

            if response.status_code == 200:
                print(f"✅ Usuario agregado correctamente: {response.text}")
                resp.status = falcon.HTTP_200
                resp.text = json.dumps({
                    "status": "success",
                    "message": "Usuario agregado correctamente",
                    "response": response.text
                })
            else:
                print(f"❌ Error en la solicitud: {response.status_code} - {response.text}")
                resp.status = response.status_code
                resp.text = json.dumps({
                    "status": "error",
                    "message": f"Error al agregar usuario: {response.text}"
                })

        except Exception as e:
            print(f"❌ Error al agregar usuario: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/add_user', AddUser())





