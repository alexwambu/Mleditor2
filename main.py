from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json, os, time, threading

app = Flask(__name__)

# Load environment configuration
MEMORY_STORAGE_1 = os.getenv("MEMORY_STORAGE_1", "https://storagememory-2-bngo.onrender.com")
MEMORY_STORAGE_2 = os.getenv("MEMORY_STORAGE_2", "https://storagemem.onrender.com")
HEARTBEAT_INTERVAL = 18

# Connect to Ethereum node (infura or local)
RPC_URL = os.getenv("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract template for ERC-20
ERC20_TEMPLATE = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract Token {
    string public name = "{{NAME}}";
    string public symbol = "{{SYMBOL}}";
    uint8 public decimals = 18;
    uint public totalSupply = {{SUPPLY}};
    mapping(address => uint) public balanceOf;
    event Transfer(address indexed from, address indexed to, uint value);
    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }
    function transfer(address to, uint value) public returns (bool) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
}
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/deploy_token", methods=["POST"])
def deploy_token():
    data = request.json
    name = data.get("name", "MyToken")
    symbol = data.get("symbol", "MTK")
    supply = data.get("supply", "1000000") + " * 10**18"

    contract_code = ERC20_TEMPLATE.replace("{{NAME}}", name).replace("{{SYMBOL}}", symbol).replace("{{SUPPLY}}", supply)
    
    # Here we simulate deployment — in production use web3.eth.contract + compile
    fake_address = "0x" + os.urandom(20).hex()
    explorer_link = f"https://etherscan.io/address/{fake_address}"

    return jsonify({
        "contract_address": fake_address,
        "explorer": explorer_link,
        "message": f"Deployed {name} ({symbol}) successfully!"
    })

@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "alive", "timestamp": time.time()})

def keep_alive():
    while True:
        try:
            os.system(f"curl -s {MEMORY_STORAGE_1}/heartbeat > /dev/null 2>&1")
            os.system(f"curl -s {MEMORY_STORAGE_2}/heartbeat > /dev/null 2>&1")
        except Exception as e:
            print("Heartbeat error:", e)
        time.sleep(HEARTBEAT_INTERVAL)

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
