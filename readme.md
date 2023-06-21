# Local file server

## Launching project


In the project directory, you can run:

### `flask start --port=8001`

or by opening `start.bat`

Runs the app in the development mode.\
Open [http://127.0.0.1:8001/](http://127.0.0.1:8001/) to view it in the browser.
This task contains simple front-end to test its functionality.
Tested with 5000+ and 2.5GB files

## Used libraries:

- Flask
- Flask-cors

## Folder structure

- `html` - Folder with .html files
- `upload` - Folder to storing uploaded files (doesn't need to exist at beginning)
- `api.json` - generated API documentation
- `app.py` - Back-end Flask script
- `readme.md` - This readme
- `start.bat` - Launch script for Flask application

## API calls

API calls are documented in `API.json` by `APIFlask` tool