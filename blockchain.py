import warnings
import requests
from pysui import SuiConfig, SyncClient
from pysui.sui.sui_txn import SyncTransaction
from pysui.sui.sui_types import SuiString, SuiInteger, SuiAddress
from pysui.sui.sui_crypto import gen_mnemonic_phrase, recover_key_and_address
from pysui.abstracts.client_keypair import SignatureScheme
from config import SUI_RPC_URL

#PYSUI IMPORTS
warnings.filterwarnings("ignore", category=DeprecationWarning)


# WEB3 / CRYPTO FUNCTIONS

def generate_new_wallet():
    mnemonic = gen_mnemonic_phrase(12)
    derivation_path = "m/44'/784'/0'/0'/0'"
    mnem, keypair, address = recover_key_and_address(
        SignatureScheme.ED25519,
        mnemonic,
        derivation_path
    )
    return str(address), keypair.serialize(), mnemonic

def get_sui_balance(address: str):
    try:
        cfg = SuiConfig.user_config(prv_keys=[], rpc_url=SUI_RPC_URL)
        client = SyncClient(cfg)
        result = client.get_gas(SuiAddress(address))
        if result.is_ok():
            total_mist = sum(int(obj.balance) for obj in result.result_data.data)
            return total_mist / 1_000_000_000
        return 0.0
    except Exception as e:
        return 0.0

def send_sui_payment(sender_priv_key: str, recipient_addr: str, amount_sui: float):
    amount_mist = int(amount_sui * 1_000_000_000)
    try:
        cfg = SuiConfig.user_config(prv_keys=[sender_priv_key], rpc_url=SUI_RPC_URL)
        client = SyncClient(cfg)
        txn = SyncTransaction(client=client)
        split_coin = txn.split_coin(coin=txn.gas, amounts=[SuiInteger(amount_mist)])
        txn.transfer_objects(transfers=[split_coin], recipient=SuiAddress(recipient_addr))
        result = txn.execute(gas_budget="5000000")
        if result.is_ok():
            digest = result.result_data.digest if hasattr(result.result_data, 'digest') else "Unknown Digest"
            return True, digest
        else:
            return False, result.result_string
    except Exception as e:
        return False, str(e)
    
def get_sui_market_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=sui&vs_currencies=usd&include_24h_change=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['sui']['usd'], data['sui']['usd_24h_change']
    except:
        return 1.56, 2.22
