# Music-DL Server

Backend flask application for [Music-DL](https://github.com/CaptainDaVinci/Music-DL), handles conversion to 
mp3/mp4 file and tags them.  

## Contributing

* Clone the project and cd into it.
```
$ git clone https://github.com/CaptainDaVinci/Music-DL-Server.git
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

