import requests
import json
import pandas as pd
import httpx
from selectolax.parser import HTMLParser



def toronto_fugitive_profiles_list():
    """
    Extract records.
    """

    profile_links = set()
    for i in range(1, 5):
        url = f'https://www.tps.ca/organizational-chart/specialized-operations-command/detective-operations/investigative-services/homicide/most-wanted/?page={i}'
        response = httpx.get(url)
        html = HTMLParser(response.text)

        # Base case
        current_page_number = html.css_first('div.pagination li.active').text()
        if int(current_page_number) != i:
            break

        # Extract fugitive profile links
        links = html.css('article.suspect a')
        for link in links:
            profile_links.add(link.attributes['href'])

    return profile_links

def toronto_fugitive_profile_extract():
    """
    Extract data from records.
    """
    profile_links = toronto_fugitive_profiles_list()
    link = list(profile_links)
    url = f'https://www.tps.ca{link[2]}'
    print(url)
    response = httpx.get(url)
    html = HTMLParser(response.text)

    # Extract
    name = html.css_first('div.people-content h1').text()
    print(name)
    info_block = html.css('div.meta p')

    charge = info_block[0].text().strip()
    print(charge)

    profile_content = html.css('div.people-content p')
    # print(profile_content)
    print(profile_content[3].text().strip())
    print(profile_content[4].text().strip())
    # print(profile_content[2].text().strip())
    print('\n')

    for link in profile_links:
        url = f'https://www.tps.ca{link}'
        print(url)
        response = httpx.get(url)
        html = HTMLParser(response.text)

        # Extract
        name = html.css_first('div.people-content h1').text()
        print(name)
        info_block = html.css('div.meta p')

        charge = info_block[0].text().strip()
        print(charge)

        profile_content = html.css('div.people-content p')
        # print(profile_content)
        print(profile_content[3].text().strip())
        # print(profile_content[3].text().strip())
        # print(profile_content[2].text().strip())
        print('\n')

        # #######################################################
        # 'name'
        # 'aliases': fbi_data_pd['items'][i]['aliases'],
        # 'sex': fbi_data_pd['items'][i]['sex'],
        # 'weight': fbi_data_pd['items'][i]['weight'],
        # 'eyes': fbi_data_pd['items'][i]['eyes'],
        # 'hair': fbi_data_pd['items'][i]['hair'],
        # 'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
        # 'nationality': fbi_data_pd['items'][i]['nationality'],
        # 'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
        # 'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
        # 'charges': fbi_data_pd['items'][i]['subjects'],
        # 'wanted_by': 'FBI',
        # 'status': fbi_data_pd['items'][i]['status'],
        # 'publication': fbi_data_pd['items'][i]['publication'],
        # 'last_modified': fbi_data_pd['items'][i]['modified'],
        # 'reward': fbi_data_pd['items'][i]['reward_max'],
        # 'details': fbi_data_pd['items'][i]['details'],
        # 'caution': fbi_data_pd['items'][i]['caution'],
        # 'warning': fbi_data_pd['items'][i]['warning_message'],
        # 'images': '',
        # 'link': fbi_data_pd['items'][i]['url'],



class Scraper:
    def __init__(self):
        self.compiled_fugitive_list = []

    def rcmp_fugitive_profile_list(self):
        fugitive_profile_links = set()
        URL = 'https://www.rcmp-grc.gc.ca/en/wanted'
        response = httpx.get(URL)
        html = HTMLParser(response.text)

        profile_link = html.css('a.text-neutral')
        for link in profile_link:
            fugitive_profile_links.add(link.attributes['href'])

        return fugitive_profile_links

    def scrape_rcmp_fugitive_profiles(self):
        print('Extracting RCMP Fugitives...')
        fugitive_profile_extracts = []
        fugitive_profiles = self.rcmp_fugitive_profile_list()
        for profile in fugitive_profiles:
            URL = f'https://www.rcmp-grc.gc.ca/en/{profile}'
            # print(URL)
            response = httpx.get(URL)
            html = HTMLParser(response.text)

            # Extracts
            name = html.css_first('h1.page-header')
            status = html.css_first('p.mrgn-bttm-md').text()
            charges = html.css('ul.list-group li.list-group-item') # list of charges
            last_modified = html.css_first('time')
            description = html.css('div.col-md-9 p') # description[1].text()
            details = description[1].text()
            details_cleaned = details.replace('\xa0', ' ')
            image = html.css_first('img.img-responsive').attributes['src']
            image = 'https://www.rcmp-grc.gc.ca' + image
            # To determine the value associtaed with the extracted list, split the sentence into
            # words, and assign the value to the right variable with the first word
            personal_details = html.css('ul.list-unstyled li')
            alias = ''
            sex = ''
            date_of_birth = ''
            place_of_birth = ''
            eyes = ''
            hair = ''
            height = ''
            weight = ''
            scars = ''
            for detail_list in personal_details:
                details = detail_list.text().split()
                if details[0] == 'Aliases:':
                    alias = details[1:]
                elif details[0] == 'Sex:':
                    sex = details[1:]
                elif details[0] == 'Born:':
                    date_of_birth = details[1:]
                elif details[0] == 'Place':
                    place_of_birth = details[3:]
                elif details[0] == 'Eye':
                    eyes = details[2:]
                elif details[0] == 'Hair':
                    hair = details[2:]
                elif details[0] == 'Height:':
                    height = details[1:]
                elif details[0] == 'Weight:':
                    weight = details[1:]
                elif details[0] == 'Tattoos:':
                    pass
                elif details[0] == 'Scars:':
                    scars = details[1:]
            # Restructure sentence
            profile_values = [alias, sex, date_of_birth, place_of_birth, eyes, hair, height, weight, scars]
            profile_values = [ ''.join(text) if index == 6 or index == 7 else ' '.join(text) for index, text in enumerate(profile_values) ]

            profile = {
                'name': name.text(),
                'alias': profile_values[0],
                'sex': profile_values[1],
                'height': profile_values[6],
                'weight': profile_values[7],
                'eyes': profile_values[4],
                'hair': profile_values[5],
                'distinguishing_marks': '',
                'nationality': '',
                'date_of_birth': profile_values[2],
                'place_of_birth': profile_values[3],
                'charges': [ charge.text() for charge in charges ],
                'wanted_by': 'RCMP',
                'status': status,
                'publication': '',
                'last_modified': last_modified.text(),
                'reward': '',
                'details': details_cleaned,
                'caution': '',
                'remarks': '',
                'images': image,
                'link': URL,
            }
            fugitive_profile_extracts.append(profile)

        for profile in fugitive_profile_extracts:
            self.compiled_fugitive_list.append(list(profile.values()))

    def scrape_fbi_fugitive_profiles(self):
        """
        Implements api pagination.
        """
        print('Extracting FBI Fugitives...')
        fugitive_profile_extracts = []
        page = 1
        while True:
            response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
            print(response)
            fbi_data = response.json()
            # fbi_data = json.loads(response.content)
            fbi_data_pd = pd.DataFrame.from_dict(fbi_data)

            # Base case
            if len(fugitive_profile_extracts) == fbi_data['total']:
                break

            for i in range(0, len(fbi_data_pd['items'])):
                age = ''
                if fbi_data_pd['items'][i]['age_min']:
                    age = str(fbi_data_pd['items'][i]['age_min']) + '-' + str(fbi_data_pd['items'][i]['age_max'])
                else:
                    age = str(fbi_data_pd['items'][i]['age_max'])

                height = ''
                if fbi_data_pd['items'][i]['height_min']:
                    height = str(fbi_data_pd['items'][i]['height_min']) + '-' + str(fbi_data_pd['items'][i]['height_max'])
                else:
                    height = str(fbi_data_pd['items'][i]['height_max'])
                profile = {
                    'name': fbi_data_pd['items'][i]['title'],
                    'alias': fbi_data_pd['items'][i]['aliases'],
                    'sex': fbi_data_pd['items'][i]['sex'],
                    'height': '',
                    'weight': fbi_data_pd['items'][i]['weight'],
                    'eyes': fbi_data_pd['items'][i]['eyes'],
                    'hair': fbi_data_pd['items'][i]['hair'],
                    'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
                    'nationality': fbi_data_pd['items'][i]['nationality'],
                    'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
                    'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
                    'charges': fbi_data_pd['items'][i]['subjects'],
                    'wanted_by': 'FBI',
                    'status': fbi_data_pd['items'][i]['status'],
                    'publication': fbi_data_pd['items'][i]['publication'],
                    'last_modified': fbi_data_pd['items'][i]['modified'],
                    'reward': fbi_data_pd['items'][i]['reward_max'],
                    'details': fbi_data_pd['items'][i]['details'],
                    'caution': fbi_data_pd['items'][i]['caution'],
                    'remarks': fbi_data_pd['items'][i]['warning_message'],
                    'images': '',
                    'link': fbi_data_pd['items'][i]['url'],
                }
                fugitive_profile_extracts.append(profile)
                # print(profile)
            page += 1

        for profile in fugitive_profile_extracts:
            self.compiled_fugitive_list.append(list(profile.values()))

    def interpol_fugitive_id(self):
        fugitive_id_list = []
        for i in range(0, 346):
            interpol_response = requests.get(f'https://ws-public.interpol.int/notices/v1/red?page={i}')
            interpol_data = json.loads(interpol_response.content)

            # Base case
            if interpol_data['query']['page'] != i:
                return
            # print(interpol_data['query']['page'])

            additional_info_url = 'https://ws-public.interpol.int/notices/v1/red/'
            for i in range(0, len(interpol_data['_embedded']['notices'])):
                # interpol_data['_embedded']['notices'][i]['']
                entity_id = interpol_data['_embedded']['notices'][i]['entity_id']
                fugitive_id = additional_info_url + entity_id.replace('/','-')
                fugitive_id_list.append(fugitive_id)
        print(fugitive_id_list)
        print('here')
        print('\n')
        print(len(fugitive_id_list))
        print('there')
        return fugitive_id_list

    def scrape_interpol_fugitive_profiles(self):
        print('Extracting Interpol Fugitives...')
        fugitive_profile_extracts = []
        individual_red_notice_url = self.interpol_fugitive_id()
        # print(individual_red_notice_url)
        # print(len(individual_red_notice_url))
        for url in individual_red_notice_url:
            # print(len(interpol_fugitive_records))
            interpol_response = requests.get(url)
            interpol_data = json.loads(interpol_response.content)
            # print(interpol_data['arrest_warrants'])
            # print(url)
            # print(interpol_data['_links']['thumbnail'])
            # Check if a profile consists of images
            if interpol_data['_links']:
                if interpol_data['_links']['images']:
                    images = [ interpol_data['_links']['images']['href'] if interpol_data['_links']['images']['href'] else '' ],
                if interpol_data['_links']['self']:
                    link = [ interpol_data['_links']['self']['href'] if interpol_data['_links']['self']['href'] else '' ],

            firstname = [ interpol_data['forename'] if interpol_data['forename'] else '' ]
            lastname = [ interpol_data['name'] if interpol_data['name'] else '' ]
            record = {
                'name': firstname + ' ' + lastname,
                'alias': '',
                'sex': [ interpol_data['sex_id'] if interpol_data['sex_id'] else '' ],
                'height': [ interpol_data['height'] if interpol_data['height'] else '' ],
                'weight': [ interpol_data['weight'] if interpol_data['weight'] else '' ],
                'eyes': [ interpol_data['eyes_colors_id'] if interpol_data['eyes_colors_id'] else '' ],
                'hair': [ interpol_data['hairs_id'] if interpol_data['hairs_id'] else '' ],
                'distinguishing_marks': [ interpol_data['distinguishing_marks'] if interpol_data['distinguishing_marks'] else '' ],
                'nationality': [ interpol_data['nationalities'] if interpol_data['nationalities'] else '' ],
                'date_of_birth': [ interpol_data['date_of_birth'] if interpol_data['date_of_birth'] else '' ],
                'place_of_birth': [ interpol_data['place_of_birth'] if interpol_data['place_of_birth'] else '' ],
                'charges' : [ interpol_data['arrest_warrants'][0]['charge'] if interpol_data['arrest_warrants'][0]['charge'] else '' ],
                'wanted_by': [ interpol_data['arrest_warrants'][0]['issuing_country_id'] if interpol_data['arrest_warrants'][0]['issuing_country_id'] else '' ],
                'status': 'wanted',
                'publication': '',
                'last_modified': '',
                'reward': '',
                'details': '',
                'caution': '',
                'remarks': '',
                'images': images,
                'thumbnail': '',
                'link': link,
            }
            fugitive_profile_extracts.append(record)

        for profile in fugitive_profiles_extract:
            self.compiled_fugitive_list.append(list(profile.values()))



def main():
    sc = Scraper()
    # sc.scrape_rcmp_fugitive_profiles()
    sc.scrape_fbi_fugitive_profiles()
    # sc.interpol_fugitive_id()
    # sc.scrape_interpol_fugitive_profiles()

    for i in sc.compiled_fugitive_list:
        print(i)
        print('\n')
    print(len(sc.compiled_fugitive_list))


if __name__ == '__main__':
    main()