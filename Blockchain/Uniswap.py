import time

from web3 import Web3

from Blockchain.Erc20Abi import erc20_abi
from Blockchain.UniswapAbi import uniswap_abi
from Services.DecimalService import to_decimals
from config import ANKR_API_KEY, PRIVATE_KEY, UNISWAP_CONTRACT_ADDRESS

web3 = Web3(Web3.HTTPProvider(f'https://rpc.ankr.com/eth_goerli/{ANKR_API_KEY}'))
swap_contract_address = web3.to_checksum_address(UNISWAP_CONTRACT_ADDRESS)
user_address = web3.to_checksum_address('0x7Fd02c0d1Fd6300208AFe7bdeaC4D316924093AE')

# get native token balance
# balance = web3.eth.get_balance(web3.to_checksum_address('0x7Fd02c0d1Fd6300208AFe7bdeaC4D316924093AE'))
# balance = to_decimals(balance, 18, 4)
# print(balance)


def getPrivateKey():
    return PRIVATE_KEY


def allowance(token_out_address):
    token_out_address = web3.to_checksum_address(token_out_address)
    token_out_contract = web3.eth.contract(address=token_out_address, abi=erc20_abi)
    allowance_value = token_out_contract.functions.allowance(user_address, swap_contract_address).call()
    return allowance_value


def approve(token_address):
    token_address = web3.to_checksum_address(token_address)
    token = web3.eth.contract(address=token_address, abi=erc20_abi)
    spender = swap_contract_address
    # max_amount = web3.to_wei(value, 'ether')
    max_amount = web3.to_wei(2 ** 64 - 1, 'ether')
    nonce = web3.eth.get_transaction_count(user_address)

    approve_tx = token.functions.approve(spender, max_amount).build_transaction({
        'from': user_address,
        'nonce': nonce
    })

    approve_signed_tx = web3.eth.account.sign_transaction(approve_tx, getPrivateKey())
    approve_tx_hash = web3.eth.send_raw_transaction(approve_signed_tx.rawTransaction)
    print("approve_tx_hash: ", web3.to_hex(approve_tx_hash))
    return web3.to_hex(approve_tx_hash)


def swap(token_out_address, token_in_address, value_to_swap):
    router_contract = web3.eth.contract(address=swap_contract_address, abi=uniswap_abi)
    # user_address = web3.to_checksum_address(user_address)
    token_out = web3.to_checksum_address(token_out_address)
    token_in = web3.to_checksum_address(token_in_address)
    value = int(value_to_swap * 10 ** 18)

    params = (
        token_out,  # токен который отдаем
        token_in,  # токен который получаем
        3000,
        user_address,  # получатель
        round(time.time()) + 60 * 20,
        value,
        0,
        0,
    )
    tx_params = {
        'nonce': web3.eth.get_transaction_count(user_address),
        'gas': 2100000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'value': value
    }
    swap_tx = router_contract.functions.exactInputSingle(params).build_transaction(tx_params)
    swap_signed_tx = web3.eth.account.sign_transaction(swap_tx, getPrivateKey())
    swap_tx_hash = web3.eth.send_raw_transaction(swap_signed_tx.rawTransaction)
    print("swap_tx_hash: ", web3.to_hex(swap_tx_hash))
    return web3.to_hex(swap_tx_hash)


def transaction_status(tx_hash):
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt["status"]
