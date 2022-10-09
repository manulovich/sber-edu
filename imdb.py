import re
import requests
from bs4 import BeautifulSoup


def exec_year(str_line: str) -> str:
    match = re.search(f'\((\d+)\)', str_line)

    return '0' if match is None else match.group(1)


def get_info_by_id(id: str):
    url_main_info = f'https://www.imdb.com{id}'
    url_rating_info = f'https://www.imdb.com{id}parentalguide'
    soup_main_info = BeautifulSoup(requests.get(url_main_info).text, 'lxml')
    soup_rating_info = BeautifulSoup(requests.get(url_rating_info).text, 'lxml')

    title = soup_main_info.find('div', class_='sc-dae4a1bc-0 gwBsXc')
    year = soup_main_info.find('span', class_='sc-8c396aa2-2 itZqyK')
    imdb_score = soup_main_info.find('span', class_='sc-7ab21ed2-1 jGRxWM')
    rating = soup_rating_info.find('td', class_='ipl-zebra-list__label')

    if (title is None) or (year is None) or (imdb_score is None) or (rating is None):
        return None

    return  {
        'title': title.text.split(': ')[-1],
        'year': year.text,
        'imdb_score': imdb_score.text,
        'rating': rating.text,
        'prequels_and_sequels': list(
            map(
                lambda a: a['href'].split('?')[0],
                soup_main_info.findAll(
                    'a',
                    class_='ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable'
                )
            )
        )
    }


def get_id_by_title_and_year(title: str, year: str):
    url = f'https://www.imdb.com/find?q={title}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    id = None

    for result_text in soup.findAll('td', class_='result_text'):
        if exec_year(result_text.text) == year:
            id = result_text.find('a')['href']

        break

    return id
