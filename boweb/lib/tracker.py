import socket
import json


class Connection(object):

    socket_file = '/tmp/.blitzortung-tracker'

    def __init__(self, command, socket_file=socket_file):

        try:
            tracker_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            tracker_socket.connect(socket_file)
            tracker_socket.send(json.dumps({'cmd': command}))
            response = tracker_socket.recv(10240)
            self.json_object = json.loads(str(response))
            tracker_socket.close()
        except socket.error:
            pass

    def is_empty(self):
        return self.json_object is None

    def has_element(self, path):
        json_object = self.json_object

        if json_object is not None:
            for component in path.split('/'):
                if component in json_object:
                    json_object = json_object[component]
                else:
                    return False
        return True

    def get_result(self, path=None):
        json_object = self.json_object

        if json_object is not None:
            if path:
                for component in path.split('/'):
                    if component in json_object:
                        json_object = json_object[component]
                    else:
                        json_object = None
                        break
        return json_object


class Activity(Connection):
    def __init__(self, socket_file=Connection.socket_file):
        Connection.__init__(self, 'getActivity', socket_file)

    def get(self):
        if self.json_object:
            if 'activity' in self.json_object:
                return self.json_object['activity']
        return []


class Info(Connection):
    def __init__(self, socket_file=Connection.socket_file):
        Connection.__init__(self, 'getInfo', socket_file)
