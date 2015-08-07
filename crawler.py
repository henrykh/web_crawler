from Queue import Queue
import threading
from ??? import Download, Parse, Store


LOCK = threading.Lock()
visited_urls = set()


def crawl(url, threads):
    the_queue = Queue(0)

    for n in threads:
        t = threading.Thread(target=download_parse, args=(q,))
        t.daemon = True
        t.start()


def download_parse(the_queue):
    while True:
        #
        LOCK.acquire()
        # grab the next available url from the queue,
        # block until one is available or timeout

        url = the_queue.get(block=True, timeout=5)
        # add the url to the set of
        visited_urls.add(url)
        LOCK.release()
        page = Download(url)
        new_urls = Parse(page)
        for url in new_urls:
            if url not in visited_urls:
                the_queue.add(url)
        store(page)

