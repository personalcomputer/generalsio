from socketIO_client import SocketIO, BaseNamespace



# Returns a new array created by patching the diff into the old array.
# The diff formatted with alternating matching and mismatching segments:
# <Number of matching elements>
# <Number of mismatching elements>
# <The mismatching elements>
# ... repeated until the end of diff.
# Example 1: patching a diff of [1, 1, 3] onto [0, 0] yields [0, 3].
# Example 2: patching a diff of [0, 1, 2, 1] onto [0, 0] yields [2, 0].
#
def patch(old, diff):
    

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
