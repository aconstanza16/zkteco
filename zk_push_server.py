import requests

ZK_IP = "10.0.0.201"
ZK_PORT = "8080"
DEVICE_SN = "5430244500365"

def send_user(pin, name, passwd, card):
    url = f"http://{ZK_IP}:{ZK_PORT}/iclock/devicecmd?SN={DEVICE_SN}"
    payload = f"SET USERINFO PIN={pin} Name={name.replace(' ', '_')} Passwd={passwd} Card={card} Grp=1 TZ="
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print(f"📡 Enviando usuario al ZKTeco: {payload}")
    
    response = requests.post(url, data={"CMD": payload}, headers=headers)

    if response.status_code == 200:
        print(f"✅ Usuario agregado correctamente: {response.text}")
        # Responder OK para forzar la inserción
        requests.post(f"http://{ZK_IP}:{ZK_PORT}/iclock/cdata", data="OK")
    else:
        print(f"❌ Error al agregar usuario: {response.status_code} - {response.text}")

# Prueba enviando un usuario
send_user("1001", "Juan Perez", "1234", "987654")






