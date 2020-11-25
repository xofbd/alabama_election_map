# Alabama Election Map
This repository contains the files necessary to deploy a [Bokeh](https://docs.bokeh.org/en/latest/index.html) figure on [Heroku](https://www.heroku.com) using [Flask](https://flask.palletsprojects.com/en/1.1.x/). The code visualizes the Alabama Senate Special Election 2017 results on a county level. The results of the US Presidential Election 2016 are also visualized as a comparison.

## Description
There are two modules, `process` and `app`.
* `process`: generates the requisite CSV files needed to visualize the election results.
* `app`: serves the Bokeh visualization using Flask.

While we could use one set of dependencies for the entire application, we use [`pip-tools`](https://github.com/jazzband/pip-tools/) so that the deployment environment only contains the necessary packages to run.

## Running the application
The first step to run the application is to clone the repository:
`git clone https://github.com/xofbd/alabama_election_map`.

If you have `make` installed you can run the application several ways.

1. `make deploy-standalone` to deploy with Bokeh directly.
1. `make deploy-dev` to deploy with Flask.
1. `make deploy-prod` to deploy with Flask and Gunicorn as the WSGI.

Note, running `make all` deploys with Flask in development mode. If you don't have `make` installed, you can following these steps instead.

1. `python3 -m venv venv`
1. `source venv/bin/activate && pip install -r requirements.txt`
1. `bin/deploy dev` (with the virtual environment activated)

## Deploying to Heroku
[Heroku](https://www.heroku.com) is a service to easily host web applications. Sign up and download the Heroku CLI tool. Make sure the application is ready to be deployed to Heroku by running the application locally. Follow the steps below to deploy to Heroku.

1. clone the repository.
1. `heroku login` and enter your credentials.
1. `heroku create` or `heroku create <app-name>` where `<app-name>` is a custom application name.
1. `git push heroku master`.
1. `heroku open` or open the application online through your Heroku profile.

## License
This project is distributed under the MIT license. Please see `LICENSE` for more information.
