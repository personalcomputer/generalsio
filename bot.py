import commentjson

from pygeneralsio import Client


CONFIG_FILENAME = 'config.json'


def main():
    config = commentjson.loads(open(CONFIG_FILENAME).read())
    client = Client(config['server'], config['user_id'], config['username'])


if __name__ == '__main__':
    main()
