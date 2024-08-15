import random

from module.transfer import Transfer
from Account import add_logger
from other.read_db import get_bd


class Runner:
    def __init__(self):
        self.logger = add_logger()
        self.bd = get_bd()
        print(
            '\033[91m Developed by @Irorsss \033[m' +
            f""" \033[96m
1. 📁 Transfer to OKX
2. 📁 Transfer to BITGET
3. 📁 Transfer random CEX
\033[m """
        )
        self.answer = int(input("\033[94m---➜ \033[0m "))

    @staticmethod
    def withdraw(private_key, address_transfer, cex):

        worker = Transfer(private_key=private_key)
        worker.withdraw(address_transfer=address_transfer, cex=cex)
        return worker.notes_transfer

    def start(self, private_key):
        # try:

            if self.answer == 1:
                return Runner.withdraw(private_key=private_key,
                                       address_transfer=[self.bd[i]["OKX"] for i in range(len(self.bd)) if
                                                         str(self.bd[i]["PrivateKey"]).lower() == str(
                                                             private_key).lower()][0],
                                       cex='OKX')

            elif self.answer == 2:
                return Runner.withdraw(private_key=private_key,
                                       address_transfer=[self.bd[i]["BITGET"] for i in range(len(self.bd)) if
                                                         str(self.bd[i]["PrivateKey"]).lower() == str(
                                                             private_key).lower()][
                                           0],
                                       cex='BITGET')

            elif self.answer == 3:
                cex = random.choice(["BITGET", "OKX"])
                return Runner.withdraw(private_key=private_key,
                                       address_transfer=[self.bd[i][cex] for i in range(len(self.bd)) if
                                                         str(self.bd[i]["PrivateKey"]).lower() == str(
                                                             private_key).lower()][0],
                                       cex=cex)

        # except Exception as error:
        #     self.logger.error(f'Error: {error}')
