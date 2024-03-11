from web3 import Web3

from Blockchain.Erc20Abi import erc20_abi
from Services.DecimalService import to_decimals
from config import ANKR_API_KEY

decimals = 18
precision = 2


class ERC20Token:
    def __init__(self, contract_address, provider_url):
        self.contract_address = contract_address
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = self.w3.eth.contract(address=contract_address, abi=erc20_abi)

    def get_balance(self, address):
        address = Web3.to_checksum_address(address.strip())
        balance = self.contract.functions.balanceOf(address).call()
        return balance

    def get_decimals(self):
        token_decimals = self.contract.functions.decimals().call()
        return token_decimals


erc20_tokens = {
    "ETH": {
        "USDT": ERC20Token(Web3.to_checksum_address("0xdac17f958d2ee523a2206206994597c13d831ec7"),
                           f'https://rpc.ankr.com/eth/{ANKR_API_KEY}'),
    },
    "BSC": {
        "USDT": ERC20Token(Web3.to_checksum_address("0x55d398326f99059ff775485246999027b3197955"),
                           f'https://rpc.ankr.com/bsc/{ANKR_API_KEY}'),
        "USDC": ERC20Token(Web3.to_checksum_address("0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"),
                           f'https://rpc.ankr.com/bsc/{ANKR_API_KEY}'),
    },
    "OPTIMISM": {
        "USDT": ERC20Token(Web3.to_checksum_address("0x94b008aa00579c1307b0ef2c499ad98a8ce58e58"),
                           f'https://rpc.ankr.com/optimism/{ANKR_API_KEY}'),
        "OP": ERC20Token(Web3.to_checksum_address("0x4200000000000000000000000000000000000042"),
                         f'https://rpc.ankr.com/optimism/{ANKR_API_KEY}'),
    },
}


def get_erc20_tokens():
    return erc20_tokens


def get_balance_erc20_tokens(network, address):
    token_balances = {}
    token_info = erc20_tokens.get(network)
    if token_info:
        for token_name, token in token_info.items():
            token_decimal = token.get_decimals()
            balance = to_decimals(token.get_balance(address), token_decimal, precision)
            token_balances[token_name] = balance
    return token_balances
