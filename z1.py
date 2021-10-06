import requests 
from bs4 import BeautifulSoup 
import queue 
from threading import Thread 
 
starting_url = 'https://scrapeme.live/shop/page/1/' 
visited = set() 
max_visits = 100 # careful, it will crawl all the pages 
num_workers = 5 
data = [] 
 
def get_html(url): 
	try: 
		response = requests.get(url) 
		# response = requests.get(url, headers=headers, proxies=proxies) 
		return response.content 
	except Exception as e: 
		print(e) 
		return '' 
 
def extract_links(soup): 
	return [a.get('href') for a in soup.select('a.page-numbers') 
			if a.get('href') not in visited] 
 
def extract_content(soup): 
	for product in soup.select('.product'): 
		data.append({ 
			'id': product.find('a', attrs={'data-product_id': True})['data-product_id'], 
			'name': product.find('h2').text, 
			'price': product.find(class_='amount').text 
		}) 
 
def crawl(url): 
	visited.add(url) 
	print('Crawl: ', url) 
	html = get_html(url) 
	soup = BeautifulSoup(html, 'html.parser') 
	extract_content(soup) 
	links = extract_links(soup) 
	for link in links: 
		if link not in visited: 
			q.put(link) 
 
def queue_worker(i, q): 
	while True: 
		url = q.get() # Get an item from the queue, blocks until one is available 
		if (len(visited) < max_visits and url not in visited): 
			crawl(url) 
		q.task_done() # Notifies the queue that the item has been processed 
 
q = queue.Queue() 
for i in range(num_workers): 
	Thread(target=queue_worker, args=(i, q), daemon=True).start() 
 
q.put(starting_url) 
q.join() # Blocks until all items in the queue are processed and marked as done 
 
print('Done') 
print('Visited:', visited) 
print('Data:', data)