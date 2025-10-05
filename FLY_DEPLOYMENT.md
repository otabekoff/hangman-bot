# Deploy to Fly.io

## Why Fly.io?

✅ **No sleep** - Your bot stays online 24/7  
✅ **Free tier** - 3 shared VMs with 256MB RAM  
✅ **Fast deployment** - Global edge network  
✅ **Better for bots** - Designed for long-running processes  
✅ **Simple scaling** - Easy to upgrade when needed  

---

## Prerequisites

1. **Fly.io Account**: Sign up at https://fly.io/
2. **Credit Card**: Required for verification (won't be charged on free tier)
3. **Fly CLI**: Install the Fly command-line tool

### Install Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Verify installation:**
```bash
fly version
```

---

## Deployment Steps

### Step 1: Login to Fly.io

```bash
fly auth login
```

This opens your browser for authentication.

### Step 2: Launch Your App

From your project directory, run:

```bash
fly launch
```

**Answer the prompts:**
- **App Name**: Press Enter to use `hangman-bot` (or choose your own)
- **Region**: Choose closest to your users (e.g., `iad` for US East)
- **PostgreSQL**: No (we don't need a database)
- **Redis**: No (we don't need Redis)
- **Deploy now**: No (we need to set secrets first)

This creates `fly.toml` configuration file (already provided).

### Step 3: Set Your Bot Token

Set the `BOT_TOKEN` as a secret (encrypted environment variable):

```bash
fly secrets set BOT_TOKEN=your_telegram_bot_token_here
```

**Important**: Replace `your_telegram_bot_token_here` with your actual token from @BotFather.

### Step 4: Deploy Your Bot

```bash
fly deploy
```

This will:
1. Build your Docker container
2. Upload to Fly.io
3. Start your bot
4. Make it accessible globally

### Step 5: Check Status

```bash
fly status
```

You should see your app running with status `running`.

### Step 6: View Logs

Monitor your bot in real-time:

```bash
fly logs
```

You should see:
```
INFO:root:Starting bot...
```

---

## Management Commands

### View App Status
```bash
fly status
```

### View Real-time Logs
```bash
fly logs
```

### Restart Your Bot
```bash
fly apps restart hangman-bot
```

### SSH into Container (debugging)
```bash
fly ssh console
```

### Scale Resources (if needed)
```bash
# Increase memory to 512MB
fly scale memory 512

# Scale to 2 VMs for redundancy
fly scale count 2
```

### View Secrets
```bash
fly secrets list
```

### Update Bot Token
```bash
fly secrets set BOT_TOKEN=new_token_here
```

### Stop Your Bot
```bash
fly apps stop hangman-bot
```

### Start Your Bot
```bash
fly apps start hangman-bot
```

### Delete App (careful!)
```bash
fly apps destroy hangman-bot
```

---

## Configuration Details

### fly.toml Explained

```toml
app = "hangman-bot"              # Your app name
primary_region = "iad"           # Region (US East)

[build]
  builder = "paketobuildpacks/builder:base"  # Auto-detects Python

[env]
  PORT = "8080"                  # Not used by bot, but good practice

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = false     # Keep running always
  auto_start_machines = true
  min_machines_running = 1       # Always have 1 VM running

[[vm]]
  cpu_kind = "shared"            # Free tier
  cpus = 1                       # 1 CPU core
  memory_mb = 256                # 256MB RAM (free tier)
```

### Dockerfile Explained

- Uses Python 3.11 slim for smaller image
- Copies only necessary files (excludes via `.dockerignore`)
- Installs dependencies efficiently
- Runs `python hangman-bot.py` on startup

---

## Free Tier Limits

Fly.io free tier includes:

- ✅ **3 shared-cpu VMs** (256MB RAM each)
- ✅ **3GB persistent storage**
- ✅ **160GB outbound bandwidth/month**
- ✅ **No sleep** - stays running 24/7

**For this bot**: You'll use 1 VM, leaving 2 for other projects!

---

## Troubleshooting

### Bot Not Starting

**Check logs:**
```bash
fly logs
```

**Common issues:**
- Missing `BOT_TOKEN` secret
- Wrong bot token
- Syntax errors in code

### Bot Token Issues

**Verify secrets:**
```bash
fly secrets list
```

**Update token:**
```bash
fly secrets set BOT_TOKEN=correct_token_here
```

### Deployment Fails

**Check fly.toml syntax:**
```bash
fly config validate
```

**Rebuild from scratch:**
```bash
fly deploy --build-only
```

### Memory Issues

**Increase memory if needed:**
```bash
fly scale memory 512
```

This moves to paid tier but gives more resources.

### Connection Issues

**Verify region:**
```bash
fly regions list
```

**Add backup region:**
```bash
fly regions add lhr  # London
```

---

## Monitoring

### View Dashboard
Visit: https://fly.io/dashboard

Here you can:
- Monitor app health
- View metrics (CPU, memory, requests)
- Check deployment history
- Manage secrets

### Set Up Alerts (Optional)

1. Go to dashboard
2. Navigate to your app
3. Click "Monitoring" tab
4. Configure alerts for downtime

---

## Updating Your Bot

### Deploy Changes

After making code changes:

```bash
git add .
git commit -m "Update bot features"
git push origin main
fly deploy
```

### Automatic Deployments (Optional)

Set up GitHub Actions for auto-deployment on push:

Create `.github/workflows/fly-deploy.yml`:
```yaml
name: Fly Deploy
on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy app
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Get `FLY_API_TOKEN` from: https://fly.io/user/personal_access_tokens

---

## Cost Optimization

### Stay on Free Tier

- Use only 1 VM (default)
- Monitor bandwidth usage
- Keep memory at 256MB

### If You Exceed Free Tier

Fly.io will email you. Options:
1. Add payment method (charges only for overage)
2. Scale down resources
3. Delete unused apps

**Typical costs** (if needed):
- Extra VM: ~$2/month
- Extra memory (512MB): ~$4/month
- Bandwidth overage: Very cheap

---

## Comparison: Render vs Fly.io

| Feature | Render | Fly.io |
|---------|--------|--------|
| **Sleep** | 15 min inactivity | Never |
| **Cold start** | 30-60 seconds | Instant |
| **Free tier** | 750 hours/month | 3 VMs 24/7 |
| **Regions** | US only (free) | Global |
| **Setup** | Easier | Slightly harder |
| **Best for** | Webhooks | Long polling |

**Verdict**: Fly.io is better for Telegram bots using long polling! ✅

---

## Security Best Practices

1. **Never commit secrets** - Use `fly secrets set`
2. **Rotate tokens** - Change `BOT_TOKEN` periodically
3. **Monitor logs** - Watch for suspicious activity
4. **Use latest images** - Keep Python/dependencies updated
5. **Limit access** - Use Fly.io teams for collaboration

---

## Next Steps

After deployment:

1. ✅ Test your bot in Telegram (`/start`)
2. ✅ Monitor logs for errors
3. ✅ Set up monitoring alerts
4. ✅ Document your deployment process
5. ✅ Consider adding a health check endpoint

---

## Support

- **Fly.io Docs**: https://fly.io/docs/
- **Community Forum**: https://community.fly.io/
- **Status Page**: https://status.flyio.net/

---

## Quick Command Reference

```bash
# Deploy
fly launch                    # First time setup
fly deploy                    # Deploy changes
fly secrets set KEY=value     # Set environment variable

# Monitor
fly status                    # Check app status
fly logs                      # View logs
fly logs -a hangman-bot       # Logs for specific app

# Manage
fly apps list                 # List all apps
fly apps restart              # Restart app
fly apps destroy              # Delete app

# Scale
fly scale count 2             # Run 2 VMs
fly scale memory 512          # Increase RAM

# Debug
fly ssh console               # SSH into container
fly ssh sftp shell            # File transfer
```

---

**Ready to deploy?** Run `fly launch` and follow the steps above! 🚀

© 2025 Otabek Sadiridinov
