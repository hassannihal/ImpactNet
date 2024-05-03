
def sleep_random_between(start, end):
    import random
    import time
    
    """
    Pauses the program execution for a random amount of time between start and end seconds.
    
    Parameters:
    - start (float): The minimum amount of time to sleep, in seconds.
    - end (float): The maximum amount of time to sleep, in seconds.
    """
    sleep_time = random.uniform(start, end)
    print(f"Sleeping for {sleep_time:.2f} seconds.")
    time.sleep(sleep_time)