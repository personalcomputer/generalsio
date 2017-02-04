from socketIO_client import SocketIO, BaseNamespace



def _patch(old, diff):
    """Returns a new list created by modfying the old list using change information encoded in the
    generals.io list diff encoding.
    """
    new = []
    cursor = 0

    while cursor < len(diff):
        num_elems_matching = diff[cursor]
        if num_elems_matching != 0:
            new.extend(old[len(new):len(new)+num_elems_matching])
        cursor += 1
        if cursor >= len(diff):
            break
        num_elems_changed = diff[cursor]
        if num_elems_changed != 0:
            cursor += 1
            new.extend(diff[cursor:cursor+num_elems_changed])
        cursor += num_elems_changed
    return new


class Tile(object): # enum
    EMPTY = -1
    MOUNTAIN = -2
    UNKNOWN = -3
    UNKNOWN_OBSTACLE = -4


def Client(object):

    class SIOHandler(BaseNamespace):

        def on_connect(self):
            print('[Connected]')

        def on_reconnect(self):
            print('[Reconnected]')

        def on_disconnect(self):
            print('[Disconnected]')

    def __init__(self, server, user_id, username):
        socketIO = SocketIO('localhost', 8000, SIOHandler)
        socketIO.wait(seconds=1)
