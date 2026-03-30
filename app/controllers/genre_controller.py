from models.genre_model import Genre


def list_genres():
    """"
        Crea una lista con todos los géneros precargados en la base de datos.
        """

    genres = Genre.get_all_genres()

    return [row[0] for row in genres] if genres else []
