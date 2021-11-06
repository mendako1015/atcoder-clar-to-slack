#!/usr/bin/env python3

import sys, time, yaml
import atcoder as ac
import slack as sl

def load_config():
    with open(sys.argv[1], 'r') as f:
        return yaml.load(f, Loader = yaml.FullLoader)

def main():
    config = load_config()
    atcoder = ac.Atcoder()
    atcoder.login(config['USERNAME'], config['PASSWORD'])
    slack = sl.Slack()

    clars = atcoder.load_clar_page(config['CLAR_URL'])
    while True:
        try:
            current_clars = atcoder.load_clar_page(config['CLAR_URL'])
            for i in range(len(current_clars)):
                if i >= len(clars) or clars[i].update_time != current_clars[i].update_time:
                    slack.send_message(config['SLACK_URL'],
                                    current_clars[i].convert_json(i < len(clars)))
            clars = current_clars
            time.sleep(config['INTERVAL'])
        except:
            print('Connection Error')

if __name__ == "__main__":
    main()
