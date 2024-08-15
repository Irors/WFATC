from web3 import Web3
from data.settings import *
from other.add_loguru import add_logger
from data.constant import ABI
import random


class Web3Client:
    def __init__(self, private_key):
        self.network = CHAIN
        self.web3 = Web3(Web3.HTTPProvider(random.choice(self.network.rpc)))
        self.private_key = private_key
        self.address = self.web3.to_checksum_address(self.get_address_from_private_key(self.private_key))
        self.logger = add_logger()


    def convert_to_wei(self, value):
        return self.web3.to_wei(value, 'ether')

    def convert_from_wei(self, value):
        return self.web3.from_wei(value, 'ether')

    def get_value(self, value):
        return value, self.convert_to_wei(value)

    def get_address_from_private_key(self, private_key):
        return self.web3.eth.account.from_key(private_key=private_key).address

    def get_priotiry_fee(self):
        fee_history = self.web3.eth.fee_history(5, 'latest', [20.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]

        divisor_priority = max(len(non_empty_block_priority_fees), 1)

        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))

        return priority_fee

    def prepare_transaction(self, value=0):
        tx_params = {
            'chainId': self.web3.eth.chain_id,
            'from': self.web3.to_checksum_address(self.address),
            'nonce': self.web3.eth.get_transaction_count(self.address),
            'value': value,
        }

        if self.network.eip1559_support:

            base_fee = self.web3.eth.gas_price
            max_priority_fee_per_gas = self.get_priotiry_fee()
            max_fee_per_gas = int(base_fee + max_priority_fee_per_gas * 1.05 * GAS_PRICE_MULTIPLIER)

            if max_priority_fee_per_gas > max_fee_per_gas:
                max_priority_fee_per_gas = int(max_fee_per_gas * 0.95)

            tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            tx_params['maxFeePerGas'] = int(max_fee_per_gas * 1.2)
            tx_params['type'] = '0x2'

        else:
            if self.network.name == 'BNB Chain':
                tx_params['gasPrice'] = self.web3.to_wei(round(random.uniform(1.4, 1.5), 1), 'gwei')
            else:
                gas_price = self.web3.eth.gas_price
                if self.network.name == ['Scroll', 'Optimism']:
                    gas_price = int(gas_price / GAS_PRICE_MULTIPLIER * 1.1)

                tx_params['gasPrice'] = int(gas_price * 1.2 * GAS_PRICE_MULTIPLIER)

        return tx_params

    def transaction_runner(self, transaction):
        transaction['gas'] = int((self.web3.eth.estimate_gas(transaction)) * GAS_LIMIT_MULTIPLIER)
        sign_txn_claim = self.web3.eth.account.sign_transaction(transaction,
                                                                private_key=self.private_key)
        submitted_transaction = self.web3.eth.send_raw_transaction(sign_txn_claim.rawTransaction)
        return submitted_transaction

    def get_transaction(self, submitted_transaction):
        self.web3.eth.wait_for_transaction_receipt(
            transaction_hash=self.web3.to_hex(submitted_transaction), timeout=300)
        return self.web3.eth.wait_for_transaction_receipt(
            transaction_hash=self.web3.to_hex(submitted_transaction), timeout=300)

    def send_transaction(self, transaction):
        submitted_transaction = self.transaction_runner(transaction=transaction)
        self.logger.info(f'[{self.address}] | transaction: {self.network.explorer}tx/{submitted_transaction.hex()}')

        if self.get_transaction(submitted_transaction=submitted_transaction).status:
            self.logger.success(f'[{self.address}] | transaction completed 📗')
            return True

        else:
            self.logger.error(f'[{self.address}] | transaction failed 📕')
            return False

    def get_contract(self, address, abi):
        return self.web3.eth.contract(address=self.web3.to_checksum_address(address), abi=abi)

    def get_allowance(self, token_address, spender_address):
        contract = self.get_contract(token_address, ABI)
        return contract.functions.allowance(
            self.address,
            spender_address
        ).call()

    def make_approve(
            self, token_address, spender_address, amount_in_wei, unlimited_approve, symbol
    ):
        self.logger.info(f'[{self.address}] | make approve {symbol} 📒')

        transaction = self.get_contract(token_address, ABI).functions.approve(
            spender_address,
            amount=2 ** 256 - 1 if unlimited_approve else amount_in_wei
        ).build_transaction(self.prepare_transaction())

        return self.send_transaction(transaction)


    def gas_checker(self):
        if GAS_PRICE_MAXIMUM:
            while GAS_PRICE_MAXIMUM >= self.web3.eth.gas_price:
                self.logger.debug(f'current gas: {self.web3.eth.gas_price / 10**9} > {GAS_PRICE_MAXIMUM} | wait...')
            return True

    def check_for_approved(
            self, token_address, spender_address, amount_in_wei,
            unlimited_approve
    ):
        contract = self.get_contract(token_address, ABI)

        balance_in_wei = contract.functions.balanceOf(self.address).call()
        symbol = contract.functions.symbol().call()

    def check_balanceOf(
            self, token_address,
    ):
        contract = self.get_contract(token_address, ABI)

        balance_in_wei = contract.functions.balanceOf(self.address).call()
        return balance_in_wei

    def check_balance_native_from_wei(self):
        return self.convert_from_wei(self.web3.eth.get_balance(account=self.address))
