from threading import Condition
from threading import Thread
from threading import current_thread
import time
import random

class ReadWriteLock(object):

	def __init__(self):
		self.readers_cnt = 0
		self.writer_in_progress = False
		self.cond = Condition()

	def acquireReadLock(self):

		self.cond.acquire()

		while self.writer_in_progress:
			self.cond.wait()

		self.readers_cnt += 1

		self.cond.release()

	def releaseReadLock(self):

		self.cond.acquire()

		self.readers_cnt -= 1

		if self.readers_cnt == 0:
			self.cond.notifyAll()
		self.cond.release()

	def acquireWriteLock(self):

		self.cond.acquire()

		while self.writer_in_progress or self.readers_cnt > 0:
			self.cond.wait()

		self.writer_in_progress = True

		self.cond.release()

	def releaseWriteLock(self):

		self.cond.acquire()

		self.writer_in_progress = False

		self.cond.notifyAll()
		self.cond.release()


def writerThread(lock):
	while 1:
		lock.acquireWriteLock()

		print("{0} writing at {1}".format(current_thread().getName(), time.time()))
		time.sleep(random.randint(1, 5))
		
		print("{0} releasing writelock at {1}".format(current_thread().getName(), time.time()))

		lock.releaseWriteLock()
		time.sleep(1)

def readerThread(lock):
	while 1:
		lock.acquireReadLock()

		print("{0} reading at {1}".format(current_thread().getName(), time.time()))
		time.sleep(random.randint(1, 2))
		
		print("{0} releasing readlock at {1}".format(current_thread().getName(), time.time()))

		lock.releaseReadLock()
		time.sleep(1)

if __name__ == '__main__':

	lock = ReadWriteLock()

	writer1 = Thread(target=writerThread, args=(lock,), name="writer-1")
	writer2 = Thread(target=writerThread, args=(lock,), name="writer-2")
	writer1.daemon=True
	writer2.daemon=True

	writer1.start()

	readers = list()
	for i in range(0, 3):
		t = Thread(target=readerThread, args=(lock, ), name="reader-"+str(i))
		t.daemon=True
		readers.append(t)
	for reader in readers:
		reader.start()

	writer2.start()

	time.sleep(15)