import socket
import random
import time
import logging

logging.basicConfig(filename='coordinator.log', level=logging.INFO)

class Coordinator:
    def __init__(self, participants):
        self.participants = participants

    def send_prepare_message(self):
        # Simulate coordinator failure before sending prepare message
        if random.random() < 0.2:
            logging.info("Coordinator failed before sending prepare message.")
            return None

        logging.info("Coordinator sending prepare message.")
        return "prepare"

    def receive_votes(self):
        # Simulate coordinator recovery
        time.sleep(5)  # Simulating recovery time
        logging.info("Coordinator recovered. Sending prepare message again.")

        # Send prepare message again
        prepare_message = self.send_prepare_message()

        # Receive votes from participants
        if prepare_message == "prepare":
            votes = []
            for participant_socket in self.participants:
                vote = participant_socket.recv(1024).decode()
                votes.append(vote)

            return all(vote == "yes" for vote in votes)

    def commit_transaction(self):
        # Store transaction information on disk before sending commit message
        logging.info("Storing transaction information on disk.")
        # Simulate storing transaction information on disk

        # Send commit message to participants
        for participant_socket in self.participants:
            participant_socket.send("commit".encode())
            logging.info("Coordinator sending commit message to a participant.")

if __name__ == "__main__":
    num_participants = int(input("Enter the number of participants: "))
    participants = []

    # Set up sockets for participants
    for i in range(num_participants):
        participant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        participant_socket.connect(("127.0.0.1", 8080 + i))
        participants.append(participant_socket)

    coordinator = Coordinator(participants)

    # Phase 1: Coordinator sends prepare message
    prepare_message = coordinator.send_prepare_message()

    # Phase 2: Coordinator receives votes
    if prepare_message == "prepare":
        all_votes = coordinator.receive_votes()

        if all_votes:
            logging.info("All participants voted 'yes'. Committing the transaction.")
            # Phase 3: Coordinator commits transaction
            coordinator.commit_transaction()
        else:
            logging.info("Abort! Not all participants voted 'yes'.")

    # Close participant sockets
    for participant_socket in participants:
        participant_socket.close()
