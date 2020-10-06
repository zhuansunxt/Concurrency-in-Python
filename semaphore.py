from threading import Condition
from threading import Thread
import time

class Semaphore(object):

	def __init__(self, count):
		self.count = count
		self.left = count
		self.cond = Condition()

	def acquire(self):
		self.cond.acquire()

		while self.left == 0:
			self.cond.wait()

		self.left -= 1

		self.cond.notifyAll()
		self.cond.release()


	def release(self):
		self.cond.acquire()

		while self.left == self.count:
			self.cond.wait()

		self.left += 1

		self.cond.notifyAll()
		self.cond.release()


if __name__ == '__main__':

	def task_1(s):

		print "acquiring..."
		s.acquire()
		print "acqruired"

		print "acquiring..."
		s.acquire()
		print "acqruired"

		print "acquiring..."
		s.acquire()
		print "acqruired"

	def task_2(s):

	 	time.sleep(2)
	 	print "releasing"
	 	s.release()

	 	time.sleep(2)
	 	print "releasing"
	 	s.release()

	 	time.sleep(2)
	 	print "releasing"
	 	s.release()

	s = Semaphore(1)

	t1 = Thread(target=task_1, args=(s,))
	t2 = Thread(target=task_2, args=(s,))

	t1.start()
	t2.start()

	t1.join()
	t2.join()