import cherrypy
import argparse


def foo(value):
    print(f"foo: {value}")
    return 'foo'


def do_operation(action, value):
    if len(value) != 2:
        return "Error: To use that action you need to sent a list with two numbers"

    if action == 'sum':
        response = value[0] + value[1]
    else:
        response = value[0] / value[1]

    return response


def do_something(action, value):
    response = None

    if action == 'echo':
        response = value
    elif action == 'sum' or action == 'div':
        response = do_operation(action, value)
    elif action == 'foo':
        response = foo(value)
    else:
        response = "action not supported."

    return response


class MyWebService(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process(self):
        data = cherrypy.request.json
        response = do_something(data['action'], data['value'])

        return response


def main():
    parser = argparse.ArgumentParser(description='A simple web server.')

    parser.add_argument('--host_ip', type=str, default='0.0.0.0')
    parser.add_argument('--host_port', type=int, default=8080)

    args = parser.parse_args()

    config = {'server.socket_host': args.host_ip,
              'server.socket_port': args.host_port}

    cherrypy.config.update(config)
    cherrypy.quickstart(MyWebService())


if __name__ == '__main__':
    main()
