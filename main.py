import random

from other.functions_run import Runner, add_logger
from other.add_sleep import sleep_account


def main(count, all_value):
    with open('data/wallets.txt', 'r') as file:
        private_keys = [i.strip() for i in file]

    runner = Runner()
    logger = add_logger()

    random.shuffle(private_keys)
    for private_key in private_keys:
        try:
            notes_transfer = runner.start(private_key=private_key)
            sleep_account()
            count += 1

            for value in (notes_transfer.values() if notes_transfer is not None else [0]):
                all_value += float(value)
        except Exception as err:
            logger.error(err)

    return count, all_value


if __name__ == '__main__':
    count = 0
    all_value = 0
    count, all_value = main(count, all_value)

    print(f'Выведено с {count} кошельков токенов на сумму общую сумму: {all_value}.')

