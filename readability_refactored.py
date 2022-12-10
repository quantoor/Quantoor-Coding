import telegram
import util
import strategy
import time


class CryptoBreakoutBot:
    def __init__(self, token: str, chat_id: str):
        self._bot = telegram.Bot(token=token)
        self._chat_id = chat_id
        self._found_symbols_to_timestamp = {}  # {found symbol: timestamp found} Used to avoid signaling the same symbol again before some time has passed

    def start(self):
        all_symbols = util.get_all_symbols()
        print(f'All symbols: {all_symbols}')

        while True:  # TODO this is an infinite loop witout an exit condition. Change this.
            for symbol in all_symbols:

                if self._is_already_found_within_last_hour(symbol):
                    # ignore if already found this symbol within the last hour
                    continue

                is_consolidating, is_pumping = strategy.check_status_now(symbol)
                print(f"{symbol} is consolidating: {is_consolidating}, is breaking out: {is_pumping}")

                if is_consolidating and is_pumping:
                    # send Telegram notification
                    self._bot.sendMessage(chat_id=self._chat_id, text=f"{symbol} is breaking out")

                    # add the symbol to the found dict with the corresponding timestamp
                    self._found_symbols_to_timestamp[symbol] = time.time()

    def _is_already_found_within_last_hour(self, symbol: str) -> bool:
        """Returns True if the symbol has been already found within the last hour, False otherwise"""
        if symbol not in self._found_symbols_to_timestamp:
            return False

        last_timestamp_found = self._found_symbols_to_timestamp[symbol]
        return (time.time() - last_timestamp_found) < 3600


def main():
    with open('private.txt', 'r') as f:
        token = f.readline().strip()
        chat_id = f.readline()

    bot = CryptoBreakoutBot(token, chat_id)
    bot.start()


if __name__ == '__main__':
    main()
