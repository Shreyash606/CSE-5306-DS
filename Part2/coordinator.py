import socket
import random
import time
import logging

logging.basicConfig(filename='coordinator_part2.log', level=logging.INFO)

class Coordinator:
    def __init__(self, participants):
        self.participants = participants

    def send_prepare_messages(self):
        # Simulate coordinator failure before sending prepare message
        if random.random() < 0.2:
            logging.info("Coordinator failed before sending prepare message.")
            return None

        logging.info("Coordinator sending prepare message.")
        return "prepare"

    def receive_votes(self, participant_sockets):
        # Simulate coordinator recovery
        time.sleep(5)  # Simulating recovery time
        logging.info("Coordinator recovered. Sending prepare message again.")

        # Send prepare message again
        prepare_message = self.send_prepare_messages()

        # Receive votes from participants
        if prepare_message == "prepare":
            votes = []
            for participant_socket in participant_sockets:
                vote = participant_socket.recv(1024).decode()
                votes.append(vote)

            if "yes" not in votes:
                logging.info("Coordinator received 'no' vote from at least one participant. Aborting transaction.")
                self.send_abort_messages(participant_sockets)  # Send abort messages
                return False

            return True

    def send_abort_messages(self, participant_sockets):
        for participant_socket in participant_sockets:
            participant_socket.send("abort".encode())
            logging.info("Coordinator sent 'abort' message to participant.")

if __name__ == "__main__":
    num_participants = int(input("Enter the number of participants: "))
    participants = []

    # Set up sockets for participants
    for i in range(num_participants):
        participant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        participant_socket.connect(("127.0.0.1", 8080 + i))
        participants.append(participant_socket)

    coordinator = Coordinator(participants)

    # Phase 1: Coordinator sends prepare messages
    prepare_message = coordinator.send_prepare_messages()

    # Phase 2: Coordinator receives votes
    if prepare_message == "prepare":
        all_votes = coordinator.receive_votes(participants)

        if all_votes:
            logging.info("All votes received: Yes. Committing the transaction.")
        else:
            logging.info("Abort! Not all participants voted 'yes'.")

    # Close participant sockets
    for participant_socket in participants:
        participant_socket.close()
