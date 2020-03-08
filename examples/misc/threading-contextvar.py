"""THREADING ContextVars
Demonstration of Python ContextVars behaviour on threads
"""

from threading import Thread
from contextvars import ContextVar
from time import sleep
from uuid import uuid4

RequestID = ContextVar("ID of the request")


def _do_sleep(time_to_sleep):
    request_id = RequestID.get()
    print(f"Starting Sleep of {time_to_sleep} seconds - request_id={request_id}")
    sleep(time_to_sleep)
    print(f"Ended Sleep of {time_to_sleep} seconds - request_id={request_id}")


def threadable_function(time_to_sleep, request_id=None):
    if request_id is None:
        request_id = RequestID.get()
    else:
        RequestID.set(request_id)
    
    print(f"Starting thread - sleep={time_to_sleep}; request_id={request_id}")
    _do_sleep(time_to_sleep)
    print(f"Ended thread - sleep={time_to_sleep}; request_id={request_id}")


def main_define_out():
    """Setting the context variable from the function where threads are created WILL NOT set the value inside the threads
    """
    print("Running example: defining request_id OUTSIDE threads")
    threads = list()

    for time_to_sleep in range(3):
        RequestID.set(str(uuid4()))
        thread = Thread(
            target=threadable_function,
            args=[time_to_sleep],
            daemon=True
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main_define_in():
    """The context variables must be set on the main function of each thread
    """
    print("Running example: defining request_id INSIDE threads")
    threads = list()

    for time_to_sleep in range(3):
        request_id = str(uuid4())
        thread = Thread(
            target=threadable_function,
            args=[time_to_sleep, request_id],
            daemon=True
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main_define_out()
    main_define_in()
