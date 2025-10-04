import os
import json
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)

# ✅ Path to the same cousins.json your bot updates on the VPS
COUSINS_FILE = "/home/container/cousins.json"
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/nenenen/main/cousins.json"

@app.route("/cousin/<user_id>", methods=["GET", "POST"])
def cousin_profile(user_id):
    # Load the latest data directly from the file
    try:
        with open(COUSINS_FILE, "r") as f:
            cousins = json.load(f)
    except Exception as e:
        return f"❌ Could not load local data: {e}", 500

    data = cousins.get(user_id)
    if not data:
        return abort(404)

    if request.method == "POST":
        password = request.form.get("password")
        if password == data.get("password"):
            # ✅ Show profile when password matches
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{data['name']}'s Profile</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{
                        background-color: #ffffff;
                        color: #000000;
                        font-family: 'Segoe UI', sans-serif;
                    }}
                    .card {{
                        background-color: #f8f9fa;
                        border: none;
                        border-radius: 1rem;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                        transition: transform 0.3s, box-shadow 0.3s;
                        max-width: 600px;
                        margin: 50px auto;
                        text-align: center;
                    }}
                    .card:hover {{
                        transform: translateY(-8px);
                        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    }}
                    .avatar {{
                        width: 140px;
                        height: 140px;
                        border-radius: 50%;
                        margin: -70px auto 10px;
                        display: block;
                        border: 5px solid #fff;
                    }}
                    .banner {{
                        width: 100%;
                        border-top-left-radius: 1rem;
                        border-top-right-radius: 1rem;
                        max-height: 200px;
                        object-fit: cover;
                    }}
                    h1 {{
                        margin-top: 15px;
                        font-size: 2.2rem;
                    }}
                    p {{
                        font-size: 1.2rem;
                        margin: 5px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    {"<img src='"+data.get('banner', '')+"' class='banner'>" if data.get('banner') else ""}
                    {"<img src='"+data.get('avatar', '')+"' class='avatar'>" if data.get('avatar') else ""}
                    <h1>{data['name']}</h1>
                    <p>🆔 Cousin ID: <strong>{data['cousin_id']}</strong></p>
                    <p>🏅 Rank: <strong>#{data['rank']}</strong></p>
                    <p>👀 Reputation: <strong>{data['rep']}/100</strong></p>
                </div>
            </body>
            </html>
            """
            return html
        else:
            return render_template_string("""
                <h1>❌ Wrong password!</h1>
                <a href="">Try again</a>
            """)

    # ✅ Login form page
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Login to View Profile</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #ffffff;
                    color: #000;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: 'Segoe UI', sans-serif;
                }
                .login-box {
                    background: #f8f9fa;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                    width: 350px;
                    text-align: center;
                }
                input {
                    margin-top: 10px;
                    width: 100%;
                    padding: 10px;
                    border-radius: 8px;
                    border: 1px solid #ccc;
                }
                button {
                    margin-top: 20px;
                    width: 100%;
                    padding: 10px;
                    border: none;
                    border-radius: 8px;
                    background: #000;
                    color: white;
                    font-weight: bold;
                    transition: background 0.3s;
                }
                button:hover {
                    background: #333;
                }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h2>🔒 Enter Password</h2>
                <form method="post">
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Access Profile</button>
                </form>
            </div>
        </body>
        </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
