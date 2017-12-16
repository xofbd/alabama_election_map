# Alabama Election Map
This repository is ready to deploy a Bokeh figure on Heroku. <br>

## Running using only Bokeh
To run the code only using Bokeh, simply run `bokeh_plot.py`. This will open up the figure on your web browser. You may want to modify the code by changing parameters, adding feature, widgets, etc. If that is the case, it is easier to debug your code by running `bokeh_plot.py`. <br>

## Running the app locally using Flask
You may want to run the app using Flask locally before deploying it on Heroku, especially if you have made any changes to the code. To run locally: <br>

0.) clone repository: `git clone https://github.com/xofbd/alabama_election_map` <br>
1.) navigate to the `alabama_election_map` directory <br>
2.) in the alabama_election_map directory, run `export FLASK_APP=app.py` in the command line. If you are using Windows, replace `export` with `set` <br>
3.) run `python -m flask run` <br>
4.) open the link provided in the command line <br>

For more information on running Flask, go to http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application <br>

## Deploying to Heroku
Make sure your app is ready to be deployed on Heroku by running Flask locally. To deploy to Heroku: <br>

0.) clone repository (if you haven't yet): `git clone https://github.com/xofbd/alabama` <br>
1.) `heroku login` and enter your credentials <br>
2.) `heroku create` or `heroku create app-name` where app-name is your custom app name <br>
3.) `git push heroku master` <br>
4.) `heroku open` or open the app on your Heroku online profile <br>