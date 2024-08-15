from data.network import *

CHAIN = BaseRPC
GAS_PRICE_MAXIMUM = 2
GAS_PRICE_MULTIPLIER = 1.3
GAS_LIMIT_MULTIPLIER = 1.3
SLEEP_ACCOUNT = [22, 222]
IF_THE_MINIMUM_ACCOUNT_BALANCE_IS_MORE_THAN = 0.001  # Если баланс аккаунта меньше указанного числа, то вывод средств выполнятся не будет


class TransferSettings:
    TOKEN_CONTRACT = ''

    # transfer_with_contract = True

    withdraw_amount = [0.001, 0.002]
    percentage = True
    withdraw_percentage = [91, 93]

