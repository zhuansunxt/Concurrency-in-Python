from threading import *
from collections import deque
import time
import random
import sys

# A queue for communication between producer and consumer.
# Producer can enqueue item and consumer can dequeue item from the queue.
# If queue is full, producer will be blocked; if queue is empty, consumer
# will be blocked.
class BlockingQueue:

	# bq = BlockingQueue(N)
	def __init__(self, max_size):
		self.max_size = max_size
		self.curr_size = 0
		self.cond = Condition()
		self.queue = deque([])

	# Put item in the queue.
	def enqueue(self, item):

		# ------ Critical section begins ------
		self.cond.acquire() 	# acquire the lock.

		# If queue is full, wait until it is not full again.
		while self.curr_size == self.max_size:
			self.cond.wait()

		self.queue.append(item)
		self.curr_size += 1

		self.cond.notifyAll()	# notify all blocked threads.
		self.cond.release()		# release the lock.
		# ------ Critical section ends ------

	def dequeue(self):

		# ------ Critical section begins ------
		self.cond.acquire()		# acquire the lock.

		# If queue is empty, wait until it is non-empty again.
		while self.curr_size == 0:
			self.cond.wait()

		res = self.queue.popleft()
		self.curr_size -= 1

		self.cond.notifyAll()	# notify all blocked threads.
		self.cond.release()		# release the lock.
		# ------ Critical section ends ------

		return res

def consumer_thread(q):
	while 1:
		item = q.dequeue()
		sys.stdout.write("\n{0} consumed item {1}".format(current_thread().getName(), item))
		sys.stdout.flush()
		time.sleep(random.randint(1, 3))

def producer_thread(q, val):
    item = val
    while 1:
        q.enqueue(item)
        sys.stdout.write("\n{0} produced item {1}".format(current_thread().getName(), item))
        sys.stdout.flush()
        item += 1
        time.sleep(0.1)		# producer is faster than consumer

if __name__ == "__main__":
    blocking_q = BlockingQueue(5)

    consumerThread1 = Thread(target=consumer_thread, name="consumer-1", args=(blocking_q,))
    consumerThread2 = Thread(target=consumer_thread, name="consumer-2", args=(blocking_q,))
    producerThread1 = Thread(target=producer_thread, name="producer-1", args=(blocking_q, 0))
    producerThread2 = Thread(target=producer_thread, name="producer-2", args=(blocking_q, 100))
    consumerThread1.daemon = True
    consumerThread2.daemon = True
    producerThread1.daemon = True
    producerThread2.daemon = True

    consumerThread1.start()
    consumerThread2.start()
    producerThread1.start()
    producerThread2.start()

    time.sleep(15)

    print("\nMain thread exiting")