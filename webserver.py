import os
import requests
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/cousinunited/refs/heads/main/cousins.json"

# --- Loading Screen ---
LOADING_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Loading Cousin Network...</title>
<style>
:root{
  --bg:#000;
  --neon:#00fff7;
  --accent:#61f3ff;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;}
body{
  display:flex;
  align-items:center;
  justify-content:center;
  background:var(--bg);
  color:#fff;
  font-family:Inter, "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
  text-align:center;
  overflow:hidden;
}
.container{
  width:100%;
  max-width:520px;
  padding:28px;
}
.title{
  font-size:1.6rem;
  letter-spacing:0.06em;
  margin-bottom:22px;
  text-shadow: 0 0 22px rgba(0,255,255,0.08);
}
.ring{
  width:110px;
  height:110px;
  margin:0 auto 22px;
  border-radius:50%;
  position:relative;
  box-shadow: 0 0 40px rgba(0,255,247,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
}
.ring::before{
  content:"";
  position:absolute;
  inset:6px;
  border-radius:50%;
  border:6px solid rgba(255,255,255,0.03);
}
.spinner {
  width:72px;
  height:72px;
  border-radius:50%;
  border:6px solid rgba(255,255,255,0.06);
  border-top-color:var(--neon);
  animation:spin 1s linear infinite;
  box-shadow: 0 0 20px var(--neon);
}
@keyframes spin{to{transform:rotate(360deg)}}
.hint{margin-top:12px;font-size:.95rem;color:rgba(255,255,255,0.7)}
</style>
</head>
<body>
<div class="container">
  <div class="title">Loading Cousin Network...</div>
  <div class="ring">
    <div class="spinner"></div>
  </div>
  <div class="hint">Syncing profile data — this takes a sec</div>
</div>
<script>
setTimeout(function(){
    window.location.href = window.location.pathname + "?verified=1";
}, 3000);
</script>
</body>
</html>
"""

# --- Login Screen ---
LOGIN_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Enter password</title>
<style>
:root{
  --bg:#000;
  --neon:#00fff7;
  --glass: rgba(255,255,255,0.03);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;}
body{
  display:flex;
  align-items:center;
  justify-content:center;
  background: linear-gradient(180deg,#000 0%, #050505 60%);
  font-family:Inter, "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
  padding:20px;
}
.card{
  width:100%;
  max-width:420px;
  background:var(--glass);
  border-radius:14px;
  padding:28px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.7), 0 0 20px rgba(0,255,247,0.03);
  text-align:center;
}
h1{margin:0 0 12px; font-size:1.4rem; text-shadow:0 0 10px rgba(0,255,247,0.04)}
form{display:flex; flex-direction:column; align-items:center}
input[type="password"]{
  width:100%;
  padding:12px 14px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,0.06);
  background:rgba(255,255,255,0.02);
  color:#fff;
  margin-bottom:12px;
  font-size:1rem;
  outline:none;
}
button{
  padding:11px 18px;
  border-radius:10px;
  border:none;
  background:linear-gradient(90deg,var(--neon), #61f3ff);
  color:#000;
  font-weight:700;
  cursor:pointer;
  width:100%;
}
small{display:block; margin-top:10px; color:rgba(255,255,255,0.6)}
</style>
</head>
<body>
<div class="card">
  <h1>Enter your password to view profile</h1>
  <form method="post">
    <input type="password" name="password" placeholder="Password" required />
    <button type="submit">Enter</button>
  </form>
  <small>Protected profile</small>
</div>
</body>
</html>
"""

# --- Profile Screen ---
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
  --bg:#000;
  --neon:#00fff7;
  --accent:#61f3ff;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{
  display:flex;
  align-items:center;
  justify-content:center;
  background: radial-gradient(1200px 600px at 20% 10%, rgba(0,255,247,0.04), transparent 6%),
              radial-gradient(1000px 500px at 85% 90%, rgba(97,243,255,0.03), transparent 6%),
              var(--bg);
  font-family:Inter, "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
  color:#fff;
  padding:24px;
}
.wrapper{
  max-width:900px;
  width:100%;
  display:flex;
  justify-content:center;
  align-items:center;
}
.card{
  background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius:18px;
  padding:28px;
  box-shadow: 0 10px 50px rgba(0,0,0,0.7);
  width:100%;
  max-width:500px;
  position:relative;
  overflow:hidden;
}
.banner{
  width:100%;
  height:200px;
  border-radius:12px;
  object-fit:cover;
  filter:brightness(.55);
}
.avatar-wrap{
  position:relative;
  margin-top:-70px;
  text-align:center;
}
.avatar{
  width:140px;height:140px;border-radius:50%;
  border:6px solid rgba(255,255,255,0.06);
  box-shadow:0 6px 30px rgba(0,255,247,0.06);
  object-fit:cover;
  background:#111;
}
.username{
  font-size:2rem;
  font-weight:700;
  margin-top:12px;
  text-shadow:0 0 18px rgba(0,255,247,0.18);
}
.verified-badge{
  display:inline-block;
  margin-left:8px;
  background:linear-gradient(90deg,var(--neon),var(--accent));
  color:#001;
  padding:4px 8px;
  border-radius:8px;
  font-size:.8rem;
  font-weight:700;
}
.info-row{
  display:flex;
  justify-content:center;
  flex-wrap:wrap;
  gap:12px;
  margin-top:20px;
}
.info-pill{
  background:rgba(255,255,255,0.03);
  padding:8px 12px;
  border-radius:10px;
  font-weight:600;
  font-size:.9rem;
}
.status-card{
  margin:30px auto 0;
  display:flex;
  align-items:center;
  gap:12px;
  background:linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
  padding:12px;
  border-radius:12px;
  width:fit-content;
  box-shadow:0 6px 30px rgba(0,0,0,0.6);
}
.status-avatar{
  width:52px;height:52px;border-radius:50%;object-fit:cover;
}
.status-text{font-weight:600;font-size:.95rem}
.status-sub{font-size:.85rem;color:rgba(255,255,255,0.6)}
</style>
</head>
<body>
<div class="wrapper">
  <div class="card">
    {% if data.banner %}
      <img src="{{ data.banner }}" class="banner">
    {% endif %}
    <div class="avatar-wrap">
      {% if data.avatar %}
        <img src="{{ data.avatar }}" class="avatar">
      {% endif %}
      <div class="username">
        {{ data.name }}
        {% if data.verified %}<span class="verified-badge">VERIFIED</span>{% endif %}
      </div>
      <div class="info-row">
        <div class="info-pill">🆔 ID: {{ data.cousin_id }}</div>
        <div class="info-pill">🏅 Rank: #{{ data.rank }}</div>
        <div class="info-pill">👀 Rep: {{ data.rep }}/100</div>
      </div>
      <div class="status-card">
        {% if data.small_avatar %}
          <img src="{{ data.small_avatar }}" class="status-avatar">
        {% elif data.avatar %}
          <img src="{{ data.avatar }}" class="status-avatar">
        {% endif %}
        <div>
          <div class="status-text">{{ data.status_name or data.name }}</div>
          <div class="status-sub">{{ data.status_text or 'currently doing nothing' }}</div>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

# --- Flask Route ---
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
            return "<h1 style='color:white;text-align:center;margin-top:50px'>❌ Wrong password!</h1>"

    if verified:
        return render_template_string(PROFILE_HTML, data=data)

    return render_template_string(LOGIN_HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
