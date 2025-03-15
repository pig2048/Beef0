from web3 import Web3
from colorama import init, Fore, Style
import json
import asyncio
import logging
import time
import random
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from eth_account import Account
from eth_account.messages import encode_defunct
import sys
from datetime import datetime
import math

from config import (
    RPC_URL, REWARD_CONTRACT, TOKEN_CONTRACT, CHAIN_ID,
    HEADERS, LOG_FORMAT, LOG_FILE, CONTRACT_ABI
)

# 初始化colorama
init(autoreset=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class HumanityProtocol:
    def __init__(self):
        self.session = self._get_session()
        self.web3 = Web3(Web3.HTTPProvider(RPC_URL))
        self.contract = self.web3.eth.contract(
            address=Web3.to_checksum_address(REWARD_CONTRACT),
            abi=CONTRACT_ABI
        )
        
        if not self.web3.is_connected():
            logging.error(Fore.RED + "连接失败")
            sys.exit(1)
        logging.info(Fore.GREEN + "已连接到 Humanity Protocol")

    def _get_session(self):
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update(HEADERS)
        return session

    def display_header(self):
        header_text = """
        ===============================
                Humanity Protocol
        Author: https://x.com/snifftunes
        ===============================
        """
        print(Fore.CYAN + Style.BRIGHT + header_text + "\n")

    @staticmethod
    def load_accounts(config_path='config.json'):
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
                return config['accounts']
        except FileNotFoundError:
            logging.error(Fore.RED + f"找不到配置文件: {config_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            logging.error(Fore.RED + f"配置文件格式错误: {config_path}")
            sys.exit(1)
        except KeyError:
            logging.error(Fore.RED + "配置文件缺少accounts字段")
            sys.exit(1)

    def check_claim_status(self, wallet_address):
        try:
            time.sleep(random.uniform(1, 2))  # 添加随机延迟
            
            # 检查Genesis状态
            genesis_claimed = self.contract.functions.userGenesisClaimStatus(wallet_address).call()
            
            time.sleep(random.uniform(1, 2))  # 添加随机延迟
            
            # 获取当前epoch
            current_epoch = self.contract.functions.currentEpoch().call()
            
            time.sleep(random.uniform(1, 2))  # 添加随机延迟
            
            # 检查当前epoch的领取状态
            buffer_amount, claim_status = self.contract.functions.userClaimStatus(
                wallet_address, 
                current_epoch
            ).call()

            logging.info(f"账号 {wallet_address} 状态:")
            logging.info(f"Genesis状态: {'已领取' if genesis_claimed else '未领取'}")
            logging.info(f"当前Epoch: {current_epoch}")
            logging.info(f"Buffer数量: {buffer_amount / 1e18}")
            logging.info(f"领取状态: {'已领取' if claim_status else '未领取'}")

            if genesis_claimed and not claim_status:
                logging.info(Fore.GREEN + f"可以领取奖励 (Genesis已领取)")
                return True
            elif not genesis_claimed:
                logging.info(Fore.GREEN + f"可以领取奖励 (Genesis未领取)")
                return True
            else:
                logging.info(Fore.YELLOW + f"当前Epoch {current_epoch} 已领取，跳过")
                return False

        except Exception as e:
            logging.error(Fore.RED + f"检查状态失败 {wallet_address}: {str(e)}")
            return False

    def claim_rewards(self, account):
        try:
            private_key = account['private_key']
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
                
            wallet_address = account['wallet_address']
            
            can_claim = self.check_claim_status(wallet_address)
            if not can_claim:
                return False

            logging.info(Fore.GREEN + f"开始为账号 {wallet_address} 领取奖励")

            
            max_retries = 15
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    time.sleep(random.uniform(1, 2))  
                    
                    
                    nonce = self.web3.eth.get_transaction_count(wallet_address, 'pending')
                    gas_price = self.web3.eth.gas_price
                    
                    
                    gas_amount = self.contract.functions.claimReward().estimate_gas({
                        'chainId': CHAIN_ID,
                        'from': wallet_address,
                        'gasPrice': int(gas_price),
                        'nonce': nonce
                    })
                    
                    
                    transaction = self.contract.functions.claimReward().build_transaction({
                        'chainId': CHAIN_ID,
                        'from': wallet_address,
                        'gas': gas_amount,
                        'gasPrice': int(gas_price),
                        'nonce': nonce
                    })

                   
                    signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key)
                    tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                    
                    
                    logging.info(f"等待交易确认: {self.web3.to_hex(tx_hash)}")
                    receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
                    
                    if receipt['status'] == 1:
                        logging.info(Fore.GREEN + f"✅ 交易成功: {self.web3.to_hex(tx_hash)}")
                        return True
                    else:
                        logging.error(Fore.RED + f"❌ 交易失败: {self.web3.to_hex(tx_hash)}")
                        return False

                except Exception as e:
                    error_message = str(e)
                    
                   
                    if "ALREADY_EXISTS: already known" in error_message or "replacement transaction underpriced" in error_message:
                        logging.warning(Fore.YELLOW + "⚠️ 交易重复或gas价格过低，增加gas价格重试...")
                        gas_price = int(math.ceil(gas_price * 3.2))  
                        nonce += 1 
                        retry_count += 1
                        time.sleep(5)
                        continue
                    else:
                        logging.error(Fore.RED + f"❌ 领取失败 {wallet_address}: {error_message}")
                        return False

            logging.error(Fore.RED + f"❌ 达到最大重试次数 {max_retries}，交易失败")
            return False

        except Exception as e:
            logging.error(Fore.RED + f"❌ 领取失败 {wallet_address}: {str(e)}")
            return False

    def process_accounts(self):
        accounts = self.load_accounts()
        for account in accounts:
            try:
                self.claim_rewards(account)
                
                time.sleep(random.uniform(3, 5))
            except Exception as e:
                logging.error(f"处理账号错误 {account['wallet_address']}: {str(e)}")
                time.sleep(random.uniform(5, 8))  

    def run_forever(self):
        self.display_header()
        while True:
            try:
                self.process_accounts()
                wait_time = random.randint(21600, 22000)  
                logging.info(Fore.CYAN + f"等待 {wait_time} 秒后进行下一轮...")
                time.sleep(wait_time)
            except Exception as e:
                logging.error(Fore.RED + f"运行出错: {str(e)}")
                time.sleep(300)

if __name__ == "__main__":
    bot = HumanityProtocol()
    bot.run_forever()
