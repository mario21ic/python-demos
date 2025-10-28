import threading

def print_numbers():
    for i in range(10):
        print(i)

# Create a thread object
thread = threading.Thread(target=print_numbers)

# Start the thread
thread.start()

# Optionally, wait for the thread to finish before proceeding
#print("before join")
#thread.join()

# Continue with the rest of your program
print("finish")
