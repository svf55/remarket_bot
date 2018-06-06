#!/usr/bin/env python
"""
    The task for the Remarket-bot: translation Depth of Market.
    Connecting to a web socket. Data parsing.
    Use of the module for handling pusher websockets.

"""


import json
import pysher
import logging
import time
from decimal import Decimal


def remove_order(order_type, price):
    """
        Stubs: actions in case of order removal from the Depth of Market.
    """
    print('Remove order \'{}\': price {}'.format(order_type, price))


def set_order(order_type, price, volume):
    """
        Stubs: actions in case of change of order from the Depth of Market.
    """
    print('Set order \'{}\': price {}, volume {}'.format(order_type, price, volume))


class WexRemarketBot(object):
    """
        Translation Depth of Market.
    """

    WEX_PUSHER_KEY = 'ee987526a24ba107824c'
    WEX_PUSHER_CLUSTER = 'eu'

    def __init__(self, pair_name):
        self.pair_name = pair_name
        self.pusher = pysher.Pusher(
            self.WEX_PUSHER_KEY,
            custom_host='ws-{}.pusher.com'.format(self.WEX_PUSHER_CLUSTER),
            log_level=logging.WARNING
        )
        self._logger = logging.getLogger(__name__)

    def run(self):
            self.pusher.connection.bind('pusher:connection_established', self._connect_handler)
            self.pusher.connect()

    def _connect_handler(self, data):
        channel = self.pusher.subscribe('{}.depth'.format(self.pair_name))
        channel.bind('depth', self._depth_handler)

    def _depth_handler(self, data):
        self._logger.info('Processing Data: {}'.format(data))
        data = json.loads(data)
        for order_type in data:
            for price, volume in data[order_type]:
                volume = Decimal(volume)
                price = Decimal(price)
                if volume == 0:
                    remove_order(order_type, price)
                else:
                    set_order(order_type, price, volume)
        print('\n')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Wex remarket bot')
    parser.add_argument('pair_name', help='Currency pair, example: btc_usd')
    args = parser.parse_args()

    # Setup logging
    FORMAT = '%(asctime)s %(process)d %(levelname)s %(name)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    # Run bot
    print('\n')
    WexRemarketBot(args.pair_name).run()
    while True:
        time.sleep(1)

