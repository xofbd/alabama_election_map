from flask import Flask, redirect, render_template

from alabama.app.bokeh_plot import create_plot

app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/plot')


@app.route('/plot')
def plot():
    script, div = create_plot()

    return render_template('plot.html', script=script, div=div)


if __name__ == '__main__':
    app.run(debug=True)
