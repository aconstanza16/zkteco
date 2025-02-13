import falcon
import json
import requests

ZK_IP = "10.0.0.201"  # IP del dispositivo ZKTeco
ZK_PORT = "8080"  # Puerto del dispositivo
DEVICE_SN = "5430244500365"  # Número de serie del dispositivo

class AddUser:
    def on_post(self, req, resp):
        """ Agrega un usuario al ZKTeco """
        try:
            user_data = json.load(req.bounded_stream)

            if "PIN" not in user_data or "Name" not in user_data:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"status": "error", "message": "Faltan datos obligatorios (PIN y Name)"})
                return

            # Construir la solicitud con los datos del usuario
            payload = f"DATA UPDATE USERINFO PIN={user_data['PIN']}\tName={user_data['Name']}"
            if "Passwd" in user_data:
                payload += f"\tPasswd={user_data['Passwd']}"
            if "Card" in user_data:
                payload += f"\tCard={user_data['Card']}"
            if "Grp" in user_data:
                payload += f"\tGrp={user_data['Grp']}"
            if "TZ" in user_data:
                payload += f"\tTZ={user_data['TZ']}"

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

# 📌 Enviar usuarios de prueba automáticamente al iniciar el servidor
def send_test_users():
    users = [
        {"PIN": "1001", "Name": "Juan Perez", "Passwd": "1234", "Card": "987654", "Grp": "1", "TZ": ""},
        {"PIN": "1002", "Name": "Maria Garcia", "Passwd": "5678", "Card": "555444", "Grp": "1", "TZ": ""},
        {"PIN": "1003", "Name": "Carlos Diaz", "Passwd": "0000", "Card": "111222", "Grp": "1", "TZ": ""}
    ]
    
    for user in users:
        url = f"http://{ZK_IP}:{ZK_PORT}/iclock/devicecmd?SN={DEVICE_SN}"
        payload = f"DATA UPDATE USERINFO PIN={user['PIN']}\tName={user['Name']}\tPasswd={user['Passwd']}\tCard={user['Card']}\tGrp={user['Grp']}\tTZ={user['TZ']}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        print(f"📡 Enviando usuario de prueba al ZKTeco: {payload}")
        response = requests.post(url, data={"CMD": payload}, headers=headers)

        if response.status_code == 200:
            print(f"✅ Usuario agregado: {user['Name']}")
        else:
            print(f"❌ Error al agregar usuario {user['Name']}: {response.text}")

# Ejecutar la función de prueba cuando se inicie el servidor
send_test_users()





