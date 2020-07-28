from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def list_actors(f):
        actors = Actors.query.all()
        formatted_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def list_movies(f):
        movies = Movies.query.all()

        formatted_movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatted_movies
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(f):
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
    @requires_auth('post:movies')
    def create_movie(f):
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
    @requires_auth('patch:actors')
    def update_actor(f, actor_id):
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
    @requires_auth('patch:movies')
    def update_movie(f, movie_id):
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
    @requires_auth('delete:actors')
    def delete_actor(f, actor_id):
        try:
            actor = Actors.query.get(actor_id)
            actor.delete()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(f, movie_id):
        try:
            movie = Movies.query.get(movie_id)
            movie.delete()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
