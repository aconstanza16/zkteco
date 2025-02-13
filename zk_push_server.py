import requests

ZK_IP = "10.0.0.201"  # IP del dispositivo ZKTeco
ZK_PORT = "8080"  # Puerto del dispositivo
DEVICE_SN = "5430244500365"  # Número de serie del dispositivo

def send_user(pin, name, passwd, card):
    url = f"http://{ZK_IP}:{ZK_PORT}/iclock/devicecmd?SN={DEVICE_SN}"
    payload = f"SET USERINFO PIN={pin}\tName={name}\tPasswd={passwd}\tCard={card}\tGrp=1\tTZ="
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print(f"📡 Enviando usuario al ZKTeco: {payload}")
    
    response = requests.post(url, data={"CMD": payload}, headers=headers)

    if response.status_code == 200:
        print(f"✅ Usuario agregado correctamente: {response.text}")
    else:
        print(f"❌ Error al agregar usuario: {response.status_code} - {response.text}")

# Prueba enviando un usuario
send_user("1001", "Juan Perez", "1234", "987654")






