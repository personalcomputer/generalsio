import commentjson
import numpy as np
import random

from generalsio import GameClient, GameClientListener


CONFIG_FILENAME = 'config.json'


class WorldUnderstanding(object):

    def __init__(self):
        self.map_size = (None, None)
        self.enemy_pos = None
        self.player_pos = None

        self.cities = None
        self.mountains = None

        self.last_seen_scores = None
        self.expected_scores = None

    def update(self, tiles, armies, cities, enemy_position, enemy_total_army, enemy_total_land):
        pass


class Bot(object, GameClientListener):

    def __init__(self, game_client):
        self.client = game_client
        self.world = WorldUnderstanding()
        self.client.add_listener(self)

    def handle_game_update(self, tiles, armies, cities, enemy_position, enemy_total_army,
                           enemy_total_land):
        self.world.update(tiles, armies, cities, enemy_position, enemy_total_army, enemy_total_land)

        # Move randomly
        delta_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        moves = [np.add(self.world.player_pos, delta_move) for delta_move in delta_moves]
        def move_feasible(position):
            if position in self.world.mountains:
                return False
            if not 0 <= position.x < self.world.map_size[0]:
                return False
            if not 0 <= position.y < self.world.map_size[1]:
                return False
            return True
        move_options = [move for move in moves if move_feasible(move)]
        move = random.choice(move_options)
        self.client.move(self.world.player_pos, move)

    def handle_game_start(self):
        pass

    def handle_game_over(self, won, replay_url):
        if won:
            header = 'Game Won'
        else:
            header = 'Game Lost'
        print(header)
        print('%s\n' % '='*len(header))
        print('Replay: %s' % replay_url)


def main():
    config = commentjson.loads(open(CONFIG_FILENAME).read())
    client = GameClient(config['user_id'], config['username'])
    
    bot = Bot(client)


if __name__ == '__main__':
    main()
