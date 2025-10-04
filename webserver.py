import os
import requests
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/cousinunited/refs/heads/main/cousins.json"

@app.route("/cousin/<user_id>", methods=["GET", "POST"])
def cousin_profile(user_id):
    # Fetch latest JSON for live updates
    try:
        resp = requests.get(JSON_URL)
        resp.raise_for_status()
        cousins = resp.json()
    except Exception as e:
        return f"❌ Could not load data: {e}", 500

    data = cousins.get(user_id)
    if not data:
        return abort(404)

    if request.method == "POST":
        password = request.form.get("password")
        if password != data.get("password"):
            return render_template_string("""
                <h1 style="color:white;text-align:center;">❌ Wrong password!</h1>
                <a href="" style="color:white;text-align:center;display:block;margin-top:10px;">Try again</a>
            """)
        # Render profile with live update JS
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
                    background-color: #000;
                    color: #fff;
                    font-family: 'Segoe UI', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                .container-card {{
                    background: rgba(255,255,255,0.05);
                    border: 2px solid #fff;
                    border-radius: 1rem;
                    padding: 2rem;
                    text-align: center;
                    max-width: 600px;
                    box-shadow: 0 0 30px #fff, 0 0 60px #fff inset;
                }}
                .avatar {{
                    width: 140px;
                    height: 140px;
                    border-radius: 50%;
                    border: 3px solid #fff;
                    margin-top: -70px;
                    object-fit: cover;
                    box-shadow: 0 0 20px #fff, 0 0 40px #fff inset;
                }}
                .banner {{
                    width: 100%;
                    max-height: 200px;
                    object-fit: cover;
                    border-radius: 1rem 1rem 0 0;
                    transition: transform 0.5s ease;
                }}
                .banner:hover {{ transform: scale(1.05); }}
                h1 {{
                    margin: 1rem 0;
                    font-size: 2.2rem;
                    text-shadow: 0 0 10px #fff;
                    color: #fff;
                }}
                p {{
                    font-size: 1.3rem;
                    margin: 0.5rem 0;
                    text-shadow: 0 0 5px #fff;
                    color: #fff;
                }}
            </style>
        </head>
        <body>
            <div class="container-card">
                {"<img src='"+data.get('banner', '')+"' class='banner'>" if data.get('banner') else ""}
                {"<img src='"+data.get('avatar', '')+"' class='avatar' id='avatar'>" if data.get('avatar') else ""}
                <h1 id="name">{data['name']}</h1>
                <p>🆔 Cousin ID: <strong id="cousin_id">{data['cousin_id']}</strong></p>
                <p>🏅 Rank: <strong id="rank">#{data['rank']}</strong></p>
                <p>👀 Reputation: <strong id="rep">{data['rep']}/100</strong></p>
            </div>

            <script>
                const userId = "{user_id}";
                const token = "{data.get('password', '')}";

                async function updateProfile() {{
                    try {{
                        const resp = await fetch("{JSON_URL}");
                        const json = await resp.json();
                        const user = json[userId];
                        if (!user) return;

                        document.getElementById('name').textContent = user.name;
                        document.getElementById('rank').innerHTML = "🏅 Rank: <strong>#" + user.rank + "</strong>";
                        document.getElementById('rep').innerHTML = "👀 Reputation: <strong>" + user.rep + "/100</strong>";
                        document.getElementById('cousin_id').innerHTML = user.cousin_id;
                        if(user.avatar) document.getElementById('avatar').src = user.avatar;
                    }} catch(e) {{
                        console.error("Error fetching live data:", e);
                    }}
                }}

                setInterval(updateProfile, 2000); // live update every 2 sec
            </script>
        </body>
        </html>
        """
        return html

    # GET → show password form
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Login - Cousin Network</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    background-color: #000;
                    color: #fff;
                    font-family: 'Segoe UI', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                .login-card {{
                    background: rgba(255,255,255,0.05);
                    border: 2px solid #fff;
                    padding: 2rem;
                    border-radius: 1rem;
                    text-align: center;
                    box-shadow: 0 0 20px #fff;
                    max-width: 400px;
                }}
                input {{
                    width: 100%;
                    padding: 0.5rem;
                    margin-bottom: 1rem;
                    border-radius: 0.5rem;
                    border: 1px solid #fff;
                    background: rgba(255,255,255,0.1);
                    color: #fff;
                }}
                button {{
                    padding: 0.5rem 1rem;
                    border-radius: 0.5rem;
                    border: none;
                    background: #fff;
                    color: #000;
                    font-weight: bold;
                    cursor: pointer;
                }}
                button:hover {{
                    box-shadow: 0 0 10px #fff;
                }}
            </style>
        </head>
        <body>
            <div class="login-card">
                <h1>Enter your password</h1>
                <form method="post">
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Enter</button>
                </form>
            </div>
        </body>
        </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
