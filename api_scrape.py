from imdb import IMDb
from imdb import IMDbDataAccessError
import pandas as pd
import requests
import imdb


def get_imdb_movie_id(df_title_year_dedu):
    """Function that takes array with movies as argument and returns a list
    of movies matched with their imdb id."""
    ia = IMDb()
    list_of_movies = []
    for year, award, winner, name, film in df_title_year_dedu:
        line = []
        movies_found = ia.search_movie(film)
        for movie in movies_found:
            try:
                if movie['year'] != None:
                    # if title and year match append
                    if movie['title'].lower() == film.lower(
                    ) and movie['year'] == year:
                        line.extend(
                            (movie['title'], movie['year'], movie.movieID,
                             year, film, award, winner, name))
                        break
                    # if title matches and year is in +-1 range
                    elif movie['title'].lower() == film.lower(
                    ) and year - 1 <= movie['year'] <= year + 1:
                        line.extend(
                            (movie['title'], movie['year'], movie.movieID,
                             year, film, award, winner, name))
                        break
                    # if title is in api title or vice versa, and years match
                    elif film.lower() in movie['title'].lower(
                    ) and year <= movie['year'] <= year or movie[
                            'title'] in film and year <= movie['year'] <= year:
                        line.extend(
                            (movie['title'], movie['year'], movie.movieID,
                             year, film, award, winner, name))
                        break
                    elif film.lower() in movie['title'].lower(
                    ) and year - 1 <= movie['year'] <= year + 1 or movie[
                            'title'] in film and year - 1 <= movie[
                                'year'] <= year + 1:
                        line.extend(
                            (movie['title'], movie['year'], movie.movieID,
                             year, film, award, winner, name))
                        break
            except KeyError:
                line.extend(
                    (None, None, None, year, film, award, winner, name))

        list_of_movies.append(line)
    return list_of_movies




def get_imdb_person_id(np_get_actor_data):
    """Function that takes array of actors names and movies played
    in as argument and returns a list of actors id and a dictionary
    of cast for every movie."""
    ia = IMDb()

    imdb_people_data = []
    cast_dict = dict.fromkeys(dict.fromkeys(np_get_actor_data[:, 0]))
    for id_movie, actor, last_name in np_get_actor_data:
        line = []
        cast_line = []
        # get movie info
        try:
            movie = ia.get_movie(id_movie)
            cast = movie['cast']
            # loop through cast of movie
            for person in cast:
                # add cast to dict with movie ids as keys
                cast_line.append([person.personID, person['name']])
                # if person in cast
                try:
                    if person['name'].lower() == actor.lower():
                        line.append(person.personID)
                        line.append(person['name'])
                        line.append(actor)
                        line.append(id_movie)
                        break
                    elif last_name.lower() in person['name'].lower():
                        line.append(person.personID)
                        line.append(person['name'])
                        line.append(actor)
                        line.append(id_movie)
                except IMDbDataAccessError:
                    print("error")
                except:
                    pass
            imdb_people_data.append(line)
            cast_dict[id_movie] = cast_line
        except IMDbDataAccessError:
            print("error")
        end = time.time()
    return imdb_people_data, cast_dict


def get_movie_details(movies):
    """Function that takes a list of movie ids as argument and 
    returns a list with runtime, genre, rating, and directors
    for each movie."""
    ia = IMDb()
    list_of_stuff = []
    for film in movies:
        line = []
        try:
            movie = ia.get_movie(film)
        except IMDbDataAccessError:
            print("error")
        try:
            runtime = movie['runtimes']
        except KeyError:
            runtime = None
        try:
            genres = movie['genres']
        except KeyError:
            genres = None
        try:
            rating = movie['rating']
        except KeyError:
            rating = None
        try:
            directors = movie['directors']
        except KeyError:
            directors = None
            break
        list_director = []
        for director in directors:
            director_id = director.personID
            director_name = director['name']
            list_director.append([director_id, director_name])
        list_of_stuff.append([film, runtime, genres, rating, list_director])
    return list_of_stuff


def get_actor_details(actors):
    """Function that takes a list of actor ID's as argument and returns a list
    with birthdate, birhtplace, height, headshot source and trademark."""
    ia = IMDb()
    list_of_stuff = []
    for actor in actors:
        line = []
        try:
            person = ia.get_person(actor)
        except IMDbDataAccessError:
            print("error")
        try:
            birth = person['birth date']
        except KeyError:
            birth = None
        try:
            height = person['height']
        except KeyError:
            height = None
        try:
            birth_i = person['birth info']['birth place']
        except KeyError:
            birth_i = None
        try:
            headshot = person['headshot']
        except KeyError:
            headshot = None
        try:
            trademark = person['trade mark']
        except KeyError:
            trademark = None
        list_of_stuff.append(
            [actor, birth, height, birth_i, headshot, trademark])
    return list_of_stuff

def get_birthplaces(actor_place, api_key):
    """Function that takes names of places as arguments and returns
    a dataframe with actor ID, birth place, name of birth town, 
    longitude and latitude of the birth town."""
    gmaps = googlemaps.Client(key=api_key)
    list_actor_places = []
    for actor, place in actor_place:
        try:
            geocode_result = gmaps.geocode(place)
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            true_name = geocode_result[0]['address_components'][0]['long_name']
            list_actor_places.append([actor, place, true_name, lat, lng])
        except:
            pass
    actor_places_df = pd.DataFrame.from_records(
        list_actor_places,
        columns=['actor_id', 'birth_place', 'true_name', 'latitude', 'longitude'])
    return actor_places_df

def get_movie_details2(movies):
    ia = IMDb()
    list_of_stuff = []
    for film in movies:
        line = []
        try:
            movie = ia.get_movie(film)
        except IMDbDataAccessError:
            print("error")
        try:
            box_office = movie['box office']
        except KeyError:
            box_office = None
        try:
            certificates = movie['certificates']
        except KeyError:
            certificates = None
        try:
            plot_o = movie['plot outline']
        except KeyError:
            plot_o = None
        try:
            plot = movie['plot']
        except KeyError:
            plot = None
            break
        list_of_stuff.append([film, box_office, certificates, plot_o, plot])
    return list_of_stuff
