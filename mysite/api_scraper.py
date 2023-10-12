import requests
import json
import pandas as pd

################################### FBI API ###################################
def fbi_fugitive_profiles():
    """
    Implements api pagination.
    """
    fbi_profile_extracts = []
    page = 1
    while True:
        response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
        print(response)
        fbi_data = response.json()
        # fbi_data = json.loads(response.content)
        fbi_data_pd = pd.DataFrame.from_dict(fbi_data)

        # Base case
        if len(fbi_profile_extracts) == fbi_data['total']:
            break

        for i in range(0, len(fbi_data_pd['items'])):
            profile = {
                'name': fbi_data_pd['items'][i]['title'],
                'alias': fbi_data_pd['items'][i]['aliases'],
                'sex': fbi_data_pd['items'][i]['sex'],
                'age_min': fbi_data_pd['items'][i]['age_min'],
                'age_max': fbi_data_pd['items'][i]['age_max'],
                'height_min': fbi_data_pd['items'][i]['height_min'],
                'height_max': fbi_data_pd['items'][i]['height_max'],
                'weight': fbi_data_pd['items'][i]['weight'],
                'eyes': fbi_data_pd['items'][i]['eyes'],
                'hair': fbi_data_pd['items'][i]['hair'],
                'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
                'nationality': fbi_data_pd['items'][i]['nationality'],
                'age_range': fbi_data_pd['items'][i]['age_range'],
                'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
                'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
                'charges': fbi_data_pd['items'][i]['subjects'],
                'wanted_by': 'FBI',
                'publication': fbi_data_pd['items'][i]['publication'],
                'last_modified': fbi_data_pd['items'][i]['modified'],
                'status': fbi_data_pd['items'][i]['status'],
                'reward': fbi_data_pd['items'][i]['reward_max'],
                'details': fbi_data_pd['items'][i]['details'],
                'caution': fbi_data_pd['items'][i]['caution'],
                'remarks': fbi_data_pd['items'][i]['warning_message'],
                'images': '',
                'link': fbi_data_pd['items'][i]['url'],
            }
            fbi_profile_extracts.append(profile)
            print(profile)

        page += 1
        print('#########################')
    print(len(fbi_profile_extracts))

fbi_fugitive_profiles()
# print(fbi_profile_extracts[999])


################################### INTERPOL API  ###################################
def interpol_fugitive_id():
    fugitive_id_urls = []
    for i in range(0, 346):
        interpol_response = requests.get(f'https://ws-public.interpol.int/notices/v1/red?page={i}')
        interpol_data = json.loads(interpol_response.content)

        # Base case
        if interpol_data['query']['page'] != i:
            return
        print(interpol_data['query']['page'])

        additional_info_url = 'https://ws-public.interpol.int/notices/v1/red/'
        for i in range(0, len(interpol_data['_embedded']['notices'])):
            # interpol_data['_embedded']['notices'][i]['']
            id = interpol_data['_embedded']['notices'][i]['entity_id']
            url = additional_info_url + id.replace('/','-')
            url_list.append(url)
    return fugitive_id_urls


def interpol_profiles_extract():
    interpol_fugitive_profiles = []

    individual_red_notice_url = interpol_fugitive_id()
    # Iterate over URLs of fugitive recrods
    for url in individual_red_notice_url:
        # print(len(interpol_fugitive_records))
        interpol_response = requests.get(url)
        interpol_data = json.loads(interpol_response.content)
        # print(interpol_data['arrest_warrants'])
        print(url)
        # print(interpol_data['_links']['thumbnail'])
        # Check if a profile consists of images
        if interpol_data['_links']:
            if interpol_data['_links']['images']:
                images = [ interpol_data['_links']['images']['href'] if interpol_data['_links']['images']['href'] else '' ],
            if interpol_data['_links']['self']:
                link = [ interpol_data['_links']['self']['href'] if interpol_data['_links']['self']['href'] else '' ],

        record = {
            'firstname': [ interpol_data['forename'] if interpol_data['forename'] else '' ],
            'lastname': [ interpol_data['name'] if interpol_data['name'] else '' ],
            'alias': '',
            'sex': [ interpol_data['sex_id'] if interpol_data['sex_id'] else '' ],
            'age_min': '',
            'age_max': '',
            'height_min': '',
            'height_max': '',
            'height': [ interpol_data['height'] if interpol_data['height'] else '' ],
            'weight': [ interpol_data['weight'] if interpol_data['weight'] else '' ],
            'eyes': [ interpol_data['eyes_colors_id'] if interpol_data['eyes_colors_id'] else '' ],
            'hair': [ interpol_data['hairs_id'] if interpol_data['hairs_id'] else '' ],
            'distinguishing_marks': [ interpol_data['distinguishing_marks'] if interpol_data['distinguishing_marks'] else '' ],
            'nationality': [ interpol_data['nationalities'] if interpol_data['nationalities'] else '' ],
            'age_range': '',
            'date_of_birth': [ interpol_data['date_of_birth'] if interpol_data['date_of_birth'] else '' ],
            'place_of_birth': [ interpol_data['place_of_birth'] if interpol_data['place_of_birth'] else '' ],
            'charges' : [ interpol_data['arrest_warrants'][0]['charge'] if interpol_data['arrest_warrants'][0]['charge'] else '' ],
            'wanted_by': [ interpol_data['arrest_warrants'][0]['issuing_country_id'] if interpol_data['arrest_warrants'][0]['issuing_country_id'] else '' ],
            'publication': '',
            'last_modified': '',
            'status': 'wanted',
            'reward': '',
            'details': '',
            'caution': '',
            'remarks': '',
            'images': images,
            'thumbnail': '',
            'link': link,
        }
        interpol_fugitive_profiles.append(record)

# interpol_fugitive_id(page_num, fugitive_id_urls)
# get_interpol_records(fugitive_id_urls)
# print('complete')



from selectolax.parser import HTMLParser

class APIScraper:
    def __init__(self):
        self.interpol_fugitive_records = []
        self.fbi_fugitive_records = []

    def interpol_records(self):
        URL = 'https://www.interpol.int/en/How-we-work/Notices/Red-Notices/View-Red-Notices'
        interpol_response = requests.get(URL)
        interpol_data = json.loads(interpol_response.content)
        # interpol_data_pd = pd.DataFrame(interpol_data)

        # Base case
        if page == 20:
            return

    def fbi_fugitive_profiles(self):
        """
        Implements api pagination.
        """
        fbi_profile_extracts = []
        page = 1
        while True:
            response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
            print(response)
            fbi_data = response.json()
            # fbi_data = json.loads(response.content)
            fbi_data_pd = pd.DataFrame.from_dict(fbi_data)

            # Base case
            if len(fbi_profile_extracts) == fbi_data['total']:
                break

            for i in range(0, len(fbi_data_pd['items'])):
                profile = {
                    'name': fbi_data_pd['items'][i]['title'],
                    'alias': fbi_data_pd['items'][i]['aliases'],
                    'sex': fbi_data_pd['items'][i]['sex'],
                    'age_min': fbi_data_pd['items'][i]['age_min'],
                    'age_max': fbi_data_pd['items'][i]['age_max'],
                    'height_min': fbi_data_pd['items'][i]['height_min'],
                    'height_max': fbi_data_pd['items'][i]['height_max'],
                    'weight': fbi_data_pd['items'][i]['weight'],
                    'eyes': fbi_data_pd['items'][i]['eyes'],
                    'hair': fbi_data_pd['items'][i]['hair'],
                    'distinguishing_marks': fbi_data_pd['items'][i]['scars_and_marks'],
                    'nationality': fbi_data_pd['items'][i]['nationality'],
                    'age_range': fbi_data_pd['items'][i]['age_range'],
                    'date_of_birth': fbi_data_pd['items'][i]['dates_of_birth_used'],
                    'place_of_birth': fbi_data_pd['items'][i]['place_of_birth'],
                    'charges': fbi_data_pd['items'][i]['subjects'],
                    'wanted_by': 'FBI',
                    'publication': fbi_data_pd['items'][i]['publication'],
                    'last_modified': fbi_data_pd['items'][i]['modified'],
                    'status': fbi_data_pd['items'][i]['status'],
                    'reward': fbi_data_pd['items'][i]['reward_max'],
                    'details': fbi_data_pd['items'][i]['details'],
                    'caution': fbi_data_pd['items'][i]['caution'],
                    'remarks': fbi_data_pd['items'][i]['warning_message'],
                    'images': '',
                    'link': fbi_data_pd['items'][i]['url'],
                }
                fbi_profile_extracts.append(profile)
                print(profile)

            page += 1
            print('#########################')
        print(len(fbi_profile_extracts))




    def fbi_records(self):
        pass

