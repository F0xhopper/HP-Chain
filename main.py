import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, sender, receiver, health_change, message, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.health_change = health_change
        self.message = message
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_string = str(self.index) + str(self.timestamp) + str(self.sender) + str(self.receiver) + str(self.health_change) + str(self.message) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis", "Genesis", 0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, sender, receiver, health_change, message):
        latest_block = self.get_latest_block()
        new_block = Block(latest_block.index + 1, date.datetime.now(), sender, receiver, health_change, message, latest_block.hash)
        self.chain.append(new_block)
        return new_block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

class User:
    def __init__(self, public_key):
        self.public_key = public_key
        self.health = 100

class HealthEconomyApp:
    def __init__(self):
        self.blockchain = Blockchain()
        self.users = {}

    def add_user(self, public_key):
        if public_key not in self.users:
            self.users[public_key] = User(public_key)
            print(f"User {public_key} added with 100 health points.")
        else:
            print(f"User {public_key} already exists.")

    def get_user_health(self, public_key):
        if public_key in self.users:
            return self.users[public_key].health
        else:
            return None

    def update_health(self, public_key, health_change):
        if public_key in self.users:
            self.users[public_key].health += health_change
            if self.users[public_key].health <= 0:
                self.users.pop(public_key)
                print(f"User {public_key} has been removed from the network.")
            return True
        return False

    def transfer_health(self, sender, receiver, health_change, message):
        if sender in self.users and receiver in self.users:
            if self.users[sender].health >= health_change:
                self.update_health(sender, -health_change)
                self.update_health(receiver, health_change)
                self.blockchain.add_block(sender, receiver, health_change, message)
                print(f"{health_change} health transferred from {sender} to {receiver}. Message: {message}")
            else:
                print(f"{sender} does not have enough health points.")
        else:
            print("Invalid sender or receiver.")

    def compete(self, user1, user2, stake):
        if user1 in self.users and user2 in self.users:
            if self.users[user1].health >= stake and self.users[user2].health >= stake:
                # For simplicity, let's use random to determine the winner
                import random
                winner = random.choice([user1, user2])
                loser = user1 if winner == user2 else user2

                self.update_health(loser, -stake)
                self.update_health(winner, stake)
                self.blockchain.add_block(loser, winner, -stake, f"Competition: {loser} vs {winner}, Winner: {winner}")

                print(f"Competition: {loser} vs {winner}, Winner: {winner}, Stake: {stake}")
            else:
                print("One or both users do not have enough health points to compete.")
        else:
            print("Invalid competitors.")

    def print_blockchain(self):
        for block in self.blockchain.chain:
            print("Block #" + str(block.index))
            print("Timestamp: " + str(block.timestamp))
            print("Sender: " + block.sender)
            print("Receiver: " + block.receiver)
            print("Health Change: " + str(block.health_change))
            print("Message: " + block.message)
            print("Hash: " + block.hash)
            print("Previous Hash: " + block.previous_hash)
            print("\n")

# Example Usage
if __name__ == "__main__":
    app = HealthEconomyApp()

    # Add users
    app.add_user("AlicePublicKey")
    app.add_user("BobPublicKey")
    app.add_user("CharliePublicKey")

    # Simulate health transfers
    app.transfer_health("AlicePublicKey", "BobPublicKey", 10, "Gift")
    app.transfer_health("BobPublicKey", "CharliePublicKey", 5, "Debt Payment")

    # Simulate a competition
    app.compete("AlicePublicKey", "CharliePublicKey", 15)

    # Print blockchain status
    print("Current Blockchain Status:")
    app.print_blockchain()

    # Print user health status
    print("User Health Status:")
    for user in app.users:
        print(f"{user}: {app.get_user_health(user)} health points")