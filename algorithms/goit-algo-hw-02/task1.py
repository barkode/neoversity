from queue import Queue
from uuid import uuid4
import random
import time

# A pool of sample tasks that can be randomly assigned to incoming service requests.
tasks = [
    "Review weekly project budget", "Draft marketing email copy", "Schedule team sync meeting",
    "Update client onboarding deck", "Reply to pending emails", "Submit monthly expense report",
    "Review presentation slides", "Prepare meeting agenda", "Update CRM pipeline",
    "Follow up with leads", "Archive old digital files", "Brainstorm product feature ideas",
    "Proofread contract draft", "Renew software subscriptions", "Outline quarterly goals",
    "Schedule performance reviews", "Optimise website landing page", "Research competitor pricing",
    "Organise shared Google Drive", "Write weekly status report",
    "Buy groceries for the week", "Prep Sunday meal lunches", "Clean kitchen counters",
    "Run a washing machine load", "Vacuum living room rug", "Water indoor house plants",
    "Empty all rubbish bins", "Organise bedroom wardrobe", "Clean bathroom mirror",
    "Wipe down refrigerator shelves", "Take out recycling bins", "Change bed sheets",
    "Wash dirty dishes", "Mop hallway floors", "Dust living room shelves",
    "Mow the front lawn", "Clean the microwave interior", "Restock pantry essentials",
    "Sort incoming post", "Fix leaking bathroom tap",
    "Pay monthly electricity bill", "Check credit card statement", "Transfer money to savings",
    "Review investment portfolio", "Cancel unused subscriptions", "Update personal budget spreadsheet",
    "File quarterly tax documents", "Renew driving licence online", "Scan important paper receipts",
    "Ring the insurance agent",
    "Schedule annual dental check-up", "Refill daily prescription medications", "Complete 30-minute morning workout",
    "Meditate for ten minutes", "Drink eight glasses of water", "Prep healthy evening snacks",
    "Schedule therapy session", "Go for an evening walk", "Stretch for fifteen minutes",
    "Restock first aid kit",
    "Pick up dry cleaning", "Buy a birthday gift for a friend", "Drop off Amazon return",
    "Get car oil changed", "Buy new running shoes", "Fill up the petrol tank",
    "Visit local post office", "Pick up prescription refills", "Buy household cleaning supplies",
    "Return borrowed library books",
    "Back up laptop hard drive", "Clear desktop clutter", "Update phone operating system",
    "Change weak digital passwords", "Unsubscribe from junk newsletters", "Clean laptop keyboard exterior",
    "Organise phone photo gallery", "Delete unused mobile apps", "Empty email spam folder",
    "Set up two-factor authentication",
    "Read twenty pages of a book", "Practise Spanish on Duolingo", "Watch an educational tutorial video",
    "Listen to an industry podcast", "Write a daily journal entry", "Plan a weekend getaway itinerary",
    "Ring a close friend", "Book concert tickets online", "Research local cookery classes",
    "Update professional CV",
    "Feed the dog", "Clean the cat litter tray", "Pack travel suitcase early",
    "Order new business cards", "Donate old clothes", "Assemble new office chair",
    "Hang living room artwork", "Wash the car exterior", "Check smoke alarm batteries",
    "Plan next week's schedule"
    ]

queue = Queue()


def generate_request():
    """Randomly selects a task, creates a new request with a unique ID, and adds it to the queue."""
    request = {
        "id": str(uuid4())[:8],
        "task": random.choice(tasks),
        }
    queue.put(request)
    print(f"Request #{request['id']} created — {request['task']}. Added to the queue.")


def process_request():
    """Retrieves and processes the next request from the front of the queue."""
    if not queue.empty():
        request = queue.get()
        print(f"Processing request #{request['id']} — {request['task']}.")
        queue.task_done()
    else:
        print("The queue is empty. Waiting for new requests...")
        time.sleep(1)


def show_tasks():
    """Displays all requests currently waiting in the queue without removing them."""
    print("--- Current queue ---")
    if queue.empty():
        print("  (queue is empty)")
    else:
        for q in queue.queue:
            print(f"  #{q['id']} — {q['task']}")
    print("---------------------")


def main():
    """Entry point: runs the interactive command loop for the service centre simulation."""

    # Map user-typed commands to their corresponding functions
    commands = {
        "add": generate_request,
        "get": process_request,
        "show": show_tasks,
        }

    print("Service request system started.")
    print("Commands: 'add' — add a request | 'get' — process a request | 'show' — view queue | 'exit' — quit")
    print("Press Enter to add and immediately process a random request.\n")

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            print("Exiting the service request system. Goodbye!")
            break
        elif command == "":
            # Default action: add a new request and immediately process it
            print("Adding a random request to the queue...")
            generate_request()
            print(f"Requests remaining in queue: {queue.qsize()}\n")
        elif command in commands:
            commands[command]()
        else:
            print(f"Unknown command: '{command}'. Please try again.")


if __name__ == "__main__":
    main()
