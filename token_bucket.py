from threading import *
import random
import time
import sys


# An implementation of token bucket algorithm.
#
# Tokens get filled at the rate of one token per second. A bucket
# can hold up to a max number of tokens. When all tokens are taken
# and there is no refill yet, calling thread will be blocked.
#
# This algorithm is usually used for implementing traffic control
# with rate limitting / quota.
class TokenBucket:

	# tb = TokenBucket(M, R)
	# max_size decides the peak number of tokens can be granted per second
	# rate decides the avg number of tokens can be granted per second
	def __init__(self, max_size, rate=1):
		self.max_size = max_size
		self.token_left = 0
		self.rate = rate
		self.last_req_time = time.time()
		self.lock = Lock()


	# Get a token from the bucket.
	# The API does not return any data: the fact it returns means
	# a token is sucessfully grabbed by the calling thread.
	def get_token(self):
		with self.lock:
			refill = self.rate * int(time.time() - self.last_req_time)
			self.token_left = min(self.max_size, self.token_left + refill)

			if self.token_left == 0:
				time.sleep(1)
				self.token_left = min(self.max_size, self.token_left + self.rate - 1)
			else:
				self.token_left -= 1

			self.last_req_time = time.time()

			sys.stdout.write("\nGranting {0} token at {1} ".format(current_thread().getName(), int(time.time())))

if __name__ == '__main__':
	tb = TokenBucket(10, 3)

	time.sleep(6)

	threads = list()
	for _ in range(0, 30):
		threads.append(Thread(target=tb.get_token))

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()