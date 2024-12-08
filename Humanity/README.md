# Humanity Testnet 自动领取脚本

这是一个用于自动在 Humanity Testnet 上领取代币的 Python 脚本。

## 功能特点

- 自动检查钱包地址的领取资格
- 自动执行代币领取操作
- 支持多钱包批量操作

## 使用前准备

1. 确保已安装 Python 3.X 或更高版本
2. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 准备配置文件 `config.json`，格式如下：
   ```json
   {
     "wallets": [
       {
         "private_key": "你的私钥",
         "address": "钱包地址",
         "proxy": "你的代理"
       }
     ]
   }
   ```

## 使用说明

1. 配置文件设置:
   - 将您的钱包私钥和地址添加到 `config.json` 文件中
   - 确保私钥格式正确（需要包含0x前缀）

2. 运行脚本:

   ```bash
   python -m venv venv
   ./venv/Scripts/activate
   python main.py
   ```

3. 查看运行日志:
   - 程序运行日志将保存在 `humanity_claim.log` 文件中
   - 同时也会在控制台显示运行状态

## 注意事项

- 每个钱包每天只能领取一次
- 请妥善保管您的私钥，不要泄露给他人
