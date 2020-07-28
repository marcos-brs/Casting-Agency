from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Actors, Movies
import json

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors', methods=['GET'])
    def list_actors():
        actors = Actors.query.all()
        formatted_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

    @app.route('/movies', methods=['GET'])
    def list_movies():
        movies = Movies.query.all()

        formatted_movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatted_movies
        })

    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()

        if body is None:
            abort(422)

        required_params = ['name', 'age', 'gender']

        for param in required_params:
            if param not in body:
                abort(422)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if gender != "female" and gender != "male":
            abort(22)

        try:
            new_actor = Actors(name=name, age=age, gender=gender)
            new_actor.insert()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'created': new_actor.id
        })

    @app.route('/movies', methods=['POST'])
    def create_movie():
        body = request.get_json()

        if body is None:
            abort(422)

        required_params = ['title', 'release_date']

        for param in required_params:
            if param not in body:
                abort(422)

        title = body.get('title')
        release_date = body.get('release_date')

        try:
            new_movie = Movies(title=title, release_date=release_date)
            new_movie.insert()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'created': new_movie.id
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        try:
            body = request.get_json()

            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            actor = Actors.query.get(actor_id)

            if name:
                actor.name = name

            if age:
                actor.age = age

            if gender:
                if gender != "female" and gender != "male":
                    abort(422)
                actor.gender = gender

            actor.update()

        except:
            abort(422)

        return jsonify({
            'success': True,
            'updated': actor_id
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):
        try:
            body = request.get_json()

            title = body.get('title')
            release_date = body.get('release_date')

            movie = Movies.query.get(movie_id)

            if title:
                movie.title = title

            if release_date:
                movie.release_date = release_date

            movie.update()

        except:
            abort(422)

        return jsonify({
            'success': True,
            'updated': movie_id
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actors.query.get(actor_id)
            actor.delete()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='localhost', port=80, debug=True)
