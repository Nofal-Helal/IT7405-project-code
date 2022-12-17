"""
This module allows downloading movie information from IMDb using 
the cinemagoer package.
"""
from datetime import date
from decimal import Decimal
from django.utils import timezone
from djongo.models.fields import ObjectId
import imdb
import pickle
import random
import re
import tqdm
import zlib

from movie_hub.models import Movie

ia = imdb.Cinemagoer()


def find_mpaa_rating(certificates: [str]) -> str:
    try:
        matches = [
            re.match(r'United States:(.+?):*', cert) for cert in certificates
            if cert.startswith('United States')
        ]
        match = list(filter(None, matches))[0]
        return match.group(1)
    except Exception as e:
        print("Couldn't get MPAA ")
        return ''


def get_movie_Model(id) -> Movie:
    im = ia.get_movie(id[2:], info=['main', 'plot', 'reviews'])
    m = Movie()
    m.title = im['title']
    m.year = im['year']
    hours, minutes = divmod(int(im['runtime'][0]), 60)
    m.duration = {'hours': hours, 'minutes': minutes}
    m.directors = [p['name'] for p in im['director'] if p.keys()]
    m.writers = [p['name'] for p in im['writer'] if p.keys()]
    m.cast = [p['name'] for p in im['cast'] if p.keys()][:3]
    m.parentsGuide = find_mpaa_rating(im['certificates'])
    m.posterImage = im['full-size cover url']
    m.summary = im['plot summary'][0]
    m.moreSummary = im['plot summary'][1]
    m.genres = im['genres']
    m.imdb = {'imdb_id': id, 'rating': im['rating'], 'votes': im['votes']}

    for user_id, review in zip([100, 101, 102], im['reviews'][:3]):
        comment_date = timezone.datetime(2022, 12, random.randint(1, 31))
        m.comments += [{
            'user_id': user_id,
            'text': review['content'],
            'rating': review['rating'],
            'date': comment_date
        }]

    return m


movies = [
    'tt0050083', 'tt11271038', 'tt14549466', 'tt15426294', 'tt13560574',
    'tt0054215', 'tt1462764', 'tt0118799', 'tt1853728', 'tt11564570',
    'tt13833688', 'tt0087843', 'tt0034583', 'tt0120689', 'tt1316037',
    'tt14114802', 'tt14715170', 'tt0435761', 'tt9764362', 'tt0114369',
    'tt15600222', 'tt0120737', 'tt1464335', 'tt14369780', 'tt0057565',
    'tt11827628', 'tt0270846', 'tt0090605', 'tt0056058', 'tt0088763',
    'tt4633694', 'tt0185183', 'tt8115900', 'tt0052357', 'tt4154756',
    'tt15474916', 'tt19770238', 'tt0110912', 'tt0172495', 'tt9411972',
    'tt0091251', 'tt5090568', 'tt14826022', 'tt0033467', 'tt2382320',
    'tt0073486', 'tt11897478', 'tt3704428', 'tt0407887', 'tt1745960',
    'tt0338013', 'tt0021749', 'tt0078748', 'tt0051201', 'tt0050825',
    'tt0120586', 'tt0114709', 'tt12530246', 'tt0362165', 'tt8178634',
    'tt8760708', 'tt0027977', 'tt0086190', 'tt0053125', 'tt0169547',
    'tt21994906', 'tt15255876', 'tt5834426', 'tt15145764', 'tt11555492',
    'tt1375666', 'tt14444726', 'tt10187208', 'tt0103064', 'tt0119217',
    'tt11138512', 'tt0082971', 'tt9114286', 'tt10954984', 'tt18925334',
    'tt0799949', 'tt5311514', 'tt8110652', 'tt0167260', 'tt7144666',
    'tt5108870', 'tt0110413', 'tt1016150', 'tt2582802', 'tt6791350',
    'tt1213644', 'tt0086879', 'tt0468569', 'tt0405094', 'tt8267604',
    'tt0120815', 'tt4513678', 'tt15791034', 'tt0209144', 'tt0062622',
    'tt0060666', 'tt17220704', 'tt11291274', 'tt0068646', 'tt0060196',
    'tt8041270', 'tt0910970', 'tt0114814', 'tt0043014', 'tt7286456',
    'tt6718170', 'tt10168670', 'tt6856242', 'tt0045152', 'tt9660502',
    'tt1596342', 'tt0361748', 'tt2380307', 'tt0056172', 'tt0111161',
    'tt0057012', 'tt4154796', 'tt10343028', 'tt14439896', 'tt0102926',
    'tt0167261', 'tt6751668', 'tt0032553', 'tt2106476', 'tt14807308',
    'tt8745676', 'tt10752004', 'tt1160419', 'tt9198364', 'tt0816692',
    'tt4009460', 'tt1675434', 'tt7775720', 'tt11992694', 'tt0112573',
    'tt1630029', 'tt18550140', 'tt6334354', 'tt6467266', 'tt0081505',
    'tt9419884', 'tt0022100', 'tt6710474', 'tt0080684', 'tt11245972',
    'tt0064116', 'tt10731256', 'tt0245429', 'tt0071562', 'tt15229674',
    'tt0364569', 'tt0253474', 'tt9288822', 'tt0109830', 'tt0108052',
    'tt0317676', 'tt12477480', 'tt10872600', 'tt0076759', 'tt7657566',
    'tt0095327', 'tt13007592', 'tt0180093', 'tt14138650', 'tt1345836',
    'tt12003946', 'tt10640346', 'tt11286314', 'tt9639470', 'tt0137523',
    'tt0482571', 'tt0119698', 'tt11116912', 'tt10304142', 'tt0078788',
    'tt4998632', 'tt7322224', 'tt14209916', 'tt0095765', 'tt0099685',
    'tt0317248', 'tt13320622', 'tt0038650', 'tt7693316', 'tt1877830',
    'tt0047478', 'tt0110357', 'tt13320662', 'tt0105236', 'tt1187043',
    'tt0804492', 'tt7375466', 'tt14208870', 'tt0082096', 'tt9032400',
    'tt6264654', 'tt0133093', 'tt0047396', 'tt1488589', 'tt20917338',
    'tt6443346', 'tt10999120', 'tt12593682', 'tt10298840'
]


# Download information on the sample movies listed above
# WARNING: This may take a long time
def downloadAllSampleMovies():
    movie_objects: [Movie] = []
    for movie in tqdm.tqdm(movies):
        try:
            movie_object = get_movie_Model(movie)
            movie_objects.append(movie_object)
        except Exception as e:
            print('----------------', movie)
            __import__('pprint').pprint(e)

    with open('movie_hub/movies.pickle', 'wb') as f:
        movies_bytes = pickle.dumps(movie_objects)
        print('movie bytes ', len(movies_bytes))
        compressed_bytes = zlib.compress(movies_bytes, level=9)
        print('compressed bytes ', len(compressed_bytes))
        f.write(compressed_bytes)
