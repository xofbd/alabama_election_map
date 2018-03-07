# Alabama Election Map
This repository is ready to deploy a Bokeh figure on Heroku. The code visualizes the Alabama Senate Special Election 2017 results on a county level. The results of the US Presidential Election 2016 are also visualized as a comparison.<br>

## Prerequisites
You will need to have these python packages installed. <br>
`bokeh, Flask, pandas` <br>
You can easily download and install them by running `pip install package-name`, where "package-name" is the name of the desired package. You will also need a Heroku account and have installed the Heroku CLI. For more information on the Heroku CLI, go to https://devcenter.heroku.com/articles/heroku-cli#download-and-install.

## County Data
The file `data/counties.p` was created by pickling the county data dictionary obtained from `bokeh.sampledata.us_counties`. This dictionary contains information like the county names and latitude and longitude pairs that define the shape of the county. When importing the county data from `bokeh.sampledata.us_counties`, errors will occur on Heroku, probably from not having write access. As a workaround, `counties.p` is used. <br>

## Running using only Bokeh
To run the code only using Bokeh, simply run `bokeh_plot.py`. This will open up the figure on your web browser. You may want to modify the code by changing parameters, adding features, widgets, etc. If that is the case, it is easier to debug your code by running `bokeh_plot.py`. <br>

## Running the app locally using Flask
You may want to run the app using Flask locally before deploying it to Heroku, especially if you have made any changes to the code. To run locally: <br>

0.) clone repository: `git clone https://github.com/xofbd/alabama_election_map` <br>
1.) in the alabama_election_map directory, run `export FLASK_APP=app.py` in the command line. If you are using Windows, replace `export` with `set` <br>
2.) run `python -m flask run` <br>
3.) open the link provided in the command line <br>
For more information on running Flask, go to http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application <br>

## Deploying to Heroku
Make sure your app is ready to be deployed to Heroku by running Flask locally. To deploy to Heroku: <br>

0.) clone repository (if you haven't yet): `git clone https://github.com/xofbd/alabama_election_map` <br>
1.) `heroku login` and enter your credentials <br>
2.) `heroku create` or `heroku create app-name` where app-name is a custom app name <br>
3.) `git push heroku master` <br>
4.) `heroku open` or open the app online through your Heroku profile <br>
