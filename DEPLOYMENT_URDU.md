# 🚀 Deployment Guide (Urdu/Hindi)

## 📋 Kya Deploy Karenge?

- **Frontend (Next.js):** Vercel per
- **Backend (FastAPI):** Render per ⭐ RECOMMENDED
- **Database:** Neon PostgreSQL (Already setup ✅)

---

## 🎯 Step by Step Guide

### Part 1: GitHub Setup

#### 1. Git Initialize Karein (Agar nahi kiya)

```bash
cd D:\Phase_2\todo_full_stack_web_application

git init
git add .
git commit -m "TaskFlow App - Ready for deployment"
```

#### 2. GitHub Per Repository Banayen

1. **GitHub.com** per jao
2. **"New Repository"** click karo
3. **Name:** `taskflow-app`
4. **Public** select karo
5. **Create Repository** click karo

#### 3. Code Push Karo

```bash
git remote add origin https://github.com/YOUR_USERNAME/taskflow-app.git
git branch -M main
git push -u origin main
```

---

### Part 2: Backend Deploy (Render)

#### Step 1: Render Account Banayen

1. **Render.com** per jao
2. **Sign Up** karo (GitHub se login karo)

#### Step 2: Web Service Banayen

1. **"New +"** click karo
2. **"Web Service"** select karo
3. **"Connect GitHub"** karo
4. **Repository:** `taskflow-app` select karo

#### Step 3: Configuration

**Service Details:**
- **Name:** `taskflow-api`
- **Region:** Singapore (closest)
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- **Free** select karo

#### Step 4: Environment Variables Add Karo

**"Advanced"** → **"Add Environment Variable"** click karo:

```bash
# Database
DATABASE_URL
postgresql://neondb_owner:npg_xuzhSIR36Tpc@ep-curly-poetry-a11nqtzo-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# JWT Settings
JWT_SECRET_KEY
aapka-secret-key-yaha-daalo-32-characters-se-zyada

JWT_ALGORITHM
HS256

JWT_ACCESS_TOKEN_EXPIRE_HOURS
24

# CORS (Pehle localhost, baad mein Vercel URL)
CORS_ORIGINS
http://localhost:3000

# Debug
DEBUG
False
```

#### Step 5: Deploy Karo

1. **"Create Web Service"** click karo
2. **Wait:** 5-10 minutes
3. **URL milega:** `https://taskflow-api.onrender.com`

#### Step 6: Database Migration Run Karo

1. Render dashboard mein jao
2. **"taskflow-api"** service click karo
3. **"Shell"** tab open karo
4. Ye commands run karo:

```bash
cd backend
alembic upgrade head
```

✅ **Backend Ready!**

**Test Karo:** `https://taskflow-api.onrender.com/health`

---

### Part 3: Frontend Deploy (Vercel)

#### Step 1: Frontend Files Update Karo

**File:** `frontend/.env.local`

```bash
NEXT_PUBLIC_API_URL=https://taskflow-api.onrender.com
```

**Git commit karo:**

```bash
git add .
git commit -m "Update API URL for production"
git push origin main
```

#### Step 2: Vercel Account Banayen

1. **Vercel.com** per jao
2. **Sign Up** karo (GitHub se login karo)

#### Step 3: Project Import Karo

1. **"Add New"** → **"Project"** click karo
2. **Repository:** `taskflow-app` select karo
3. **Import** karo

#### Step 4: Configuration

**Framework:**
- Automatically **Next.js** detect ho jayega ✅

**Root Directory:**
- **"Edit"** click karo
- **`frontend`** select karo

**Environment Variables:**
- **"Add"** click karo
- **Key:** `NEXT_PUBLIC_API_URL`
- **Value:** `https://taskflow-api.onrender.com`

#### Step 5: Deploy Karo

1. **"Deploy"** click karo
2. **Wait:** 2-3 minutes
3. **URL milega:** `https://taskflow-app-xyz.vercel.app`

✅ **Frontend Ready!**

---

### Part 4: Final Setup

#### Backend CORS Update Karo

1. **Render dashboard** mein jao
2. **"taskflow-api"** click karo
3. **"Environment"** tab open karo
4. **CORS_ORIGINS** edit karo:

```bash
https://taskflow-app-xyz.vercel.app,http://localhost:3000
```

5. **"Save Changes"** - Auto redeploy hoga

---

## ✅ Testing

### 1. Frontend Test Karo

**URL:** `https://taskflow-app-xyz.vercel.app`

- ✅ Register karo
- ✅ Login karo
- ✅ Task banayen
- ✅ Task complete karo
- ✅ Task delete karo
- ✅ Logout karo

### 2. Backend Test Karo

**Health Check:** `https://taskflow-api.onrender.com/health`

**API Docs:** `https://taskflow-api.onrender.com/docs`

---

## 🎉 Ho Gaya!

Aapka app ab **LIVE** hai:

- 🌐 **Frontend:** https://taskflow-app-xyz.vercel.app
- 🔧 **Backend:** https://taskflow-api.onrender.com
- 📊 **Database:** Neon (Already running)

---

## 🔄 Update Kaise Karein?

Jab bhi changes karo:

```bash
git add .
git commit -m "Changes ka description"
git push origin main
```

**Auto Deploy Ho Jayega!** ✅
- Vercel automatically frontend deploy karega
- Render automatically backend deploy karega

---

## ⚠️ Important Notes

### Render Free Tier

- ⚠️ **15 minutes** inactive rehne ke baad service **sleep** ho jati hai
- ⚠️ **First request** slow hogi (30-60 seconds) - cold start
- ✅ Phir fast chal jayegi

### Solution: Keep Alive

Agar service ko active rakhna hai, use **cron-job.org** ya **UptimeRobot**:
- Har 10 minutes mein health endpoint hit karo
- Service sleep nahi hogi

---

## 🐛 Common Issues

### Issue 1: Frontend "Failed to fetch"

**Reason:** Backend URL galat hai
**Fix:** `.env.local` check karo, sahi URL daalo

### Issue 2: CORS Error

**Reason:** Frontend URL backend CORS mein nahi hai
**Fix:** Render mein CORS_ORIGINS update karo

### Issue 3: Backend Error 500

**Reason:** Environment variables missing
**Fix:** Render dashboard → Environment → Sab variables check karo

### Issue 4: Database Connection Failed

**Reason:** DATABASE_URL galat hai
**Fix:** Neon dashboard se correct URL copy karo

---

## 📱 Share Karo

Ab aap:
- ✅ Link share kar saktay ho
- ✅ Portfolio mein add kar saktay ho
- ✅ Resume mein mention kar saktay ho
- ✅ Friends ko dikha saktay ho

---

## 💡 Pro Tips

1. **Custom Domain** laga saktay ho (optional)
2. **Analytics** add kar saktay ho (Google Analytics)
3. **SEO** improve kar saktay ho
4. **Performance** monitor kar saktay ho

---

## 📞 Help Chahiye?

**Documentation:**
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs

**Common Commands:**

```bash
# Local test
cd backend && uvicorn src.main:app --reload
cd frontend && npm run dev

# Git push (auto-deploy)
git add .
git commit -m "Update"
git push origin main

# Check logs (Render dashboard mein)
# Check logs (Vercel dashboard mein)
```

---

## 🎊 Mubarak Ho!

Aapka **TaskFlow** app ab:
- ✅ Internet per live hai
- ✅ Kahin se bhi access ho sakta hai
- ✅ Professional infrastructure per chal raha hai
- ✅ HTTPS se secure hai
- ✅ Production ready hai

**Enjoy! 🚀**

---

**Status:** Ready to Deploy ✅
**Updated:** December 2024
