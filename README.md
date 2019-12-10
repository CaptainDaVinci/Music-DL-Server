# Music-DL Server

Backend flask application for [Music-DL](https://github.com/CaptainDaVinci/Music-DL), handles conversion to 
mp3/mp4 file and tags them.  

## Getting started

* Clone the project (if you're contributing, then you should fork the repo and then clone that copy, [more info](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github)) and cd into it.
```
$ git clone <git-url>
$ cd Music-DL-Server
```

* Set up a virtual environment
```
$ virutalenv env --python=python3
```

* Activate virtual environment
```
$ source env/bin/activate
```

* Install the packages
```
$ pip install -r requirements.txt
```

* Export flask variables
```
$ export FLASK_APP=main.py
$ export FLASK_ENV=development
```

* Run the application
```
$ flask run
```

* Navigate to http://localhost:5000/download?id=YQHsXMglC9A to download an mp3 file in high quality

