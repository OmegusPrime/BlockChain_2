import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions  # List of transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.hash_current()

    def hash_current(self):
        current_data = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(current_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.mempool = []  # Unconfirmed transactions list

    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_to_mempool(self, transaction, fee):
        self.mempool.append({"transaction": transaction, "fee": fee})

    def add_custom_block(self, transactions):
        new_block = Block(len(self.chain), transactions, self.get_latest_block().hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        print(f"\nCustom block {new_block.index} added with transaction(s): {transactions}")

    def mine_transactions(self):
        if not self.mempool:
            print("\nNo transactions to mine.")
            return

        # Sort transactions in the mempool by fee (highest first)
        self.mempool.sort(key=lambda x: x["fee"], reverse=True)

        while self.mempool:
            transactions_to_mine = [tx["transaction"] for tx in self.mempool[:3]]  # Mine up to 3 transactions per block
            new_block = Block(len(self.chain), transactions_to_mine, self.get_latest_block().hash)
            self.proof_of_work(new_block)
            self.chain.append(new_block)
            print(f"\nBlock {new_block.index} mined with transaction(s): {transactions_to_mine}")
            self.mempool = self.mempool[3:]  # Remove mined transactions

    def proof_of_work(self, block):
        block.nonce = 0
        target = '0' * self.difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.hash_current()

    def display_mempool(self):
        print("\nCurrent Mempool:")
        for i, tx in enumerate(self.mempool, 1):
            print(f"{i}. Transaction: {tx['transaction']}, Fee: {tx['fee']}")

    def display_chain(self):
        print("\nBlockchain:")
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Transactions: {block.transactions}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Hash: {block.hash}")
            print(f"  Nonce: {block.nonce}")
            print("-------------------------")

def add_custom_block(blockchain):
    print("\n--- Add a Custom Block ---")
    transactions = []
    while True:
        tx = input("Enter a transaction (or 'done' to finish): ")
        if tx.lower() == 'done':
            break
        transactions.append(tx)
    if transactions:
        blockchain.add_custom_block(transactions)
    else:
        print("No transactions entered. Block not added.")

def main():
    blockchain_instance = Blockchain()
    while True:
        print("\n1. Simulate Transaction Pinning Attack")
        print("2. Add a Custom Block")
        print("3. View Blockchain")
        print("4. Mine Pending Transactions")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            simulate_pinning_attack(blockchain_instance)
        elif choice == '2':
            add_custom_block(blockchain_instance)
        elif choice == '3':
            blockchain_instance.display_chain()
        elif choice == '4':
            blockchain_instance.mine_transactions()
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")

def simulate_pinning_attack(blockchain):
    print("\n--- Simulating Transaction Pinning Attack ---")
    
    # Custom input for transactions and fees
    high_fee_tx = input("Enter the high-fee transaction (legitimate): ")
    high_fee = int(input("Enter the fee for this transaction: "))

    low_fee_tx = input("Enter the low-fee transaction (attacker's pinning transaction): ")
    low_fee = int(input("Enter the fee for the pinning transaction: "))

    # Add transactions to mempool
    blockchain.add_to_mempool(high_fee_tx, high_fee)
    blockchain.add_to_mempool(low_fee_tx, low_fee)
    
    # Display mempool status
    blockchain.display_mempool()

    # Simulate mining
    print("\nAttempting to mine transactions...")
    blockchain.mine_transactions()

    # Display remaining mempool state
    blockchain.display_mempool()

if __name__ == "__main__":
    main()
