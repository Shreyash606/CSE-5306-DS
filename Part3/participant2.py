import random
import time
import logging
import socket

logging.basicConfig(filename='participant2.log', level=logging.INFO)

class Participant:
    def __init__(self, name):
        self.name = name

    def vote(self, coordinator_socket):
        # Simulate participant failure before receiving prepare message
        if random.random() < 0.2:
            logging.info(f"{self.name} failed before receiving prepare message.")
            return "no"

        logging.info(f"{self.name} received prepare message and votes 'yes'.")
        coordinator_socket.send("yes".encode())

        # Receive commit message from coordinator
        commit_message = coordinator_socket.recv(1024).decode()
        if commit_message == "commit":
            logging.info(f"{self.name} received commit message. Committing the transaction.")
            return "committed"
        else:
            logging.info(f"{self.name} did not receive commit message. Abort!")
            return "aborted"

if __name__ == "__main__":
    participant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    participant_socket.bind(("127.0.0.1", 8081))
    participant_socket.listen()

    coordinator_socket, addr = participant_socket.accept()
    logging.info("Participant2 connected to the coordinator.")

    # Simulate participant recovery
    time.sleep(1)
    logging.info("Participant2 recovered.")

    # Simulate participant receiving prepare message and voting 'yes' or 'no'
    participant = Participant("Participant2")
    vote_message = participant.vote(coordinator_socket)
    logging.info(f"{participant.name} voted: {vote_message}")

    participant_socket.close()
