from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/callback")
def callback():
    # Get Spotify OAuth params
    code = request.args.get("code")
    state = request.args.get("state")

    print(f"Got code: {code}, state: {state}")

    # Build local redirect URL
    n8n_redirect = f"http://localhost:5678/rest/oauth2-credential/callback"

    # Redirect to local n8n
    return redirect(n8n_redirect)

if __name__ == "__main__":
    app.run(port=8080)
