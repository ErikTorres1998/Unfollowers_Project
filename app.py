from flask import Flask, request, render_template
import instaloader

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_followers', methods=['POST'])
def check_followers():
    username = request.form['username']
    password = request.form['password']

    # Initialize instaloader
    L = instaloader.Instaloader()

    try:
        # Login to Instagram
        L.login(username, password)
    except Exception as e:
        return render_template('error.html', error=str(e))

    # Get profile
    profile = instaloader.Profile.from_username(L.context, username)

    # Get list of followers and followees
    followers = set(follower.username for follower in profile.get_followers())
    followees = set(followee.username for followee in profile.get_followees())

    # Determine non-followers
    non_followers = followees - followers

    return render_template('results.html', non_followers=non_followers)


if __name__ == '__main__':
    app.run(debug=True)
