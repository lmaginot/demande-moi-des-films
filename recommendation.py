import csv
from User import User
from random import randint


class Recommendation:

    def __init__(self):
        self.movies_list = []
        self.movies = dict()
        with open('./ml-latest-small/movies.csv', 'rt', encoding="utf-8") as moviesFile:
            movies = csv.reader(moviesFile, delimiter=',')
            is_first = True
            for movie in movies:
                if is_first:
                    is_first = False
                    continue
                self.movies[movie[0]] = movie[1]
                self.movies_list.append(movie[0])

        self.ratings = []
        with open('./ml-latest-small/ratings.csv', 'rt', encoding="utf-8") as ratingsFile:
            ratings = csv.reader(ratingsFile, delimiter=',')
            is_first = True
            for rating in ratings:
                if is_first:
                    is_first = False
                    continue
                self.ratings.append({'movie': rating[1], 'user': rating[0], 'score': rating[2]})

        self.test_users = {}
        self.users = {}
        self.process_ratings_to_users()

    def process_ratings_to_users(self):
        for rating in self.ratings:
            if rating.id not in self.test_users.keys():
                self.test_users[rating.id] = User(rating.id)
            user = self.test_users[rating.id]
            if rating.score >= 4:
                user.good_ratings.append(rating.movie)
            elif rating.score <= 2:
                user.bad_ratings.append(rating.movie)
            else:
                user.neutral_ratings.append(rating.movie)

    def register_user(self, sender):
        if sender not in self.users.keys():
            self.users[sender] = User(sender)
        return self.users[sender]

    def make_recommendation(self, user):
        similarities = self.compute_all_similarities(user)
        similarities.sort()
        similarities.reverse()
        best_match = similarities[0][0]
        recommendations = self.get_movies_from_user(best_match)
        return "Vos recommandations : " + ",".join(recommendations)

    def ask_question(self, user):
        movie_number = self.movies_list[randint(0, len(self.movies_list))]
        user.set_question(movie_number)
        return "Avez-vous aimé : " + self.movies[movie_number]

    def compute_all_similarities(self, user):
        similarities = []
        for other_user in self.test_users:
            similarities.append((User.get_similarity(user, other_user), other_user.id))
        return similarities

    def get_movies_from_user(self, user):
        movies_list = []
        good_movies = user.good_ratings
        for movie_number in good_movies:
            movies_list.append(self.movies[movie_number])
        return movies_list



