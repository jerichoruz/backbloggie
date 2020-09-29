## Installation
  - Install [Python](https://www.python.org/downloads/), [Pipenv](https://docs.pipenv.org/) and [Postgres](https://www.postgresql.org/) on your machine
  - Clone the repository `$ git clone git@github.com:jerichoruz/backbloggie.git`
  - Change into the directory `$ cd /fido-back`
  - Create the project virtual environment with `$ pipenv --three` command
  - Activate the project virtual environment with `$ pipenv shell` command
  - Install all required dependencies with `$ pipenv install`
  - Rename .env.sample to .env and edit variables
      ```
      FLASK_ENV=development
      FLASK_PORT=5005
      DATABASE_URL=postgres://user:pass@localhost:5432/bd
      JWT_SECRET_KEY=pass_salt_phrase
      ```
  - Create database fido
  - `$ python manage.py db init`
  - `$ python manage.py db migrate`
  - `$ python manage.py db upgrade`
  
  - Start the app with `python run.py`
