from bs4 import BeautifulSoup
import requests
from Queue import Queue
from threading import Lock, Thread


LOCK = Lock()
visited_urls = set()


def download(url):
    '''Return page body of requested url'''
    r = requests.get(url)
    return r.text


def parse(page):
    '''Extract hrefs from page, return as list'''
    urls = []
    parsed_page = BeautifulSoup(page, 'html.parser')
    for link in parsed_page.find_all('a'):
        urls.append(link.get('href'))
    return urls


def store(page):
    '''Do something with the page... '''
    print page


def crawl(url, threads):
    '''main function to start crawl from given url, with n threads'''

    the_queue = Queue()
    visited_urls.add(url)
    the_queue.put(url)

    # create n worker threads
    for n in xrange(threads):
        t = Worker(the_queue)
        t.daemon = True
        print t.name + " starting"
        t.start()

    # blocks until the queue is empty
    the_queue.join()


# subclassed Thread so that name would be accessible
class Worker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        '''job function for threads to get a url from the queue,
           download, parse, store and add new urls'''

        while True:
            # acquire/release lock
            with LOCK:
                # grab the next available url from the queue,
                # block until one is available or timeout
                url = self.queue.get(block=True, timeout=5)
                # just checking to make sure all threads are working
                print self.name + " " + url

            page = download(url)
            new_urls = parse(page)

            # add parse urls to the queue and the set,
            # if they're not in visited_urls
            for new_url in new_urls:
                if new_url not in visited_urls:
                    visited_urls.add(new_url)
                    self.queue.put(new_url)

            store(page)
            self.queue.task_done()

if __name__ == '__main__':
    crawl(u'http://0.0.0.0:5000/', 4)
