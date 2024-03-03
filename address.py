from newchain_web3 import Web3, HTTPProvider
import eth_utils as utils
import base58
import binascii

RPC = "https://jp.rpc.mainnet.newtonproject.org/"


def hex_to_new(address, chain_id):
    return encode_new_address(address, chain_id)


def is_new_address(address):
    return len(address) == 39 and address[:3] == "NEW"


def new_to_hex(address, chain_id):
    return decode_new_address(address, chain_id)


def encode_new_address(address, chain_id):
    address_data = address
    if address_data.startswith("0x"):
        address_data = address_data[2:]
    hex_chain_id = hex(chain_id)[2:][-8:]
    if (len(hex_chain_id) % 2) == 1:
        hex_chain_id = "0" + hex_chain_id
    num_sum = hex_chain_id + address_data
    data = base58.b58encode_check(b"\0" + binascii.a2b_hex(num_sum))
    new_address = "NEW" + data.decode()
    return new_address


def decode_new_address(address, chain_id):
    address_data = address[3:]
    hex_address = base58.b58decode_check(address_data)
    return hex_address.hex()[-40:]


def convert_address(address):
    """Convert address of NEW"""
    web3 = Web3(HTTPProvider(RPC))
    chain_id = int(web3.net.version)
    if utils.is_address(address):
        return hex_to_new(address, chain_id)
    elif is_new_address(address):
        return new_to_hex(address, chain_id)
    else:
        print("Address invalid")
        return ""


def get_balance(address):
    """Get the balance of the address"""
    web3 = Web3(HTTPProvider(RPC))
    a = web3.toChecksumAddress(convert_address(address))
    balance_wei = web3.eth.getBalance(a)
    b = web3.from_wei(balance_wei, "ether")
    # print("The balance of {} is {} NEW.".format(a, b))
    return b
