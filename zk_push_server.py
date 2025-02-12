import falcon
import json

class ZKUserHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET para obtener la lista de usuarios del equipo ZKTeco """
        params = req.params
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        # Si se solicita obtener usuarios
        if 'action' in params and params['action'] == 'get_users':
            # Responder con datos de prueba (simulando la respuesta del equipo)
            users_data = [
                {"PIN": "982", "Name": "Richard", "Passwd": "9822", "Card": "13375590", "Grp": 1, "TZ": ""},
                {"PIN": "245", "Name": "Maria", "Passwd": "1234", "Card": "22334455", "Grp": 1, "TZ": ""}
            ]
            resp.text = json.dumps({"status": "success", "users": users_data})
        else:
            resp.text = json.dumps({"status": "error", "message": "Parámetro 'action' no válido."})

        resp.status = falcon.HTTP_200

app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())






