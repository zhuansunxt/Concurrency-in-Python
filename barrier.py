from threading import *

class Barrier(object):

	def __init__(self, size):
		self.size = size
		self.reached_cnt = 0
		self.released_cnt = 0
		self.cond = Condition()

	def arrived(self):

		# Acquire the lock. Critical section starts.
		self.cond.acquire()

		# When the barrier is at its full size, the thread cannot enter
		# but needs to be blocked.		
		while self.reached_cnt == self.size:
			self.cond.wait()

		self.reached_cnt += 1

		# If the current thread is the last thread that enters the barrier,
		# we need to initiate the release process. Otherwise the thread
		# should be blocked by the condition
		if self.reached_cnt == self.size:
			self.released_cnt = self.reached_cnt
		else:
			while self.reached_cnt < self.size:
				self.cond.wait()

		# Release process starts. A thread is either holding the lock or
		# is awaken from condition wait, so this is also in the critical
		# section.
		self.released_cnt -= 1

		if self.released_cnt == 0:
			self.reached_cnt = 0

		# This notification can wake up two type of thread:
		# 1. Thread that is waiting for exiting the barrier (line 30)
		# 2. Thread that is waiting for entering the barrier (line 19)
		# Code at line 37 and 38 will make sure the first type of thread
		# will all exit the barrier before any second type of thread can
		# enter the barrier.
		self.cond.notifyAll()
		self.cond.release()
