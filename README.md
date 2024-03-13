# tnlcalender
A Hacker News clone that can be used to post links to news articles, votes are cast by posting the same news article

## Development

Uncomment the sqlite database file
```python
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/tnlnews/db/news.db'
# Local development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
```

Create a new virtualenv

```shell
python -m venv venv
```

Load the virtualenv and pull in the requirements

```shell
# Linux
source venv/bin/activate
# Windows
.\venv\Scripts\activate

pip install -r requirements.txt
```

Set the ```FLASK_ENV``` and ```FLASK_DEBUG``` environment variables and run flask

```shell
# Linux
export FLASK_ENV=development
export FLASK_DEBUG=true

# Windows
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "true"

flask run
```