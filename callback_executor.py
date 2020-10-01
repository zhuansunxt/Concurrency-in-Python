from threading import Condition
from threading import Thread
import random
import time
import sys
import heapq
import math

# A callback executor which can be used to register callback
# with certain exectuion delay.
class CallbackExecutor(object):

	def __init__(self):
		self.callbacks = list()
		self.cond = Condition()
		self.sleep = 0

	def registerCallback(self, callback):
		# ------ Critical section begins ------
		self.cond.acquire()

		execution_ts = time.time() + callback.execute_after
		heapq.heappush(self.callbacks, (execution_ts, callback))

		# notify the executor thread to wake up and examine the current heap
		self.cond.notify()
		self.cond.release()
		# ------ Critical section ends ------

	def start(self):

		while True:
			self.cond.acquire()

			while len(self.callbacks) == 0:
				self.cond.wait()

			while len(self.callbacks) > 0:
				next_callback = self.callbacks[0]
				sleep_period = next_callback[0] - math.floor(time.time())
				
				# break the loop if there is a callback to be executed now.
				if sleep_period <= 0:
					break

				self.cond.wait(timeout=sleep_period)				

			callback = heapq.heappop(self.callbacks)[1]
			callback.action()
			sys.stdout.write("Callback {0}: Executed at {1} : Scheduled at {2}\n".\
							 format(callback.name, time.time(), callback.execute_after))
			sys.stdout.flush()

			self.cond.release()

# An executable callback.
class Callback(object):

	def __init__(self, name, action, execute_after):
		self.name = name
		self.action = action
		self.execute_after = execute_after


def hello_world():
	sys.stdout.write("hello world")


if __name__ == '__main__':
	callback1 = Callback("A", hello_world, 4)
	callback2 = Callback("B", hello_world, 5)
	callback3 = Callback("C", hello_world, 6)
	callback4 = Callback("D", hello_world, 2)

	executor = CallbackExecutor()
	t = Thread(target=executor.start)
	t.daemon = True
	t.start()

	executor.registerCallback(callback1)
	executor.registerCallback(callback2)
	executor.registerCallback(callback3)
	executor.registerCallback(callback4)

	time.sleep(10)
	t.join()