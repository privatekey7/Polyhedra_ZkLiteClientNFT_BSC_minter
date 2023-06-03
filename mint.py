import random
import time
from web3 import Web3

rpc_endpoint = 'https://rpc.ankr.com/bsc'
w3 = Web3(Web3.HTTPProvider(rpc_endpoint))

with open('private_key.txt', 'r') as f:
    private_keys = f.readlines()

def mint_nft(private_key):
    account = w3.eth.account.from_key(private_key.strip())
    wallet_address = account.address
    print(f'{wallet_address} - Начинаю минт')
    contract_address = '0xD2cCC9EE7Ea2ccd154c727A46D475ddA49E99852'
    contract_abi = '[{"type":"function","name":"balanceOf","inputs":[{"type":"address"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"explicitOwnershipOf","inputs":[{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"isApprovedForAll","inputs":[{"type":"address"},{"type":"address"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"setMintTimes","inputs":[{"type":"uint256"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"mintEndTime","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"setApprovalForAll","inputs":[{"type":"address"},{"type":"bool"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"approve","inputs":[{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"renounceOwnership","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"tokenURI","inputs":[{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"setMetadataUri","inputs":[{"type":"string"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"mintStartTime","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"tokensOfOwnerIn","inputs":[{"type":"address"},{"type":"uint256"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"totalSupply","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"owner","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"tokensOfOwner","inputs":[{"type":"address"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"supportsInterface","inputs":[{"type":"bytes4"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"mint","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"safeTransferFrom","inputs":[{"type":"address"},{"type":"address"},{"type":"uint256"},{"type":"bytes"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"mintLimit","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"transferOwnership","inputs":[{"type":"address"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"ownerOf","inputs":[{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"name","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"transferFrom","inputs":[{"type":"address"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"safeTransferFrom","inputs":[{"type":"address"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"getApproved","inputs":[{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"explicitOwnershipsOf","inputs":[{"type":"uint256[]"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"symbol","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"getMintSurplus","inputs":[{"type":"address"}],"outputs":[{"type":"unknown"}]}]'
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    delay = random.randint(15, 30)
    time.sleep(delay)
    tx_data = contract.functions.mint().build_transaction({
        'from': account.address,
        'gas': 108000,
        'gasPrice': w3.to_wei(1, 'gwei'),
        'nonce': w3.eth.get_transaction_count(account.address),
    })

    signed_tx = account.sign_transaction(tx_data)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f'https://bscscan.com/tx/{tx_hash.hex()} - жду подтвержения')

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    if tx_receipt.status == 1:
        print(f'Минт успешен')
    else:
        print(f'{wallet_address} - Минт не удался')

def check_nft_balance(private_key):
    account = w3.eth.account.from_key(private_key.strip())
    wallet_address = account.address
    contract_address = '0xD2cCC9EE7Ea2ccd154c727A46D475ddA49E99852'
    contract_abi = '[{"type":"function","name":"balanceOf","inputs":[{"type":"address"}],"outputs":[{"type":"uint256"}]}]'
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    nft_balance = contract.functions.balanceOf(wallet_address).call()
    if nft_balance > 0:
        print(f'{wallet_address} - NFT уже сминчен')
        return True

    return False


used_private_keys = set()
while True:
    available_private_keys = [pk.strip() for pk in private_keys if pk.strip() not in used_private_keys]
    if not available_private_keys:
        print('Все приватные ключи использованы')
        break

    private_key = random.choice(available_private_keys)
    used_private_keys.add(private_key)
    try:
        if check_nft_balance(private_key):
            continue
        mint_nft(private_key)
    except TimeoutError:
        print(f'{private_key} - Превышен лимит времени на транзакцию')
        continue