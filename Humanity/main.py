from web3 import Web3
import json
import asyncio
import logging
from datetime import datetime
import random
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import uuid
from eth_account import Account
from eth_account.messages import encode_defunct

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('humanity_claim.log'),
        logging.StreamHandler()
    ]
)

class HumanityContract:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        self.rpc_url = 'https://rpc.testnet.humanity.org'
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://testnet.humanity.org',
            'referer': 'https://testnet.humanity.org/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        
        self.reward_contract = "0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7"
        self.token_contract = "0x693cb8de384f00a5c2580d544b38013bfb496529"
        self.chain_id = 1942999413
        
        self.session = self.get_session()
        self.w3 = Web3()  
        Account.enable_unaudited_hdwallet_features()

    def get_session(self):
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update(self.headers)
        return session

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            return json.load(f)

    def make_rpc_call(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params
        }
        
        try:
            response = self.session.post(self.rpc_url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"RPC调用失败: {str(e)}")
            return None

    async def check_claim_status(self, wallet_address):
        try:
            
            simulate_claim = self.make_rpc_call("eth_call", [{
                "from": wallet_address,
                "to": self.reward_contract,
                "data": "0x4e71d92d",  
                "gas": "0x493e0"
            }, "latest"])
            
            logging.info(f"模拟调用结果: {simulate_claim}")
            
           
            can_claim_data = f"0x78ffbec7000000000000000000000000{wallet_address[2:]}"
            result = self.make_rpc_call("eth_call", [{"to": self.reward_contract, "data": can_claim_data}, "latest"])
            
            
            kyc_data = f"0x5c622a0e000000000000000000000000{wallet_address[2:]}" 
            kyc_result = self.make_rpc_call("eth_call", [{"to": self.reward_contract, "data": kyc_data}, "latest"])
            
       
            daily_limit_data = "0x8fc0583f"  
            daily_limit_result = self.make_rpc_call("eth_call", [{"to": self.reward_contract, "data": daily_limit_data}, "latest"])
            
            
            last_claim_data = f"0x386e0a3a000000000000000000000000{wallet_address[2:]}"  
            last_claim_result = self.make_rpc_call("eth_call", [{"to": self.reward_contract, "data": last_claim_data}, "latest"])
            
            
            claimed_today_data = f"0x8b7afe2a000000000000000000000000{wallet_address[2:]}"  
            claimed_today_result = self.make_rpc_call("eth_call", [{"to": self.reward_contract, "data": claimed_today_data}, "latest"])
            
            
            claimable_amount_data = f"0x78ffbec7000000000000000000000000{wallet_address[2:]}"  
            claimable_amount_result = self.make_rpc_call("eth_call", [{"to": self.reward_contract, "data": claimable_amount_data}, "latest"])

            logging.info(f"账号 {wallet_address} 状态检查:")
            
            if kyc_result and 'result' in kyc_result:
                is_kyc = int(kyc_result['result'], 16) > 0
                logging.info(f"KYC状态: {'已完成' if is_kyc else '未完成'}")
            
            if daily_limit_result and 'result' in daily_limit_result:
                daily_limit = int(daily_limit_result['result'], 16)
                logging.info(f"每日限额: {daily_limit / 1e18} tokens")
            
            if last_claim_result and 'result' in last_claim_result:
                last_claim_time = int(last_claim_result['result'], 16)
                if last_claim_time > 0:
                    last_claim_datetime = datetime.fromtimestamp(last_claim_time)
                    logging.info(f"上次领取时间: {last_claim_datetime}")
                else:
                    logging.info("还未领取过")
            
            if claimed_today_result and 'result' in claimed_today_result:
                claimed_today = int(claimed_today_result['result'], 16)
                logging.info(f"今日已领取: {claimed_today / 1e18} tokens")
            
            if claimable_amount_result and 'result' in claimable_amount_result:
                claimable_amount = int(claimable_amount_result['result'], 16)
                logging.info(f"可领取数量: {claimable_amount / 1e18} tokens")
            
            if result and 'result' in result:
                can_claim = int(result['result'], 16) > 0
                logging.info(f"是否可领取: {can_claim}")
                
                if can_claim:
                    next_claim_time = int(time.time()) + 24 * 3600
                else:
                    
                    next_claim_data = f"0x8ae9c05b000000000000000000000000{wallet_address[2:]}"
                    next_claim_result = self.make_rpc_call("eth_call", [{"to": self.reward_contract, "data": next_claim_data}, "latest"])
                    
                    if next_claim_result and 'result' in next_claim_result:
                        next_claim_time = int(next_claim_result['result'], 16)
                
                if next_claim_time > 0:
                    next_claim_datetime = datetime.fromtimestamp(next_claim_time)
                    logging.info(f"下次领取时间: {next_claim_datetime}")
                
                return can_claim, next_claim_time
            
            return False, 0
        except Exception as e:
            logging.error(f"检查状态失败 {wallet_address}: {str(e)}")
            return False, 0

    async def claim_rewards(self, account):
        try:
            wallet_address = account['wallet_address']
            private_key = account['private_key']

            logging.info(f"开始为账号 {wallet_address} 领取奖励")

            claim_data = "0xb88a802f"  
            logging.info("准备领取奖励")

            
            nonce_result = self.make_rpc_call("eth_getTransactionCount", [wallet_address, "latest"])
            if not nonce_result:
                return False
            
            nonce = int(nonce_result['result'], 16)
            logging.info(f"当前nonce: {nonce}")
            
           
            transaction = {
                "nonce": nonce,
                "gasPrice": 0,
                "gas": 500000,  
                "to": self.reward_contract,
                "value": 0,
                "data": claim_data,
                "chainId": 1942999413
            }

            logging.info(f"交易详情: {transaction}")
            
            
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
            
           
            acct = Account.from_key(private_key)
            signed = acct.sign_transaction(transaction)
            raw_tx = "0x" + signed.raw_transaction.hex()
            
            logging.info(f"已签名交易: {raw_tx}")
            
            
            result = self.make_rpc_call("eth_sendRawTransaction", [raw_tx])
            
            if result and 'result' in result:
                tx_hash = result['result']
                logging.info(f"交易已发送: {tx_hash}")
                
                
                for i in range(30):
                    receipt = self.make_rpc_call("eth_getTransactionReceipt", [tx_hash])
                    if receipt and 'result' in receipt and receipt['result']:
                        logging.info(f"交易回执: {receipt['result']}")
                        if receipt['result']['status'] == '0x1':
                            logging.info(f"账号 {wallet_address} 领取成功!")
                            
                            for log in receipt['result']['logs']:
                                if log['address'].lower() == self.token_contract.lower():
                                    amount = int(log['data'], 16)
                                    logging.info(f"获得代币数量: {amount / 1e18}")
                            return True
                        else:
                            logging.error(f"交易失败: {tx_hash}")
                            return False
                    logging.info(f"等待交易确认，尝试次数: {i+1}/30")
                    await asyncio.sleep(2)
                
                logging.error("交易确认超时")
                return False
            else:
                if 'error' in result:
                    logging.error(f"发送交易失败: {result['error']}")
                else:
                    logging.error("发送交易失败")
                return False

        except Exception as e:
            logging.error(f"领取失败 {wallet_address}: {str(e)}")
            logging.error("错误详情:", exc_info=True)
            return False

    async def process_account(self, account):
        try:
            await self.claim_rewards(account)
        except Exception as e:
            logging.error(f"处理账号错误 {account['wallet_address']}: {str(e)}")

    async def run_all_accounts(self):
        tasks = [self.process_account(account) for account in self.config['accounts']]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def run_forever(self):
        while True:
            try:
                await self.run_all_accounts()
                wait_time = random.randint(3600, 4500)
                logging.info(f"等待 {wait_time} 秒后进行下一轮检查")
                await asyncio.sleep(wait_time)
            except Exception as e:
                logging.error(f"运行出错: {str(e)}")
                await asyncio.sleep(300)

if __name__ == "__main__":
    contract = HumanityContract()
    asyncio.run(contract.run_forever())
