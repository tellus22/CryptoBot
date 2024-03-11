from web3 import Web3

from Services.DecimalService import to_decimals
from Services.HttpService import get_crypto_price
from config import ANKR_API_KEY

decimals = 18
precision = 4


class CryptoNetwork:
    def __init__(self, provider_url):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))

    def get_balance(self, address):
        address = Web3.to_checksum_address(address.strip())
        balance = self.w3.eth.get_balance(address)
        balance = to_decimals(balance, decimals, precision)
        return balance

    # def get_fee(self,from_address, to_address, amount):
    def get_fee(self, amount):
        print("chain_id ", self.w3.eth.chain_id)
        gas_price = self.w3.eth.gas_price
        print("gas_price", gas_price)
        # убрать
        from_address = self.w3.to_checksum_address('0x7bfee91193d9df2ac0bfe90191d40f23c773c060')
        to_address = self.w3.to_checksum_address('0x7Fd02c0d1Fd6300208AFe7bdeaC4D316924093AE')
        # ######
        txn = {
            'chainId': self.w3.eth.chain_id,
            'from': from_address,
            'to': to_address,
            'value': int(Web3.to_wei(amount, 'ether')),
            'nonce': self.w3.eth.get_transaction_count(from_address),
            'gasPrice': self.w3.eth.gas_price,
        }

        estimate_gas = self.w3.eth.estimate_gas(txn)
        print("estimate_gas ", estimate_gas)
        fee = self.w3.from_wei((estimate_gas * gas_price), 'ether')
        print("fee ", fee)
        return fee


networks = {
    "ETH": CryptoNetwork(f'https://rpc.ankr.com/eth/{ANKR_API_KEY}'),
    "BSC": CryptoNetwork(f'https://rpc.ankr.com/bsc/{ANKR_API_KEY}'),
    "OPTIMISM": CryptoNetwork(f'https://rpc.ankr.com/optimism/{ANKR_API_KEY}'),
    "OPBNB": CryptoNetwork('https://opbnb-rpc.publicnode.com'),
    "ARBITRUM": CryptoNetwork(f'https://rpc.ankr.com/arbitrum/{ANKR_API_KEY}'),
    "BASE": CryptoNetwork(f'https://rpc.ankr.com/base/{ANKR_API_KEY}'),
    "LINEA": CryptoNetwork('https://linea.decubate.com'),
    "SEPOLIA": CryptoNetwork(f'https://rpc.ankr.com/eth_sepolia/{ANKR_API_KEY}'),
    "GOERLI": CryptoNetwork(f'https://rpc.ankr.com/eth_goerli/{ANKR_API_KEY}'),
    "POLYGON": CryptoNetwork(f'https://rpc.ankr.com/polygon/{ANKR_API_KEY}'),
    "AVALANCHE": CryptoNetwork(f'https://rpc.ankr.com/avalanche/{ANKR_API_KEY}'),
    "ZKSYNK": CryptoNetwork(f'https://rpc.ankr.com/zksync_era/{ANKR_API_KEY}'),
    "SCROLL": CryptoNetwork(f'https://rpc.ankr.com/scroll/{ANKR_API_KEY}'),

}

currency_to_network = {
    "ETH": "ETH",
    "BSC": "BNB",
    "OPTIMISM": "ETH",
    "OPBNB": "BNB",
    "ARBITRUM": "ETH",
    "BASE": "ETH",
    "LINEA": "ETH",
    "SEPOLIA": "ETH",
    "GOERLI": "ETH",
    "POLYGON": "MATIC",
    "AVALANCHE": "AVAX",
    "ZKSYNK": "ETH",
    "SCROLL": "ETH",

}


def get_networks():
    return networks


def get_currency_to_network():
    return currency_to_network


def get_networks_name():
    network_names = get_networks().keys()
    names_list = []
    for network_name in network_names:
        names_list.append(network_name)
    return names_list


def get_balance_network(network, address):
    crypto_network = networks.get(network)
    if crypto_network:
        balance = crypto_network.get_balance(address)
        return balance
    else:
        return None


# def get_fee_network(network, from_address, to_address, amount):
def get_fee_network(network, amount):
    crypto_network = networks.get(network)
    if crypto_network:
        fee = crypto_network.get_fee(amount)
        # fee = crypto_network.get_fee(from_address, to_address, amount)
        return fee
    else:
        return None


def get_balance_usd(network, balance):
    balance = float(balance)
    network_currency = get_currency_to_network()[network]
    price = get_crypto_price(network_currency)
    usd_balance = round(balance * price, precision)
    return usd_balance
