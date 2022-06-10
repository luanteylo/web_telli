import requests
import argparse
import cherrypy


class Robot:

    def __init__(self, server):
        self.server_ip = server.split(":")[0]
        self.server_port = int(server.split(":")[1])
        self.url = 'http://{}:{}/process'.format(self.server_ip, self.server_port)

        self.id = 1
        self.status = 'running'
        self.battery = 10
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0

    def send_msg(self):
        data = {
            'id_robo': self.id,
            'status': self.status,
            'battery': self.battery,
            'pos_x': self.x,
            'pos_y': self.y,
            'heading': self.heading,
        }

        r = requests.post(self.url, timeout=10.0, json=data)
        return r.json()

    def handle_msg(self, data):
        pass
        # mandar execução

    def check_tasks(self):
        while True:
            # verificar topico da tarefa
            # se tarefa terminou
            # inicia comunicaçao com servidor
            self.send_msg(self)
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def handle(self):
        '''
        {
            mission: int,
            operation_type: string,
            task: int
            pos x: float,
            pos y: float,
            heading: float,
        }
        '''

        data = cherrypy.request.json

        response = self.handle_msg(data)

        return response


def main():
    parser = argparse.ArgumentParser(description='A simple example of web service')

    # Robot's ip and port
    parser.add_argument('--host_ip', type=str, default='0.0.0.0')
    parser.add_argument('--host_port', required=True)

    # Server's IP and port
    parser.add_argument('--server', type=str, default='0.0.0.0:8080')

    args = parser.parse_args()

    config = {'server.socket_host': args.host_ip,
              'server.socket_port': args.host_port}

    cherrypy.config.update(config)
    cherrypy.quickstart(Robot(args.server))
