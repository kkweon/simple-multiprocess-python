#-*- encoding: utf-8 -*-
from __future__ import print_function
from multiprocessing import Pool
import bs4
import requests
import time
from urlparse import urljoin




def timeit(func):
    def func_wrapper(*args, **kwargs):
        tic = time.time()
        result = func(*args, **kwargs)
        toc = time.time()
        print("{} seconds".format(toc-tic))
        return result
    return func_wrapper



def get_information(URL):
    req = requests.get(URL).text
    html = bs4.BeautifulSoup(req, 'html.parser')
    em_list = html.find("p", {"class": "no_today"})
    today_price = em_list.find("span", {"class": "blind"}).get_text().replace(",", "")
    today_price = float(today_price)

    return today_price

@timeit
def main_async(no_of_process):
    pool = Pool(processes=no_of_process)
    link_list = get_top_10()
    result = pool.map_async(get_information, link_list)
    return result.get()

@timeit
def main_sync():
    link_list = get_top_10()

    stock_today_price_list = []
    for i, idx in enumerate(link_list):
        price = get_information(idx)
        stock_today_price_list.append(price)

    return stock_today_price_list





def get_top_10():
    URL = "http://finance.naver.com/sise/"
    req = requests.get(URL).text
    html = bs4.BeautifulSoup(req, 'html.parser')
    ul_list = html.find("ul", {"id": "popularItemList"})
    href_list = ul_list.find_all('a', href=True)
    link_list = [urljoin(URL,  x['href']) for x in href_list]

    return link_list


if __name__ == '__main__':
    number_of_processes = 10
    print("{} processes".format(number_of_processes))
    result = main_async(number_of_processes)
    print(result)

    time.sleep(5)
    print("\n\nsingle processe")
    result = main_sync()
    print(result)


