from flask import Flask, redirect, request, render_template
from bokeh_plot import create_plot

app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/plot')


@app.route('/plot')
def index():
    script, div = create_plot()
    return render_template('plot.html', script=script, div=div)

if __name__ == '__main__':
    # app.run(port=5000, debug=True)
    app.run(port=33507)
    # app.run(host='0.0.0.0')
