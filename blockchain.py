{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "383eb46f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on all addresses (0.0.0.0)\n",
      " * Running on http://127.0.0.1:5000\n",
      " * Running on http://192.168.0.2:5000\n",
      "Press CTRL+C to quit\n"
     ]
    }
   ],
   "source": [
    "import hashlib\n",
    "import json\n",
    "from time import time\n",
    "from urllib.parse import urlparse\n",
    "from uuid import uuid4\n",
    "from flask import Flask, jsonify, request\n",
    "\n",
    "class Blockchain:\n",
    "    def __init__(self):\n",
    "        self.chain = []\n",
    "        self.current_transactions = []\n",
    "        self.new_block(previous_hash='1', proof=100)\n",
    "\n",
    "    def new_block(self, proof, previous_hash=None):\n",
    "        block = {\n",
    "            'index': len(self.chain) + 1,\n",
    "            'timestamp': time(),\n",
    "            'transactions': self.current_transactions,\n",
    "            'proof': proof,\n",
    "            'previous_hash': previous_hash or self.hash(self.chain[-1]),\n",
    "        }\n",
    "        self.current_transactions = []\n",
    "        self.chain.append(block)\n",
    "        return block\n",
    "\n",
    "    def new_transaction(self, transaction_data):\n",
    "        self.current_transactions.append(transaction_data)\n",
    "        return self.last_block['index'] + 1\n",
    "\n",
    "    @property\n",
    "    def last_block(self):\n",
    "        return self.chain[-1]\n",
    "\n",
    "    @staticmethod\n",
    "    def hash(block):\n",
    "        block_string = json.dumps(block, sort_keys=True).encode()\n",
    "        return hashlib.sha256(block_string).hexdigest()\n",
    "\n",
    "app = Flask(__name__)\n",
    "node_identifier = str(uuid4()).replace('-', '')\n",
    "blockchain = Blockchain()\n",
    "\n",
    "@app.route('/mine', methods=['GET'])\n",
    "def mine():\n",
    "    last_block = blockchain.last_block\n",
    "    last_proof = last_block['proof']\n",
    "    proof = blockchain.proof_of_work(last_proof)\n",
    "\n",
    "    blockchain.new_transaction(\n",
    "        transaction_data={\n",
    "            'sender': \"0\",\n",
    "            'recipient': node_identifier,\n",
    "            'amount': 1,\n",
    "        }\n",
    "    )\n",
    "\n",
    "    previous_hash = blockchain.hash(last_block)\n",
    "    block = blockchain.new_block(proof, previous_hash)\n",
    "\n",
    "    response = {\n",
    "        'message': \"New Block Forged\",\n",
    "        'index': block['index'],\n",
    "        'transactions': block['transactions'],\n",
    "        'proof': block['proof'],\n",
    "        'previous_hash': block['previous_hash'],\n",
    "    }\n",
    "    return jsonify(response), 200\n",
    "\n",
    "@app.route('/transactions/new', methods=['POST'])\n",
    "def new_transaction():\n",
    "    values = request.get_json()\n",
    "    required = ['TransactionNo', 'Date', 'ProductNo', 'ProductName', 'Price', 'Quantity', 'CustomerNo', 'Country']\n",
    "    if not all(k in values for k in required):\n",
    "        return 'Missing values', 400\n",
    "    index = blockchain.new_transaction(values)\n",
    "    response = {'message': f'Transaction will be added to Block {index}'}\n",
    "    return jsonify(response), 201\n",
    "\n",
    "@app.route('/chain', methods=['GET'])\n",
    "def full_chain():\n",
    "    response = {\n",
    "        'chain': blockchain.chain,\n",
    "        'length': len(blockchain.chain),\n",
    "    }\n",
    "    return jsonify(response), 200\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(host='0.0.0.0', port=5000)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9b900220",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
