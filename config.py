RPC_URL = 'https://rpc.testnet.humanity.org'
REWARD_CONTRACT = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
TOKEN_CONTRACT = '0x693cb8de384f00a5c2580d544b38013bfb496529'
CHAIN_ID = 1942999413

HEADERS = {
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

# 日志配置
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'humanity_claim.log'

# 合约ABI
CONTRACT_ABI = [{"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"bufferSafe","type":"bool"}],"name":"ReferralRewardBuffered","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"enum IRewards.RewardType","name":"rewardType","type":"uint8"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cycleStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vcContract","type":"address"},{"internalType":"address","name":"tkn","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"startTimestamp","type":"uint256"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}] 
