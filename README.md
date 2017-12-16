# Alabama

This repository is ready to used to deploy onto Heroku. Just follow these steps. Make sure you have heroku CLI installed on your computer. The texas.py file from the Heroku website had to be modified to work with Heroku. The problem is that the bokeh commands to download the data requires write access which causes errors in Heroku. The work around is to use the pickle package to serialize those Python objects and unpickle them in the code.

<br>

0.) clone repository: `git clone https://github.com/xofbd/alabama` <br>
1.) `heroku login` and enter your credentials <br>
2.) `heroku create` or `heroku create app-name` where app-name is your custome app name <br>
3.) `git push heroku master` <br>
4.) `heroku open` <br>
5.) you should get something that looks like this: 