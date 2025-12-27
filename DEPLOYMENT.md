# 🚀 Deployment Guide - TaskFlow App

Complete step-by-step deployment guide for your Todo Full-Stack Application.

---

## 📋 Overview

- **Frontend:** Vercel (Next.js)
- **Backend:** Render (FastAPI) - RECOMMENDED ⭐
- **Database:** Neon PostgreSQL (Already Setup) ✅

> **Note:** Vercel is NOT recommended for FastAPI backend. Use Render instead for better Python support.

---

## 🎯 Quick Links

After deployment, you'll have:
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-api.onrender.com`
- Database: Already on Neon ✅

---

# Part 1: Backend Deployment on Render 🐍

## Step 1: Prepare Backend for Deployment

### 1.1 Create `requirements.txt` (Already exists ✅)

Your backend already has this file at `backend/requirements.txt`

### 1.2 Create `render.yaml` Configuration

Create this file in the root of your project:

```bash
# In root directory (D:\Phase_2\todo_full_stack_web_application\)
```

**File: `render.yaml`**
```yaml
services:
  - type: web
    name: taskflow-api
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && uvicorn src.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: JWT_SECRET_KEY
        sync: false
      - key: JWT_ALGORITHM
        value: HS256
      - key: JWT_ACCESS_TOKEN_EXPIRE_HOURS
        value: 24
      - key: CORS_ORIGINS
        sync: false
      - key: DEBUG
        value: False
```

### 1.3 Update Backend for Production

**File: `backend/src/core/config.py`** (Already correct ✅)

Make sure your config supports production:

```python
class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_hours: int = 24
    cors_origins: str
    debug: bool = False

    class Config:
        env_file = ".env"
```

---

## Step 2: Deploy Backend to Render

### 2.1 Create GitHub Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - TaskFlow App"

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/taskflow-app.git
git branch -M main
git push -u origin main
```

### 2.2 Deploy on Render

1. **Go to:** https://render.com
2. **Sign up/Login** with GitHub
3. Click **"New +"** → **"Web Service"**
4. **Connect your repository:** `taskflow-app`
5. **Configure:**
   - **Name:** `taskflow-api`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

6. **Add Environment Variables:**

   Click **"Advanced"** → **"Add Environment Variable"**

   ```
   DATABASE_URL = postgresql://neondb_owner:npg_xuzhSIR36Tpc@ep-curly-poetry-a11nqtzo-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

   JWT_SECRET_KEY = your-super-secret-key-min-32-characters-long-change-this-in-production

   JWT_ALGORITHM = HS256

   JWT_ACCESS_TOKEN_EXPIRE_HOURS = 24

   CORS_ORIGINS = https://your-frontend.vercel.app

   DEBUG = False
   ```

7. Click **"Create Web Service"**

8. **Wait 5-10 minutes** for deployment

9. **Your API will be live at:** `https://taskflow-api.onrender.com`

10. **Test it:** `https://taskflow-api.onrender.com/health`

---

## Step 3: Run Database Migration on Render

After deployment, you need to run migrations:

1. Go to your Render dashboard
2. Click on your service **"taskflow-api"**
3. Go to **"Shell"** tab
4. Run these commands:

```bash
cd backend
alembic upgrade head
```

✅ Database tables are now created!

---

# Part 2: Frontend Deployment on Vercel 🌐

## Step 1: Prepare Frontend for Deployment

### 1.1 Update Environment Variables

**File: `frontend/.env.local`**

Update your API URL:

```bash
NEXT_PUBLIC_API_URL=https://taskflow-api.onrender.com
```

### 1.2 Update `frontend/next.config.js` (if needed)

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
}

module.exports = nextConfig
```

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Push Code to GitHub (if not already done)

```bash
git add .
git commit -m "Update API URL for production"
git push origin main
```

### 2.2 Deploy on Vercel

1. **Go to:** https://vercel.com
2. **Sign up/Login** with GitHub
3. Click **"Add New"** → **"Project"**
4. **Import** your repository: `taskflow-app`
5. **Configure:**
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (auto-filled)
   - **Output Directory:** `.next` (auto-filled)

6. **Add Environment Variables:**

   Click **"Environment Variables"**

   ```
   NEXT_PUBLIC_API_URL = https://taskflow-api.onrender.com
   ```

7. Click **"Deploy"**

8. **Wait 2-3 minutes** for deployment

9. **Your app will be live at:** `https://taskflow-app-xxxx.vercel.app`

---

## Step 3: Update CORS Settings

After frontend is deployed, update backend CORS:

### 3.1 Update Backend Environment on Render

1. Go to Render dashboard
2. Click on **"taskflow-api"**
3. Go to **"Environment"** tab
4. Update **CORS_ORIGINS**:

```
CORS_ORIGINS = https://taskflow-app-xxxx.vercel.app,http://localhost:3000
```

5. Click **"Save Changes"**
6. Service will auto-redeploy

---

## ✅ Deployment Complete!

Your app is now live:

- **Frontend:** https://taskflow-app-xxxx.vercel.app
- **Backend API:** https://taskflow-api.onrender.com
- **API Docs:** https://taskflow-api.onrender.com/docs

---

# 🔧 Post-Deployment Checklist

## Test Your Deployed App

1. ✅ Open frontend URL
2. ✅ Register a new account
3. ✅ Login
4. ✅ Create tasks
5. ✅ Mark tasks complete
6. ✅ Delete tasks
7. ✅ Logout

## Check Backend Health

1. ✅ Visit: `https://taskflow-api.onrender.com/health`
2. ✅ Should return: `{"status": "healthy"}`
3. ✅ Visit: `https://taskflow-api.onrender.com/docs`
4. ✅ Should show Swagger API documentation

---

# 🔒 Security Best Practices

## 1. Generate Strong JWT Secret

```bash
# Generate a new secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update this in Render environment variables.

## 2. Environment Variables

Never commit `.env` files to GitHub. Always use:
- `.env.local` for local development
- Platform environment variables for production

## 3. Database Security

Your Neon database is already secure with SSL enabled ✅

---

# 🐛 Troubleshooting

## Frontend Issues

### Issue: "Failed to fetch"
**Solution:** Check if backend URL is correct in `NEXT_PUBLIC_API_URL`

### Issue: CORS Error
**Solution:** Make sure frontend URL is in backend `CORS_ORIGINS`

## Backend Issues

### Issue: "Application Error"
**Solution:** Check Render logs in dashboard → Logs tab

### Issue: Database connection failed
**Solution:** Verify `DATABASE_URL` environment variable is correct

### Issue: 500 Internal Server Error
**Solution:** Check Render logs for Python errors

---

# 📊 Monitoring & Logs

## Render Logs

1. Go to Render dashboard
2. Click on your service
3. Click **"Logs"** tab
4. View real-time logs

## Vercel Logs

1. Go to Vercel dashboard
2. Click on your project
3. Click **"Deployments"**
4. Click on a deployment
5. View **"Build Logs"** and **"Function Logs"**

---

# 🔄 Updating Your App

## Update Frontend

1. Make changes locally
2. Test locally
3. Commit and push to GitHub:

```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

4. Vercel will auto-deploy ✅

## Update Backend

1. Make changes locally
2. Test locally
3. Commit and push to GitHub:

```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

4. Render will auto-deploy ✅

---

# 💰 Free Tier Limits

## Render (Free)

- ✅ 750 hours/month
- ⚠️ Service sleeps after 15 min of inactivity
- ⚠️ Cold start: 30-60 seconds on first request
- ✅ Auto-deploy from GitHub

## Vercel (Free - Hobby)

- ✅ Unlimited websites
- ✅ 100 GB bandwidth/month
- ✅ Auto-deploy from GitHub
- ✅ Custom domains

## Neon (Free)

- ✅ 3 GB storage
- ✅ Unlimited compute hours
- ✅ PostgreSQL database

---

# 🌟 Custom Domain (Optional)

## Add Custom Domain to Vercel

1. Go to Vercel dashboard
2. Click on your project
3. Go to **"Settings"** → **"Domains"**
4. Click **"Add"**
5. Enter your domain: `yourdomain.com`
6. Follow DNS configuration instructions
7. Update backend CORS_ORIGINS with new domain

## Add Custom Domain to Render

1. Go to Render dashboard
2. Click on your service
3. Go to **"Settings"** → **"Custom Domain"**
4. Click **"Add Custom Domain"**
5. Enter your domain
6. Update DNS records as instructed

---

# 📝 Environment Variables Reference

## Backend (Render)

```bash
DATABASE_URL=postgresql://...  # Your Neon database URL
JWT_SECRET_KEY=...  # Strong random string (32+ chars)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24
CORS_ORIGINS=https://your-app.vercel.app
DEBUG=False
```

## Frontend (Vercel)

```bash
NEXT_PUBLIC_API_URL=https://your-api.onrender.com
```

---

# 🎉 Success!

Your TaskFlow app is now:
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Running on professional infrastructure
- ✅ Auto-deploying on git push
- ✅ Secure with HTTPS
- ✅ Production ready

**Share your live app URL with friends and add it to your portfolio!** 🚀

---

# 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Neon Docs:** https://neon.tech/docs

---

**Last Updated:** December 2024
**Status:** Production Ready ✅
