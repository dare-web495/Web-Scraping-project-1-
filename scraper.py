from bs4 import BeautifulSoup
from word2number import w2n
from urllib.parse import urljoin

import requests
import time


def parse_listing(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    book_dict = []
    books = soup.find_all('article', class_="product_pod")

    for book in books:
        title = book.find('h3').find('a')['title']
        price_text = book.find('div', class_='product_price').find('p', class_='price_color').text
        price = float(price_text[1:])
        word_rating = book.find('p')['class'][1]
        rating = w2n.word_to_num(word_rating)
        stock_pos = book.find('div', class_='product_price').find('p', class_='instock availability').text.strip()
        in_stock = "In stock" in stock_pos
        sliced_url = book.find('h3').find('a')['href']
        url = urljoin(page_url, sliced_url)  

        book_dict.append(
            {
                'title': title,
                'price': price,
                'rating': rating,
                'in_stock': in_stock,
                'url': url,
            }
        )

    return book_dict

def parse_detail(html):
    detail_soup = BeautifulSoup(html, "html.parser")
    table = detail_soup.find('table', class_='table table-striped')
    category = detail_soup.select_one('ul.breadcrumb li:nth-of-type(3) a').get_text(strip=True)

    upc = None
    for row in table.find_all('tr'):
        if 'upc' in row.find('th').get_text(strip=True).lower():
            upc = row.find('td').get_text(strip=True)
            break
    
    return {
           'upc': upc,
           'category': category
       }


def scrape_all(page_url):
    session = requests.Session()
    session.headers.update({"User-Agent": "BookScraperPractice/1.0 (learning project)"})
    results = []

    while page_url:
        response = session.get(page_url, timeout=10)
        response.encoding = "utf-8"
        response.raise_for_status()
        html = response.text
        unfinished = parse_listing(html, page_url)

        for book in unfinished:
            html_page = session.get(book['url'], timeout=10)
            html_page.encoding = "utf-8"
            html_page.raise_for_status()
            remaining = parse_detail(html_page.text)
            book.update(remaining)
            time.sleep(0.5)

        results.extend(unfinished)
        page_no = int(len(results)/20)
        print(f"Finished page {page_no}...")
        nxt_url = BeautifulSoup(html, "html.parser").select_one("li.next a")
        if nxt_url:
            page_url = urljoin(page_url, nxt_url["href"])
        else:
            page_url = None

    return results


def main():
    url = "https://books.toscrape.com/"

    final_book_dicts = scrape_all(url)
    print(final_book_dicts)


if __name__ == "__main__":
    main()
   