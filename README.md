# Utter — Open Source Text-to-Speech (Split Deployment: Railway + Vercel)

100% free, 100% open source. Backend Railway pe, Frontend Vercel pe.

## Stack
| Component | Kaam | Hosted On |
|---|---|---|
| Flask + Gunicorn | Backend API | Railway |
| espeak-ng | Text -> speech engine | Railway (Docker) |
| ffmpeg | WAV -> MP3 converter | Railway (Docker) |
| HTML/CSS/JS | Frontend website | Vercel |

---

# STEP BY STEP — Backend Deploy on Railway

## Step 1: Repo Structure Samjho
Tumhare GitHub repo mein 2 folders honge:
```
your-repo/
  backend/          <- Railway isko deploy karega
    app.py
    Dockerfile
    requirements.txt
    railway.json
  frontend/         <- Vercel isko deploy karega
    index.html
```

## Step 2: Railway Pe New Project Banao
1. [railway.com](https://railway.com) pe login karo
2. **New Project** > **Deploy from GitHub repo**
3. Apna repo select karo

## Step 3: Root Directory Set Karo (IMPORTANT)
Kyunki backend ek subfolder mein hai:
1. Project settings mein jaao > **Settings** tab
2. **Root Directory** mein likho: `backend`
3. Railway automatically Dockerfile detect kar lega (espeak-ng + ffmpeg + gunicorn sab install ho jayega)

## Step 4: Public Domain Generate Karo
1. **Settings** > **Networking** > **Generate Domain** dabao
2. URL milega jaisa: `https://utter-backend-production.up.railway.app`
3. **Ye URL copy kar lo** — agle step mein chahiye hoga

## Step 5: Test Karo
Browser mein ye URL kholo: `https://your-backend.up.railway.app/`
Agar koi response aaye (blank ya JSON), matlab backend live hai.

---

# STEP BY STEP — Frontend Deploy on Vercel

## Step 1: index.html Mein Backend URL Daalo
`frontend/index.html` file kholo, ye line dhundo (near top of `<script>`):
```js
const API_BASE_URL = "https://YOUR-RAILWAY-BACKEND-URL.up.railway.app";
```
Isko apne Railway URL se replace karo (Step 4 se copy kiya tha), phir GitHub pe push karo:
```bash
git add .
git commit -m "Add Railway backend URL"
git push
```

## Step 2: Vercel Pe Import Karo
1. [vercel.com](https://vercel.com) pe login karo (GitHub se)
2. **Add New** > **Project**
3. Apna repo select karo, **Import** dabao

## Step 3: Root Directory Set Karo (IMPORTANT)
1. **Root Directory** field mein `frontend` likho/select karo
2. Framework Preset: **Other** (kyunki plain HTML hai)
3. **Deploy** dabao

## Step 4: Live URL Milega
Kuch aisa: `https://utter-tts.vercel.app` — isko kholo, text likho, Generate Speech dabao. Request Vercel se Railway backend ko jayegi, MP3 wapas aayegi.

---

# Kyun Alag Backend/Frontend?
- **Vercel** static sites (HTML/CSS/JS) ke liye best hai — bahut fast, free, unlimited bandwidth
- **Railway** backend/server code (Python + system tools) chalane ke liye best hai — Docker support karta hai
- Dono ko CORS (Cross-Origin Resource Sharing) se connect kiya hai — `app.py` mein `flask-cors` already add hai, isliye Vercel se Railway ko call karna kaam karega bina kisi extra setup ke

---

# Local Testing (Deploy Se Pehle)
```bash
# Backend
cd backend
pip install -r requirements.txt --break-system-packages
python3 app.py
# Browser mein http://localhost:5000 test karo

# Frontend (agar alag test karna hai)
cd ../frontend
# index.html mein API_BASE_URL ko http://localhost:5000 kar do temporarily
# phir index.html ko browser mein directly kholo
```

---

# Voices Available
English (US/UK/Scotland), Hindi (2 styles), Spanish, French, German, Arabic.
Zyada voices ke liye: `espeak-ng --voices` chalao, phir `app.py` ke `VOICES` dictionary mein add karo.

---

# Troubleshooting
| Problem | Solution |
|---|---|
| CORS error in browser console | Confirm `flask-cors` `requirements.txt` mein hai aur Railway pe redeploy hua hai |
| "Failed to fetch" | `API_BASE_URL` sahi hai check karo — https:// se shuru hona chahiye, end mein slash (/) nahi |
| Railway build fail | Root Directory `backend` set hai confirm karo |
| Vercel 404 | Root Directory `frontend` set hai confirm karo |
| Railway free tier limit | Railway free tier mein $5 free credit/month milta hai, usage-based hai |
