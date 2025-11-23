# Deployment Guide - DigitalOcean Droplet

## Prerequisites

1. **DigitalOcean Droplet** with Ubuntu
2. **Docker** installed on the droplet
3. **GitHub Repository Secrets** configured

## Server Setup (One-time)

### 1. Install Docker on Droplet

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installation
docker --version
```

### 2. Create Project Directory

```bash
# Create directory for the bot
mkdir -p ~/hangman-bot
cd ~/hangman-bot
```

### 3. Setup SSH Key for GitHub Actions

```bash
# Generate SSH key pair
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_deploy -N ""

# Add public key to authorized_keys
cat ~/.ssh/github_deploy.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Display private key (copy this for GitHub secrets)
cat ~/.ssh/github_deploy
```

## GitHub Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these 5 secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `SSH_PRIVATE_KEY` | Full private key content from `~/.ssh/github_deploy` | `-----BEGIN OPENSSH PRIVATE KEY-----`<br>`...`<br>`-----END OPENSSH PRIVATE KEY-----` |
| `SSH_HOST` | Your droplet IP address | `123.456.789.012` |
| `SSH_USER` | SSH username (usually `root`) | `root` |
| `PROJECT_DIR` | Path to project directory on server | `/root/hangman-bot` |
| `BOT_TOKEN` | Your Telegram bot token from @BotFather | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |

## How It Works

### Automatic Deployment

Every push to `main` branch triggers:

1. **Checkout code** from repository
2. **Setup SSH** using private key
3. **Sync files** via rsync (excluding .git, .github, cache files, .env)
4. **Build Docker image** (uses cache for faster builds)
5. **Stop old container** (if running)
6. **Start new container** with BOT_TOKEN from GitHub secrets

### Docker Layer Caching

The Dockerfile is optimized to cache dependencies:
- `requirements.txt` is copied first
- Dependencies are installed (cached unless requirements change)
- Application code is copied last (changes frequently)

This means:
- **First deployment**: ~40-50 seconds (downloads all packages)
- **Subsequent deployments**: ~10-15 seconds (uses cached layers)

### Zero Downtime Strategy

The workflow:
1. Builds new image while old container still runs
2. Stops old container only after new image is ready
3. Starts new container immediately
4. Minimal downtime (~2-3 seconds during container swap)

## Manual Deployment (Optional)

If you need to deploy manually:

```bash
# SSH into your droplet
ssh root@your_droplet_ip

# Navigate to project directory
cd ~/hangman-bot

# Pull latest changes (if you have git setup)
git pull

# Or manually update files

# Rebuild and restart
docker stop hangman-bot
docker rm hangman-bot
docker build -t hangman-bot:latest .
docker run -d \
  --name hangman-bot \
  --restart unless-stopped \
  -p 8080:8080 \
  -e BOT_TOKEN="your_bot_token_here" \
  hangman-bot:latest

# Check status
docker ps
docker logs hangman-bot
```

## Monitoring

### Check Container Status

```bash
# View running containers
docker ps

# View bot logs
docker logs hangman-bot

# Follow logs in real-time
docker logs -f hangman-bot

# View last 100 lines
docker logs --tail 100 hangman-bot
```

### Health Check

```bash
# Test health endpoint
curl http://localhost:8080/health

# Or from outside
curl http://your_droplet_ip:8080/health
```

## Troubleshooting

### Container Not Starting

```bash
# Check logs for errors
docker logs hangman-bot

# Common issues:
# - Missing BOT_TOKEN in GitHub secrets
# - Invalid bot token
# - Port already in use
```

### Deployment Fails

**Error: `permission denied`**
- Check SSH key permissions (should be 600)
- Verify user has Docker access

**Error: `port already allocated`**
- Another container using port 8080
- Stop conflicting container: `docker stop $(docker ps -q --filter "publish=8080")`

### Force Rebuild (No Cache)

```bash
docker build --no-cache -t hangman-bot:latest .
```

## Updating Bot Token

Go to GitHub repository → Settings → Secrets and variables → Actions

Edit the `BOT_TOKEN` secret with the new value. The next deployment will automatically use the updated token.

## Security Notes

- ✅ SSH keys used instead of passwords
- ✅ BOT_TOKEN stored securely in GitHub secrets (not in code or server files)
- ✅ Secrets never exposed in logs or workflow outputs
- ✅ Container restart policy (survives server reboots)
- ✅ Non-root user in container (Python slim image)
- ⚠️ Consider using firewall rules to limit port access
- ⚠️ Consider using secrets management service for production

## Cost Optimization

- Basic droplet ($4-6/month) is sufficient for this bot
- Docker layer caching reduces bandwidth usage
- Health checks keep droplet active
- Auto-restart handles crashes automatically
