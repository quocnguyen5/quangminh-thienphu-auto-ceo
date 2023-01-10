import random
from flask import Flask, redirect

app = Flask(__name__)

# Note: http:// or https:// must be the prefix for proper redirection
websites = [
    # "http://tugtechmedia.com/earn/N190dW9uZ25ndXllbjE5OTc=-",  # utransfer
    # "http://tugtechmedia.com/earn/MjhfdHVvbmduZ3V5ZW4xOTk3-",  # publog
    # "http://tugtechmedia.com/earn/Ml90dW9uZ25ndXllbjE5OTc=-",  # publog
    # "http://tugtechmedia.com/earn/MTVfdHVvbmduZ3V5ZW4xOTk3-",  # gain
    "http://tugtechmedia.com/earn/NDdfdHVvbmduZ3V5ZW4xOTk3-",  # Sudda
]


@app.route('/')
def index():
    website = random.choice(websites)
    return redirect(website)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8394, debug=True)
