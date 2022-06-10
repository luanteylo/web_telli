import cherrypy
import argparse
import requests


class Status:
    IDLE = 'idle'
    CHARGING = 'charging'
    GOING_TO = 'going_to'
    ATTACHING = 'attaching'
    DETACHING = 'detaching'


class Server(object):

    def __init__(self, robots_file):
        self.my_robots = {}
        self.status = {}

        self.__load_roboInfo(robots_file)

        print(self.my_robots)

    def __load_roboInfo(self, robots_file):
        with open(robots_file) as fp:
            for line in fp.readlines():
                id_robot = line.split()[0]
                ip = line.split()[1].split(':')[0]
                port = int(line.split()[1].split(':')[1])

                self.my_robots[id_robot] = (ip, port)

    def send_task(self, id_robot, mission):
        robot_ip, robot_port = self.my_robots[id_robot]
        robot_url = 'http://{}:{}/process'.format(robot_ip, robot_port)
        data = {
            'mission': mission,
            'operation_type': self.get_operation(self.next_mission),
            'task': 1,
            'pos_x': 0.0,
            'pos_y': 0.0,
            'heading': 0.0
        }
        r = requests.post(robot_url, timeout=10.0, json=data)
        return r.json()

    def receive_status(self, data):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process(self):
        '''
        {
            id_robo: int,
            status: Status.status,
            battery: float,
            pos x: float,
            pos y: float,
            heading: float,
        }
        '''

        data = cherrypy.request.json
        response = self.receive_status(data)

        return response


def main():
    parser = argparse.ArgumentParser(description='A simple example of web service')

    parser.add_argument('--host_ip', type=str, default='0.0.0.0')
    parser.add_argument('--host_port', type=int, default=8080)
    parser.add_argument('--robots_file', type=str, default='robotsFile.txt')

    args = parser.parse_args()

    config = {'server.socket_host': args.host_ip,
              'server.socket_port': args.host_port}

    cherrypy.config.update(config)
    cherrypy.quickstart(Server(args.robots_file))


if __name__ == '__main__':
    main()
