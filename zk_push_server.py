import requests

# 📡 Configuración del servidor y dispositivo
server_url = "https://zkteco-production.up.railway.app/cdata"  # Reemplaza con la URL de Railway
device_sn = "5430244500365"  # Número de serie del ZKTeco

# 🧑 Información del usuario a registrar
user_data = {
    "PIN": 2,  # ID único del usuario
    "Name": "JUAN PEREZ",
    "Pri": 0,  # Usuario normal
    "Passwd": "1234",  # Contraseña
    "Card": "98765432",  # Tarjeta RFID
    "Grp": 1,  # Grupo de acceso
    "TZ": 0,  # Configuración de zonas horarias
    "VerifyMode": -1,  # Modo de verificación
    "StartDatetime": "20250214",  # Fecha de activación del usuario (AAAAMMDD)
    "EndDatetime": "20251231"  # Fecha de expiración del usuario (AAAAMMDD)
}

# 📡 Construcción del comando en formato correcto
user_command = f"DATA UPDATE USERINFO PIN={user_data['PIN']}\tName={user_data['Name']}\tPri={user_data['Pri']}\tPasswd={user_data['Passwd']}\tCard={user_data['Card']}\tGrp={user_data['Grp']}\tTZ={user_data['TZ']}\tVerifyMode={user_data['VerifyMode']}\tStartDatetime={user_data['StartDatetime']}\tEndDatetime={user_data['EndDatetime']}"

# 🚀 Envío de la solicitud POST
params = {"SN": device_sn, "table": "OPERLOG", "Stamp": "99999999"}
response = requests.post(server_url, params=params, data=user_command)

# 📡 Mostrar respuesta del servidor
if response.status_code == 200:
    print(f"✅ Usuario enviado correctamente: {user_command}")
else:
    print(f"❌ Error al enviar usuario: {response.status_code} - {response.text}")




