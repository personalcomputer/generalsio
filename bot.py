import random
import sys

import commentjson
import numpy as np

from generalsio import Tile, GameClient, GameClientListener


CONFIG_FILENAME = 'config.json'


class WorldUnderstanding(object):
    def __init__(self):
        self.map_size = (None, None)
        self.enemy_pos = None
        self.player_pos = None

        self.cities = None
        self.mountains = set()

        self.last_seen_scores = None
        self.expected_scores = None

    def update(self, tiles, armies, cities, enemy_position, enemy_total_army, enemy_total_land):
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                    if tiles[x][y] == Tile.MOUNTAIN:
                        self.mountains.add((x, y))


class Bot(GameClientListener):
    def __init__(self, user_id, username, custom_game_name):
        self.client = GameClient(user_id, username)
        self.world = WorldUnderstanding()
        self.client.add_listener(self)
        self.game_over = False

        if custom_game_name:
            self.client.join_custom(custom_game_name)
        else:
            self.client.join_1v1_queue()

    def handle_game_update(self, half_turns, tiles, armies, cities, enemy_position, 
                           enemy_total_army, enemy_total_land):
        self.world.update(tiles, armies, cities, enemy_position, enemy_total_army, enemy_total_land)

        # Move randomly
        delta_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        moves = [np.add(self.world.player_pos, delta_move) for delta_move in delta_moves]
        def move_feasible(position):
            if tuple(position) in self.world.mountains:
                return False
            if not 0 <= position[0] < self.world.map_size[0]:
                return False
            if not 0 <= position[1] < self.world.map_size[1]:
                return False
            return True
        move_options = [move for move in moves if move_feasible(move)]
        move = random.choice(move_options)
        self.client.attack(self.world.player_pos, move)

    def handle_game_start(self, map_size, start_pos, enemy_username):
        self.world.map_size = map_size
        self.world.player_pos = start_pos

    def handle_game_over(self, won, replay_url):
        if won:
            header = 'Game Won'
        else:
            header = 'Game Lost'
        print(header)
        print('='*len(header))
        print('Replay: %s\n' % replay_url)
        self.game_over = True

    def handle_chat(self, username, message):
        print('%s: %s' % (username, message))

    def block_forever(self):
        while not self.game_over:
            self.client.wait(seconds=2)


def main():
    if len(sys.argv) > 1:
        custom_game_name = sys.argv[1]
        run_forever = False
        print('Joining custom game %s' % custom_game_name)
    else:
        custom_game_name = None
        run_forever = True
        print('Joining 1v1 queue')

    while True:
        config = commentjson.loads(open(CONFIG_FILENAME).read())    
        bot = Bot(config['user_id'], config['username'], custom_game_name)
        bot.block_forever()
        if not run_forever:
            break


if __name__ == '__main__':
    main()
