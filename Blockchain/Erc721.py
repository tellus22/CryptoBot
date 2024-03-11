# import requests
# import solcx
# from solcx import compile_source, set_solc_version, get_solc_version, set_solc_version_pragma
# from web3 import Web3
# from solc import install_solc
# from config import ANKR_API_KEY, PRIVATE_KEY
# solcx.install_solc('0.8.20')
# # Устанавливаем версию Solidity
# set_solc_version('v0.8.20')
#
#
# def download_openzeppelin_contract(contract_url):
#     response = requests.get(contract_url)
#     if response.status_code == 200:
#         return response.text
#     else:
#         raise Exception(f"Failed to download contract from {contract_url}")
#
#
# def compile_contract():
#     erc721_source_code = download_openzeppelin_contract(
#         "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/token/ERC721/ERC721.sol")
#
#     contract_source_code = f'''
#     // SPDX-License-Identifier: MIT
#     pragma solidity ^0.8.0;
#
#     {erc721_source_code}
#
#     contract MyNFT is ERC721 {{
#         constructor(string memory name, string memory symbol) ERC721(name, symbol) {{
#         }}
#
#         function mint(address to, uint256 tokenId) public {{
#             _mint(to, tokenId);
#         }}
#     }}
#     '''
#     compiled_sol = compile_source(contract_source_code)
#     contract_interface = compiled_sol['<stdin>:MyNFT']
#     return contract_interface
#
#
# def get_private_key():
#     return PRIVATE_KEY
#
#
# # def deploy_contract(contract_interface, web3, private_key):
# #     contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
# #     account = web3.toChecksumAddress('ADDRESS')
# #     nonce = web3.eth.getTransactionCount(account)
# #     tx = contract.constructor("MyNFT Name", "MNFT").buildTransaction({
# #         'from': account,
# #         'nonce': nonce,
# #         'gas': 2000000,
# #         'gasPrice': web3.toWei('50', 'gwei')
# #     })
# #     signed_tx = web3.eth.account.signTransaction(tx, private_key)
# #     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
# #     tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
# #     contract_address = tx_receipt.contractAddress
# #     return contract_address
#
#
# if __name__ == "__main__":
#     compile_contract()
#     # contract_interface = compile_contract()
#     # web3 = Web3(Web3.HTTPProvider(f'https://rpc.ankr.com/eth_goerli/{ANKR_API_KEY}'))
#     # tx = deploy_contract(contract_interface, web3)
#     # print(tx)
#     # contract_address = deploy_contract(contract_interface, web3, get_private_key())
#     # print("Contract deployed at:", contract_address)
