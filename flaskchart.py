from flask import Flask, render_template


app = Flask(__name__)


@app.route("/<int:bars_count>/")
def chart(bars_count):
    if bars_count <= 0:
        bars_count = 1
    return render_template("chart.html", bars_count=bars_count)


if __name__ == "__main__":
    app.run(debug=True)
