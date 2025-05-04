from flask import Flask, redirect, url_for, render_template
from livereload import Server

app = Flask(__name__)

@app.route("/")
def func():
    return render_template("registration.html")

if __name__ == "__main__":
    app.debug = True

    # Use livereload server instead of app.run
    server = Server(app.wsgi_app)
    # Watch for changes in templates and static files
    server.watch('templates/')
    server.watch('static/')
    # Start the livereload server
    server.serve(port=5000)