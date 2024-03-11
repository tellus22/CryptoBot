from web3 import Web3

from Blockchain.Erc721Abi import erc721_abi
from config import ANKR_API_KEY

decimals = 18
precision = 2


class ERC721Token:
    def __init__(self, contract_address, provider_url):
        self.contract_address = contract_address
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = self.w3.eth.contract(address=contract_address, abi=erc721_abi)

    def get_balance(self, address):
        address = Web3.to_checksum_address(address.strip())
        balance = self.contract.functions.balanceOf(address).call()
        return balance


erc721_tokens = {
    "ETH": {
        "PudgyPenguins": ERC721Token(Web3.to_checksum_address("0xBd3531dA5CF5857e7CfAA92426877b022e612cf8"),
                                     f'https://rpc.ankr.com/eth/{ANKR_API_KEY}'),
        "BoredApeYachtClub": ERC721Token(Web3.to_checksum_address("0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"),
                                         f'https://rpc.ankr.com/eth/{ANKR_API_KEY}'),
    },
    "BSC": {
        "NAME": ERC721Token(Web3.to_checksum_address("0x55d398326f99059ff775485246999027b3197955"),
                            f'https://rpc.ankr.com/bsc/{ANKR_API_KEY}'),
        "NAME1": ERC721Token(Web3.to_checksum_address("0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"),
                            f'https://rpc.ankr.com/bsc/{ANKR_API_KEY}'),
    },
    "OPTIMISM": {
        "NAME3": ERC721Token(Web3.to_checksum_address("0x94b008aa00579c1307b0ef2c499ad98a8ce58e58"),
                            f'https://rpc.ankr.com/optimism/{ANKR_API_KEY}'),
        "NAME4": ERC721Token(Web3.to_checksum_address("0x4200000000000000000000000000000000000042"),
                          f'https://rpc.ankr.com/optimism/{ANKR_API_KEY}'),
    },
}


def get_erc721_tokens():
    return erc721_tokens


def get_balance_erc721_tokens(network, address):
    nft_balances = {}
    nft_info = erc721_tokens.get(network)
    if nft_info:
        for nft_name, nft in nft_info.items():
            balance = nft.get_balance(address)
            nft_balances[nft_name] = balance
    return nft_balances
