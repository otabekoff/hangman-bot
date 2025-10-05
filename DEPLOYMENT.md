# Deployment Guide

## Deploy to Render.com

### Step 1: Prepare Your Repository

All necessary files are already in place:
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - Start command
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Excludes sensitive files

### Step 2: Create Render Account

1. Go to [Render.com](https://render.com/)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 3: Deploy the Bot

1. **Click "New +"** in the Render dashboard
2. **Select "Web Service"**
3. **Connect your `hangman-bot` repository**
4. Render will auto-detect the `render.yaml` configuration
5. **Set Environment Variables**:
   - Click "Environment" tab
   - Add variable: `BOT_TOKEN` = `your_telegram_bot_token`
6. **Click "Create Web Service"**

Render will automatically:
- Install dependencies from `requirements.txt`
- Run `python hangman-bot.py`
- Deploy your bot

### Step 4: Prevent Sleep (Keep-Alive)

⚠️ **Important**: Render's free tier sleeps after 15 minutes of inactivity.

#### Option A: UptimeRobot (Recommended)

1. **Sign up at [UptimeRobot.com](https://uptimerobot.com/)** (Free)
2. **Create New Monitor**:
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Hangman Bot`
   - URL: Your Render service URL (e.g., `https://hangman-bot.onrender.com`)
   - Monitoring Interval: `5 minutes` (free tier)
3. **Save Monitor**

UptimeRobot will ping your bot every 5 minutes, preventing sleep.

#### Option B: Cronitor

1. **Sign up at [Cronitor.io](https://cronitor.io/)** (Free tier available)
2. **Create HTTP Monitor**
3. **Set interval to 10 minutes**
4. **Add your Render URL**

#### Option C: Cron-Job.org

1. **Sign up at [cron-job.org](https://cron-job.org/)** (Free)
2. **Create Cronjob**:
   - Title: `Hangman Bot Keep-Alive`
   - URL: Your Render service URL
   - Execution: Every 10 minutes
3. **Save**

### Step 5: Add Health Check Endpoint (Optional)

To make keep-alive monitoring more reliable, you can add a simple health check endpoint to your bot. This creates a lightweight HTTP server that responds to pings without affecting the bot.

**Note**: This requires modifying `hangman-bot.py` to add a web server. Let me know if you want this feature.

### Step 6: Monitor Your Bot

1. **Check Render Logs**:
   - Go to your service dashboard
   - Click "Logs" tab
   - Verify bot is running: `INFO:root:Starting bot...`

2. **Test Your Bot**:
   - Open Telegram
   - Search for your bot
   - Send `/start` command

### Troubleshooting

#### Bot Not Responding
- Check Render logs for errors
- Verify `BOT_TOKEN` environment variable is set correctly
- Ensure bot is running: look for "Starting bot..." in logs

#### Service Keeps Sleeping
- Verify UptimeRobot monitor is active
- Check monitor interval (should be 5-10 minutes)
- Render free tier has 750 hours/month limit

#### Build Fails
- Check `requirements.txt` for correct package versions
- Verify Python version in `runtime.txt` is supported
- Review build logs in Render dashboard

### Important Notes

⚠️ **Free Tier Limitations**:
- 750 hours/month (31.25 days - enough for 24/7 with one service)
- Spins down after 15 minutes of inactivity
- 30-60 second cold start when waking up
- Limited to 512 MB RAM

✅ **Advantages**:
- Easy deployment from GitHub
- Automatic SSL certificate
- Free PostgreSQL database (if needed later)
- Auto-deploys on git push

### Upgrading (Optional)

For production use without sleep:
- **Starter Plan**: $7/month
- No sleep, always online
- More resources (1 GB RAM)

### Alternative: Using Webhooks

If you want better performance on Render, consider converting to webhooks instead of long polling. Webhooks:
- ✅ More efficient
- ✅ No sleep issues (only runs when messages arrive)
- ✅ Better for free tier

Let me know if you want help converting to webhooks!

---

## Quick Deploy Checklist

- [ ] Repository pushed to GitHub
- [ ] Render account created and connected to GitHub
- [ ] Service created on Render
- [ ] `BOT_TOKEN` environment variable set
- [ ] Service deployed successfully
- [ ] Bot responds to `/start` in Telegram
- [ ] UptimeRobot monitor configured (every 5-10 minutes)
- [ ] Monitor confirmed working (check UptimeRobot dashboard)

---

**Need Help?** Check the [Render Documentation](https://render.com/docs) or open an issue on GitHub.

© 2025 Otabek Sadiridinov
