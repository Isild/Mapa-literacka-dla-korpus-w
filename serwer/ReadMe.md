### Installation and start
0.	Make sure you have python3, pip and virtualenv installed
1.	Create venv  
	**_Linux_**  
	```bash
	$ python3 -m venv env
	$ source env/bin/activate
	```
	**_Windows_**  
	```bat
	$ py -m venv env
	$ .\env\Scripts\activate
	```
2.	Install required libraries from `requirements.txt`  
	```bash
	(env) $ pip install -r requirements.txt
	```
3.	Launch  
	```bash
	(env) $ python app_run.py run
	```
	Similar output should indicate that the app is up and running:  
	```
	* Serving Flask app "app.services.app" (lazy loading)
	(...)
	* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	```

### Commands
* `run` - lunches app

### Available endpoints
Available endpoints are defined in [app/controllers/\_\_init\_\_.py](app/controllers/__init__.py).

### Folders
* `app` - main app module, contains flask app object and db object
* `configs` - configs
* `app/controllers` - controllers
* `app/helpers` - for wrappers and other classes/functions
* `app/models` - definition of db models
* `app/services` - main app logic, controllers uses services
