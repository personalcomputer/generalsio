import commentjson

from generalsio import generals


CONFIG_FILENAME = 'config.json'


def main():
    config = commentjson.loads(open(CONFIG_FILENAME).read())
    client = generals.Generals(config['user_id'], config['username'])


if __name__ == '__main__':
    main()
