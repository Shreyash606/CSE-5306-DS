import random
import time

class Participant:
    def __init__(self, name):
        self.name = name

    def vote(self):
        # Simulate participant failure before receiving prepare message
        if random.random() < 0.2:
            print(f"{self.name} failed before receiving prepare message.")
            return "no"

        print(f"{self.name} received prepare message and votes 'yes'.")
        return "yes"

if __name__ == "__main__":
    participant = Participant("Participant1")

    # Simulate participant failure before receiving prepare message
    if random.random() < 0.2:
        print("Participant failed before receiving prepare message.")
    else:
        # Simulate participant recovery
        time.sleep(1)
        print("Participant recovered.")

        # Simulate participant receiving prepare message and voting 'yes'
        vote_message = participant.vote()
        print(f"{participant.name} voted: {vote_message}")
