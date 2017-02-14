from unittest import TestCase, skip

from generalsio import GameClient, GameClientListener, _patch


class PatchTestCase(TestCase):
    def test_example1(self):
        # Example 1: patching a diff of [1, 1, 3] onto [0, 0] yields [0, 3].
        old = [0, 0]
        new = [0, 3]
        diff = [1, 1, 3]
        self.assertEquals(_patch(old, diff), new)

    def test_example2(self):
        # Example 2: patching a diff of [0, 1, 2, 1] onto [0, 0] yields [2, 0].
        old = [0, 0]
        new = [2, 0]
        diff = [0, 1, 2, 1]
        self.assertEquals(_patch(old, diff), new)

    def test_grow(self):
        old = []
        new = [5, 5, 5, 5, 5, 5, 5, 5]
        diff = [0, 8, 5, 5, 5, 5, 5, 5, 5, 5]
        self.assertEquals(_patch(old, diff), new)

    def test_start_change(self):
        old = [0, 0, 0, 0, 0, 0, 0, 0]
        new = [9, 9, 9, 0, 0, 0, 0, 0]
        diff = [0, 3, 9, 9, 9, 5]
        self.assertEquals(_patch(old, diff), new)

    def test_ending_change(self):
        old = [0, 0, 0, 0, 0, 0, 0, 0]
        new = [0, 0, 0, 0, 0, 0, 0, 1]
        diff = [7, 1, 1]
        self.assertEquals(_patch(old, diff), new)

    def test_two_changes(self):
        old = [0, 0, 0, 0, 0, 0, 0, 0]
        new = [0, 2, 5, 0, 0, 0, 3, 0]
        diff = [1, 2, 2, 5, 3, 1, 3, 1]
        self.assertEquals(_patch(old, diff), new)

    def test_replace(self):
        old = [8, 8, 8, 8, 8, 8, 8, 8]
        new = [3, 3, 3, 3, 3, 3, 3, 3]
        diff = [0, 8, 3, 3, 3, 3, 3, 3, 3, 3]
        self.assertEquals(_patch(old, diff), new)

    def test_same(self):
        old = [8, 8, 8, 8, 8, 8, 8, 8]
        new = [8, 8, 8, 8, 8, 8, 8, 8]
        diff = [8, 0]
        self.assertEquals(_patch(old, diff), new)

    def test_same_half_pair(self):
        old = [8, 8, 8, 8, 8, 8, 8, 8]
        new = [8, 8, 8, 8, 8, 8, 8, 8]
        diff = [8]
        self.assertEquals(_patch(old, diff), new)


@skip('slow, and effectively spams generals.io API')
class NetworkedClientTestCase(TestCase):
    CUSTOM_GAME_NAME = '4u3k'
    USER_ID = 'personalcomputer/generalsio/test'
    USERNAME = 'unittest'

    class ListenerImpl(GameClientListener):
        def __init__(self):
            self.game_started = False
            self.start_pos = None
            self.game_ended = False
            self.replay_url = None
            self.last_chat_message = None

        def handle_game_start(self, map_size, start_pos, enemy_username):
            self.game_started = True
            self.start_pos = start_pos

        def handle_game_over(self, won, replay_url):
            self.game_ended = True
            self.replay_url = replay_url

        def handle_chat(self, username, message):
            self.last_chat_message = message

    def _set_up_clients(self):
        self.client1 = GameClient(NetworkedClientTestCase.USER_ID, NetworkedClientTestCase.USERNAME)
        self.listener_imp1 = NetworkedClientTestCase.ListenerImpl()
        self.client1.add_listener(self.listener_imp1)

        self.client2 = GameClient(NetworkedClientTestCase.USER_ID+'2',
                                  NetworkedClientTestCase.USERNAME+'2')
        self.listener_imp2 = NetworkedClientTestCase.ListenerImpl()
        self.client2.add_listener(self.listener_imp2)

    def test_flow(self):
        self._set_up_clients()

        # Join Game
        self.client1.join_custom(NetworkedClientTestCase.CUSTOM_GAME_NAME)
        self.client2.join_custom(NetworkedClientTestCase.CUSTOM_GAME_NAME)
        self.client1.wait(seconds=3)
        self.client2.wait(seconds=3)

        self.assertTrue(self.listener_imp1.game_started)
        self.assertEquals(type(self.listener_imp1.start_pos), tuple)

        # Client 2 -> 1 Chat
        self.client2.chat('testing')
        self.client1.wait(seconds=2)
        self.assertEquals(self.listener_imp1.last_chat_message, 'testing')

        # Client 2 Leave Game
        del self.client2
        self.client2.wait(seconds=2)
        self.client1.wait(seconds=2)
        self.assertTrue(self.listener_imp1.game_ended)
        self.assertRegexpMatches(self.listener_imp1.replay_url, 
                                 'https?://bot\.generals\.io/replays/[a-zA-Z0-9]{2,10}')
