import random
import time
import logging
import socket

logging.basicConfig(filename='participant1.log', level=logging.INFO)

class Participant:
    def __init__(self, name):
        self.name = name

    def vote_and_receive_transaction_status(self, coordinator_socket):
        # Simulate participant failure before receiving prepare message
        if random.random() < 0.2:
            logging.info(f"{self.name} failed before receiving prepare message.")
            return "no"

        # Simulate participant receiving prepare message and voting 'yes'
        logging.info(f"{self.name} received prepare message and votes 'yes'.")
        coordinator_socket.send("yes".encode())

        # Receive transaction status message from coordinator
        transaction_status = coordinator_socket.recv(1024).decode()
        if transaction_status == "commit":
            logging.info(f"{self.name} received commit message. Committing the transaction.")
            return "committed"
        else:
            logging.info(f"{self.name} received abort message. Abort!")
            return "aborted"

if __name__ == "__main__":
    participant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    participant_socket.bind(("127.0.0.1", 8080))
    participant_socket.listen()

    coordinator_socket, addr = participant_socket.accept()
    logging.info("Participant1 connected to the coordinator.")

    # Simulate participant recovery
    time.sleep(1)
    logging.info("Participant1 recovered.")

    # Create participant object
    participant1 = Participant("Participant1")

    # Vote and receive transaction status
    status_message = participant1.vote_and_receive_transaction_status(coordinator_socket)
    logging.info(f"{participant1.name} status: {status_message}")

    participant_socket.close()
