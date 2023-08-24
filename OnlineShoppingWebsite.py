from requests import get as reqget
from bs4 import BeautifulSoup
import streamlit as st


def get_url(search_term, page_no):
    return f'https://www.flipkart.com/search?q={search_term}&page={page_no}'


st.title('Online Shopping Website')

search = st.text_input('Press Enter or anywhere outside to Search')

titles = []
prices = []
images = []
links = []

max_pages = 5

if search:
    loadbar = st.progress(0, text='Loading...')

for i in range(1, max_pages + 1):

    code = reqget(get_url(search, i))

    souptemp = BeautifulSoup(code.text, 'html.parser')
    soup = BeautifulSoup(souptemp.prettify(), 'html.parser')

    titles.extend([i.text.strip() for i in soup.find_all('div', class_='_4rR01T')])
    prices.extend([i.text.strip() for i in soup.find_all('div', class_='_30jeq3 _1_WHN1')])
    images.extend([i['src'] for i in soup.find_all('img', class_='_396cs4')])
    links.extend(['https://www.flipkart.com' + i['href'] for i in soup.find_all('a', class_='_1fQZEK')])
    if not titles:
        titles.extend([i['title'] for i in soup.find_all('a', class_='IRpwTa')])
        prices.extend([i.text.strip() for i in soup.find_all('div', class_='_30jeq3')])
        images.extend([i['src'] for i in soup.find_all('img', class_='_2r_T1I')])
        links.extend(['https://www.flipkart.com' + i['href'] for i in soup.find_all('a', class_='IRpwTa')])

    if search:
        loadbar.progress((100//max_pages)*i, text='Loading...')


if search:
    loadbar.progress(100, text='Done')

try:
    cont = [st.container() for i in titles]

    cont[0].divider()

    records = []
    for t, p, l, i in zip(titles, prices, images, links):
        records.append((t, p, l, i))

    for i, r in enumerate(records):
        cont[i].image(r[2])
        cont[i].write(r[0])
        cont[i].write('Price: ' + r[1])
        cont[i].write('Link: ' + r[3] + '\n\n')
        cont[i].divider()

except IndexError:
    st.error('Oops... Looks like we don\'t have anything like that, search something else')

loadbar.progress(100, 'Done!')

search = ''
