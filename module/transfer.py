import random

from data.settings import *
from Account import Web3Client
from data.constant import ABI
from other.datatypes import *


class Transfer(Web3Client):
    def __init__(self, private_key):
        super().__init__(private_key)
        self.contract = self.get_contract(
            address=TransferSettings.TOKEN_CONTRACT,
            abi=ABI
        ) if TransferSettings.TOKEN_CONTRACT != '' else None
        self.settings = TransferSettings()
        self.notes_transfer = {}

    def withdraw(self, address_transfer, cex=None):
        if (int(self.web3.to_wei(IF_THE_MINIMUM_ACCOUNT_BALANCE_IS_MORE_THAN, 'ether')) >
                int(self.web3.eth.get_balance(self.web3.to_checksum_address(self.address)))):

            raise BalanceSmall(f'[{self.address}] | На аккауте средств меньше, чем установлено в лимите')


        if TransferSettings.TOKEN_CONTRACT == '':
            value_transfer = int(self.web3.eth.get_balance(self.web3.to_checksum_address(self.address)) * (
                    random.randint(self.settings.withdraw_percentage[0],
                                   self.settings.withdraw_percentage[1]) / 100) if self.settings.percentage
                                 else random.randint(self.settings.withdraw_amount[0],
                                                     self.settings.withdraw_amount[1]))

            self.logger.info(
                f'[{self.address}] | Transfer | make transfer ['
                f'{round(value_transfer / 10 ** 18, 5)} {self.network.token}] to {cex} [{address_transfer}] 📘')

            transaction = super().prepare_transaction(value=value_transfer)
            transaction['to'] = self.web3.to_checksum_address(address_transfer)
            transaction['gas'] = self.web3.eth.estimate_gas(transaction)
            while self.send_transaction(transaction):
                break
            self.notes_transfer.update({cex: self.notes_transfer.get(cex, 0) + value_transfer / 10 ** 18})

        else:

            if self.gas_checker():
                pass


            balance_in_wei = self.check_balanceOf(
                self.web3.to_checksum_address(TransferSettings.TOKEN_CONTRACT))

            self.check_for_approved(
                token_address=self.web3.to_checksum_address(TransferSettings.TOKEN_CONTRACT),
                spender_address=TransferSettings.TOKEN_CONTRACT,
                amount_in_wei=balance_in_wei,
                unlimited_approve=True)

            tx_params = super().prepare_transaction()

            value_transfer = int(balance_in_wei * (random.randint(self.settings.withdraw_percentage[0],
                                                                  self.settings.withdraw_percentage[
                                                                      1]) / 100) if self.settings.percentage
                                 else random.randint(self.settings.withdraw_amount[0],
                                                     self.settings.withdraw_amount[1]))

            transaction = self.contract.functions.transfer(
                self.web3.to_checksum_address(address_transfer),
                value_transfer
            ).build_transaction(tx_params)

            self.logger.info(
                f'[{self.address}] | Transfer | make transfer [{round(value_transfer / 10 ** 18, 5)} '
                f'{self.contract.functions.symbol().call()}] to {cex} [{address_transfer}] 📘')

            while self.send_transaction(transaction):
                break
            self.notes_transfer.update({cex: self.notes_transfer.get(cex, 0) + balance_in_wei / 10 ** 18})
