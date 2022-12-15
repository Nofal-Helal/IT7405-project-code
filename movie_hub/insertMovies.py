from datetime import  date
from decimal import Decimal
from django.utils import timezone
from djongo.models.fields import ObjectId

from movie_hub.models import Movie

m = Movie()
m.title = "Bullet Train"
m.year = 2022
m.duration = {'hours': 2, 'minutes': 7}
m.directors = ['David Leitch']
m.writers = ['Zak Olkewicz (screenplay by)', 'Kôtarô Isaka (based on the book by)']
m.cast = ['Brad Pitt','Joey King','Aaron Taylor-Johnson']
m.parentsGuide = 'R'
m.posterImage = 'movie_hub/bullet_train.webp'
m.summary = 'Five assassins aboard a swiftly-moving bullet train find out that their missions have something in common.'
m.genres = ['action', 'comedy', 'thriller']
m.imdb = {'imdb_id': 'tt12593682', 'rating': 7.3, 'votes': 209_530}
m.comments = [{
    'user_id': ObjectId(),
    'text': 
        """This movie grabs you from the start and doesn't let go. Its an entertaining whirlwind of goofy character after goofy character, and awesome fight after awesome fight. Brad Pitt nails his leading role and everyone else does great.
        
        The visuals of the film are fantastic- soaked in a beautiful neon glow. While soundtrack is fine but not too memorable outside of the film.
        
        Overall, this is a great summer watch.
        """,
    'date': date(2022, 8, 3)
}, {
    'user_id': ObjectId(),
    'text': 
        """Rare seeing Brad Pitt in a movie like this but from what I understand the director is a good friend of his. It's an action movie the reads like Smoking Aces. An ensemble cast with a few different stories in it, of which, interestingly enough Brad Pitt's story as a man named Ladybug could be considered just as important as the others despite being the star.
        """,
    'date': date(2022, 8, 3)
}]

m.save()
