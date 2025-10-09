import os
import requests
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/cousinunited/refs/heads/main/cousins.json"

# --- Templates ---
LOADING_HTML = """..."""  # Keep your original loading HTML
LOGIN_HTML = """..."""    # Keep your original login HTML

PROFILE_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{{ data.name }} — Cousin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --blue:#00bfff;
  --white:#ffffff;
  --bg:#000;
}

/* Glow animations */
@keyframes pulseGlow {
  0% { box-shadow: 0 0 8px var(--blue),0 0 16px var(--blue); }
  50% { box-shadow: 0 0 20px var(--white),0 0 40px var(--blue); }
  100% { box-shadow: 0 0 8px var(--blue),0 0 16px var(--blue); }
}
@keyframes textGlow {
  0% { text-shadow: 0 0 4px var(--blue); }
  50% { text-shadow: 0 0 12px var(--white),0 0 24px var(--blue); }
  100% { text-shadow: 0 0 4px var(--blue); }
}

*{box-sizing:border-box;}
html,body{margin:0;height:100%;font-family:Inter,Arial,sans-serif;background:var(--bg);color:var(--white);
  display:flex;align-items:center;justify-content:center;padding:24px;}

.wrapper{
  width:100%;
  max-width:900px;
}

.card{
  background: rgba(0,0,0,0.75);
  border-radius:24px;
  padding:48px;
  text-align:center;
  animation:pulseGlow 5s infinite ease-in-out;
}

.avatar-wrap{
  width:140px;
  height:140px;
  border-radius:50%;
  overflow:hidden;
  margin:0 auto 24px;
  border:3px solid var(--blue);
  animation:pulseGlow 5s infinite ease-in-out;
}

.avatar-wrap img{
  width:100%;
  height:100%;
  object-fit:cover;
}

.username{
  font-size:2rem;
  font-weight:700;
  animation:textGlow 4s infinite ease-in-out;
  margin-bottom:6px;
}

.verified-badge{
  display:inline-block;
  background:linear-gradient(90deg,var(--blue),var(--white));
  color:#000;
  font-weight:700;
  padding:4px 8px;
  border-radius:6px;
  margin-left:8px;
}

.subtitle{
  font-size:1rem;
  color:#cfcfcf;
  margin-bottom:18px;
}

.info-row{
  display:flex;
  justify-content:center;
  flex-wrap:wrap;
  gap:12px;
  margin-bottom:20px;
}

.info-pill{
  background: rgba(255,255,255,0.05);
  padding:6px 12px;
  border-radius:12px;
  font-weight:600;
}

.status-card{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:12px;
  background: rgba(255,255,255,0.05);
  padding:12px;
  border-radius:12px;
  margin-top:20px;
}

.status-avatar{
  width:50px;
  height:50px;
  border-radius:50%;
  object-fit:cover;
  border:2px solid rgba(0,191,255,0.3);
  animation:pulseGlow 5s infinite ease-in-out;
}

.status-text{
  font-weight:600;
}

.status-sub{
  font-size:0.85rem;
  color:#ccc;
}

@media(max-width:720px){
  .card{padding:28px;}
  .avatar-wrap{width:100px;height:100px;}
  .username{font-size:1.6rem;}
  .subtitle{font-size:0.95rem;}
}
</style>
</head>
<body>
<div class="wrapper">
  <div class="card">
    <div class="avatar-wrap">
      {% if data.avatar %}
        <img src="{{ data.avatar }}" alt="avatar">
      {% endif %}
    </div>
    <div class="username">
      {{ data.name }}
      {% if data.verified %}
        <span class="verified-badge">VERIFIED</span>
      {% endif %}
    </div>
    <div class="subtitle">hello my name is {{ data.display_name or data.name }}!!!</div>
    <div class="info-row">
      <div class="info-pill">🆔 Cousin ID: <strong>{{ data.cousin_id }}</strong></div>
      <div class="info-pill">🏅 Rank: <strong>#{{ data.rank }}</strong></div>
      <div class="info-pill">👀 Rep: <strong>{{ data.rep }}/100</strong></div>
    </div>
    <div class="status-card">
      {% if data.small_avatar %}
        <img src="{{ data.small_avatar }}" class="status-avatar">
      {% elif data.avatar %}
        <img src="{{ data.avatar }}" class="status-avatar">
      {% else %}
        <div class="status-avatar"></div>
      {% endif %}
      <div>
        <div class="status-text">{{ data.status_name or data.name }}</div>
        <div class="status-sub">{{ data.status_text or 'currently doing nothing' }}</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

# --- End templates ---

@app.route("/cousin/<user_id>", methods=["GET", "POST"])
def cousin_profile(user_id):
    try:
        resp = requests.get(JSON_URL, timeout=6)
        resp.raise_for_status()
        cousins = resp.json()
    except Exception as e:
        return f"❌ Could not load data: {e}", 500

    data = cousins.get(user_id)
    if not data:
        return abort(404)

    verified = request.args.get("verified") == "1"

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == data.get("password"):
            return render_template_string(LOADING_HTML)
        else:
            return render_template_string("""
                <!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"/></head>
                <body style="background:black;color:white;font-family:Inter,Arial;text-align:center;padding:40px;">
                <h1>❌ Wrong password!</h1>
                <p><a href="" style="color:#61f3ff;text-decoration:none;font-weight:700">Try again</a></p>
                </body></html>
            """)

    if verified:
        return render_template_string(PROFILE_HTML, data=data)

    return render_template_string(LOGIN_HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
