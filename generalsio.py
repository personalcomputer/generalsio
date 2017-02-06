import pprint

from socketIO_client import SocketIO, BaseNamespace


class Tile(object): # enum
    EMPTY = -1
    MOUNTAIN = -2
    UNKNOWN = -3
    UNKNOWN_OBSTACLE = -4


class GameClientListener(object):

    def handle_game_update(self, tiles, armies, cities, enemy_position, enemy_total_army,
                           enemy_total_land):
        pass

    def handle_game_start(self, map_size, start_pos, enemy_username):
        pass

    def handle_game_over(self, won, replay_url):
        pass

    def handle_chat(self, username, message):
        pass


class GameClient(object):
    """
    A small SDK for the http://generals.io bot API.
    """
    SERVER_URL = 'http://botws.generals.io'
    REPLAY_URL_TEMPLATE = 'http://bot.generals.io/replays/%s'

    def __init__(self, user_id, username):
        self._sock = SocketIO(GameClient.SERVER_URL, 80, BaseNamespace)

        self._sock.on('connect', self._on_connect)
        self._sock.on('reconnect', self._on_reconnect)
        self._sock.on('disconnect', self._on_disconnect)

        self._sock.on('game_won', self._on_game_won)
        self._sock.on('game_lost', self._on_game_lost)
        self._sock.on('game_start', self._on_game_start)
        self._sock.on('game_update', self._on_game_update)
        self._sock.on('chat_message', self._on_chat_message)

        self._sock.send("set_username", user_id, username)
        self._user_id = user_id

        self._game_ended = False
        self._in_queue = False
        self._in_game = False
        self._chat_room = None
        self._map_size = (None, None)
        self._player_index = None
        self._map = []
        self._cities = []
        self._enemy_player_index = None
        self._enemy_username = None
        self._enemy_total_army = 1
        self._enemy_total_land = 1
        self._replay_url = None

        self._halfturns = 0
        self._sent_attack_orders = 0

        self._listeners = []

    def __del__(self):
        if self._in_game:
            self._leave_game()
        else:
            self._sock.send('cancel', '1v1')
            self._in_queue = False

    def join_queue(self):
        if self._game_ended:
            raise ValueError('Game already completed. Please create a new GameClient to requeue.')
        self._sock.send("join_1v1", self._user_id)
        self._in_queue = True

    def chat(self, message):
        self._sock.send('chat_message', self._chat_room, message)

    def attack(self, start, end, half_move=False):
        start_index = start[0] + start[1] * self._map_size[1]
        end_index = end[0] + end[1] * self._map_size[1]
        self._sock.send('attack', start_index, end_index, half_move)
        self._sent_attack_orders += 1

    def clear_moves(self):
        self._sock.send('clear_moves')

    def add_listener(self, listener):
        self._listeners.append(listener)

    def _leave_game(self):
        self._sock.send('leave_game')
        self._game_ended = True
        self._in_game = False

    def _on_game_won(self, data):
        for listener in self._listeners:
            listener.handle_game_over(won=True, replay_url=self._replay_url)
        self._leave_game()

    def _on_game_lost(self, data):
        for listener in self._listeners:
            listener.handle_game_over(won=False, replay_url=self._replay_url)
        self._leave_game()

    def _on_game_start(self, data):
        self._in_queue = False
        self._in_game = True

        self._player_index = data['playerIndex']
        self._replay_url = GameClient.REPLAY_URL_TEMPLATE % data['replay_id']
        self._enemy_player_index = int(not self._player_index)
        self._enemy_username = data['usernames'][self._enemy_player_index]

        for listener in self._listeners:
            listener.handle_game_start(data)

    def _on_game_update(self, data):
        pprint.pprint(data, indent=4, width=1)
        self._halfturns += 1

        for listener in self._listeners:
            listener.handle_game_update(data)

    def _on_chat_message(self, *args):
        print('[Received chat message, %s' % args)

        #for listener in self._listeners:
        #    listener.handle_chat(username, message)

    def _on_connect(self):
        print('[Connected]')

    def _on_reconnect(self):
        print('[Reconnected]')

    def _on_disconnect(self):
        print('[Disconnected]')


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
