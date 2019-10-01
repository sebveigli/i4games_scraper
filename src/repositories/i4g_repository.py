import pandas as pd
import json
import requests
import time as t

from bs4 import BeautifulSoup

BANNED_PLAYERS_MAP = {
    '10481': 'Surfacing',
    '10585': 'RsK',
    '10968': 'marek',
    '11023': 'Tristan9595',
    '11339': 'ir0n',
    '12145': 'nitrouz',
    '13644': 'madmaz',
    '13800': 'Hikaru',
    '13996': 'CaptainCool',
    '14086': 'Xhae',
    '14488': 'nix',
    '1501': 'ChAiNsAw',
    '15175': 'FlyOrDie',
    '15472': 'boucks',
    '15667': 'hobin',
    '15773': 'Snakehunt3r',
    '15993': 'VRN|d4nk',
    '16016': 'creep-',
    '16313': 'kman',
    '16386': '}ElitE{BoZz',
    '1893': 'infected',
    '19383': 'tuF.~',
    '19445': 'dom',
    '20022': 'sKyrO*',
    '20910': 'spyhunter',
    '21309': 'Tecktonik',
    '21395': '[mx]>|(3b0yZz2',
    '22090': '~*Elwen->',
    '22368': 'UnRealMaster',
    '2320': 'Yoda',
    '24339': 'Nikunat.)',
    '24644': 'metanet',
    '24830': 'oC.dEv^',
    '24947': 'isotoxin',
    '25043': 'eternity',
    '25056': '-FoS.Fulcrum-',
    '25176': 'nexi',
    '25427': 'Eyesolid',
    '25747': 'blableble',
    '25762': 'Olek',
    '2612': '-dvN.kvn-',
    '26221': 'HUSKUS(DSI)',
    '26399': 'MorsTuaVitaMea',
    '26563': 'utfan',
    '27017': 'confuser',
    '27030': 'Polly',
    '27050': 'goku',
    '27164': 'newblood',
    '27658': 'Tsee',
    '27673': 'C&C`',
    '27739': 'Sleepless',
    '27786': 'MoMiLii',
    '3269': 'SnOOp',
    '3352': 'Kiji',
    '3414': 'Zeiksnor',
    '4128': 'Signz',
    '5297': 'drako\'db',
    '5433': 'purr!!',
    '5918': 'teleport',
    '6176': 'leltee',
    '683': 'fighter',
    '7576': 'Blue-Ice',
    '8528': '-uV-Squid^-',
    '8608': '5ive',
    '8700': 'HyPer][',
    '9138': 'appolon',
    '9326': 'N.E.R.D.',
    '9506': 'KnoW',
}


class i4gRepository:
    def __init__(self, user):
        self.user = str(user)

    @staticmethod
    def get_most_recent_user():
        data = None

        while not data:
            try:
                data = requests.get('http://www.i4games.eu/forum/')
            except:
                print('Error trying to get most recent user, sleeping 15 seconds')
                t.sleep(15)
                continue

            soup = BeautifulSoup(data.text, features='html.parser')

            return int(soup.find('td', class_='row1', align='left').find('a')['href'][-5:])

    def get_all_records(self):
        cert = self.get_certified_records()
        best = self.get_best_records()

        for b in best:
            if b not in cert:
                cert.append(b)

        return cert

    def get_certified_records(self):
        '''
        This will only work if the users' certified records are globally visible.

        This seeems to be an manually triggered feature when a user has at least X certified records.
        '''
        certfied_records_url = f'http://www.i4games.eu/btrecords.php?user={self.user}' + \
            '&certified=1&personal=1&page={page}'

        return self._get_records(certfied_records_url)

    def get_best_records(self):
        non_certified_records_url = f'http://www.i4games.eu/btrecords.php?user={self.user}' + \
            '&certified=0&personal=1&page={page}'

        return self._get_records(non_certified_records_url)

    def _get_records(self, url):
        records = []

        page_counter = 0

        while True:
            try:
                data = requests.get(url.format(page=page_counter))
            except:
                print('Error occurred fetching, trying again in 15 seconds...')
                t.sleep(15)
                continue

            soup = BeautifulSoup(data.text, features='html.parser')

            row1_results = soup.findAll('tr', class_='row1')
            row2_results = soup.findAll('tr', class_='row2')

            rows = row1_results + row2_results

            if len(rows) == 0:
                break

            for row in rows:
                attrs = row.find_all()

                date, year = self._get_date_and_year(attrs)
                user, banned = self._get_user(row)
                _map = self._get_map_name(row)
                time = self._get_time_seconds(row)
                certified = self._get_certified(row)
                rating = self._get_rating(row)

                records.append(dict(date=date, year=int(year), user=user, map=_map, user_id=int(self.user),
                                    time=float(time), certified=int(certified), rating=int(rating), banned=int(banned)))

            page_counter += 1

        return records

    def _get_date_and_year(self, attrs):
        if ',' in attrs[0].get_text():
            date = attrs[0].get_text()[:-6]
            year = attrs[0].get_text()[-4:]
        else:
            date = attrs[0].get_text()
            year = 2019

        return date, year

    def _get_user(self, row):
        name = row.find_all('a')[-1].get_text()
        banned = 0

        if name == '':
            banned = 1

            if self.user in BANNED_PLAYERS_MAP:
                name = BANNED_PLAYERS_MAP[self.user]
            else:
                name = 'unknown_banned_user->{}'.format(self.user)

        return name, banned

    def _get_map_name(self, row):
        return row.find('a').get_text()[1:]

    def _get_time_seconds(self, row):
        if ':' in row.find('td', align='right').get_text():
            return str((int(row.find('td', align='right').get_text()[:2]) * 60) + int(row.find('td', align='right').get_text()[3:5])) + row.find('td', align='right').get_text()[-4:]
        else:
            return row.find('td', align='right').get_text()

    def _get_certified(self, row):
        return 1 if row.find('td', align='right').find('b') else 0

    def _get_rating(self, row):
        if row.find('small') and 'Rating' in row.find('small').get_text():
            return row.find('small').get_text().replace('Rating: ', '')
        else:
            return -1
