import shareithub
import math
import sys
import requests
import time
import threading
from shareithub import shareithub
from web3 import Web3
from colorama import init, Fore
from rich.console import Console
from fake_useragent import UserAgent

shareithub()
init(autoreset=True)
console = Console()

RPC_URL = 'https://rpc.testnet.humanity.org'
PRIVATE_KEYS_FILE = 'private_keys.txt'
FAUCET_API_URL = "https://faucet.testnet.humanity.org/api/claim"
CONTRACT_ADDRESS = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'

CONTRACT_ABI = [{"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"bufferSafe","type":"bool"}],"name":"ReferralRewardBuffered","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"enum IRewards.RewardType","name":"rewardType","type":"uint8"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cycleStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vcContract","type":"address"},{"internalType":"address","name":"tkn","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"startTimestamp","type":"uint256"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]

def setup_blockchain_connection():
    console.print("[bold cyan]🔗 Menghubungkan ke Humanity Protocol...[/bold cyan]")
    web3 = Web3(Web3.HTTPProvider(RPC_URL))

    if web3.is_connected():
        console.print("[bold green]✅ Koneksi berhasil![/bold green]")
    else:
        console.print(f"{Fore.RED}❌ Gagal terhubung!")
        sys.exit(1)
    
    return web3

def load_wallets():
    try:
        with open(PRIVATE_KEYS_FILE, 'r') as file:
            keys = [line.strip() for line in file if line.strip()]
            wallets = [{"private_key": key, "address": Web3().eth.account.from_key(key).address} for key in keys]
            console.print(f"[bold magenta]🔑 {len(wallets)} Wallet ditemukan![/bold magenta]")

            for w in wallets:
                console.print(f"🔹 Wallet Address: {w['address']}")
            
            return wallets
    except FileNotFoundError:
        console.print(f"{Fore.RED}🚨 File {PRIVATE_KEYS_FILE} tidak ditemukan!")
        sys.exit(1)

def claim_faucet(wallets):
    ua = UserAgent()

    for wallet in wallets:
        while True: 
            headers = {
                "authority": "faucet.testnet.humanity.org",
                "method": "POST",
                "path": "/api/claim",
                "scheme": "https",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9,id;q=0.8",
                "content-length": "56",
                "content-type": "application/json",
                "origin": "https://faucet.testnet.humanity.org",
                "priority": "u=1, i",
                "referer": "https://faucet.testnet.humanity.org/",
                "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": ua.random, 
            }
            payload = {"address": wallet["address"]}

            try:
                response = requests.post(FAUCET_API_URL, json=payload, headers=headers)
                response_json = response.json() if response.status_code == 200 else {}

                if response.status_code == 200:
                    tx_hash = response_json.get("msg", "TX Hash tidak ditemukan")
                    console.print(f"💰 [bold green]Faucet berhasil diklaim untuk {wallet['address']}![/bold green] - TX Hash: {tx_hash}")
                    break  
                elif response.status_code == 400:
                    console.print(f"⚠️ [yellow]Faucet gagal untuk {wallet['address']} - Status Code: 400, Mengulang...[/yellow]")
                    console.print(f"ℹ️ [cyan]Response: {response.text}[/cyan]")
                    time.sleep(5)  
                else:
                    console.print(f"⚠️ [yellow]Faucet gagal untuk {wallet['address']} - Status Code: {response.status_code}[/yellow]")
                    console.print(f"ℹ️ [cyan]Response: {response.text}[/cyan]")
                    time.sleep(10) 
            except Exception as e:
                console.print(f"🚨 [red]Error klaim faucet untuk {wallet['address']}: {e}[/red]")
                time.sleep(10) 

def claim_reward(wallets, web3, contract):
    for wallet in wallets:
        try:
            account = web3.eth.account.from_key(wallet["private_key"])
            sender_address = account.address

            genesis_claimed = contract.functions.userGenesisClaimStatus(sender_address).call()
            current_epoch = contract.functions.currentEpoch().call()
            _, claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()

            if genesis_claimed and not claim_status:
                console.print(f"🟢 [bold green]Claiming reward for {sender_address} (Genesis reward claimed).[/bold green]")
                process_claim(sender_address, wallet["private_key"], web3, contract)
            elif not genesis_claimed:
                console.print(f"🟢 [bold green]Claiming reward for {sender_address} (Genesis reward not claimed).[/bold green]")
                process_claim(sender_address, wallet["private_key"], web3, contract)
            else:
                console.print(f"🟡 [bold yellow]Reward sudah diklaim untuk {sender_address} pada epoch {current_epoch}, skipping.[/bold yellow]")

        except Exception as e:
            console.print(f"🚨 [red]Error klaim reward untuk {wallet['address']}: {e}[/red]")

def process_claim(sender_address, private_key, web3, contract):
    try:
        max_retries = 15  
        retry_count = 0
        gas_price = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(sender_address, 'pending') 

        while retry_count < max_retries:
            try:

                gas_amount = contract.functions.claimReward().estimate_gas({
                    'chainId': web3.eth.chain_id,
                    'from': sender_address,
                    'gasPrice': int(gas_price),  
                    'nonce': nonce
                })

                transaction = contract.functions.claimReward().build_transaction({
                    'chainId': web3.eth.chain_id,
                    'from': sender_address,
                    'gas': gas_amount,
                    'gasPrice': int(gas_price),  
                    'nonce': nonce
                })

                signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                
                console.print(f"✅ [bold green]Transaksi sukses untuk {sender_address} | TX Hash: {web3.to_hex(tx_hash)}[/bold green]")
                return  

            except Exception as e:
                error_message = str(e)

                if "ALREADY_EXISTS: already known" in error_message or "replacement transaction underpriced" in error_message:
                    console.print(f"⚠️ [yellow]Transaksi duplikat terdeteksi. Meningkatkan gas price...[/yellow]")
                    gas_price = int(math.ceil(gas_price * 3.2))  
                    nonce += 1 
                    retry_count += 1
                    time.sleep(5)  
                else:
                    console.print(f"🚨 [red]Error proses klaim untuk {sender_address}: {error_message}[/red]")
                    return 

        console.print(f"❌ [bold red]Gagal mengirim transaksi setelah {max_retries} percobaan untuk {sender_address}.[/bold red]")

    except Exception as e:
        console.print(f"🚨 [red]Gagal mengeksekusi klaim untuk {sender_address}: {str(e)}[/red]")
def main_loop():
    web3 = setup_blockchain_connection()
    contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
    wallets = load_wallets()

    while True:
        claim_faucet(wallets)
        claim_reward(wallets, web3, contract)
        console.print(f"🕒 [cyan]Menunggu 1 menit sebelum proses berikutnya...[/cyan]")
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
