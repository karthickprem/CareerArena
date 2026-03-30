# CareerArena Hosting Guide & Cost Breakdown

## What You Need

| Component | What | Options |
|-----------|------|---------|
| Domain | careerarena.in or placeright.in | GoDaddy / Namecheap / Cloudflare |
| VPS Server | Runs both backend (FastAPI) + frontend (Next.js) | Hetzner / DigitalOcean / AWS Lightsail |
| Database | PostgreSQL (production) or keep SQLite for pilot | Supabase free tier or self-host on VPS |
| LLM API | GPT-4o / GPT-4o-mini calls | OpenAI API / AMD LLM Gateway |
| SSL | HTTPS certificate | Let's Encrypt (free) |
| Reverse Proxy | Route traffic to backend + frontend | Nginx (free) |

## Monthly Cost Estimate

| Item | Cost (INR/month) | Notes |
|------|-------------------|-------|
| Domain | ~Rs 80/mo (~Rs 900/yr) | .in domain |
| VPS (4 vCPU, 8GB RAM) | Rs 1,500 - 3,000 | Hetzner CX32 (~Rs 1,500) or DigitalOcean ($12 = ~Rs 1,000) |
| LLM API | Rs 5,000 - 15,000 | Depends on usage. ~Rs 73/active student/month after optimization |
| SSL | Free | Let's Encrypt via Certbot |
| Google Cloud TTS | Rs 0-500 | Free tier covers ~1M characters/month |
| **Total (pilot, 50 students)** | **Rs 7,000 - 12,000/mo** | |
| **Total (100 students)** | **Rs 10,000 - 20,000/mo** | LLM cost scales linearly |

## Cheapest Viable Setup (Pilot)

- Hetzner CX32 (4 vCPU, 8GB RAM) — ~Rs 1,500/mo
- SQLite for database (no separate DB cost)
- GPT-4o-mini for most calls, GPT-4o only for final evaluation
- Let's Encrypt for SSL
- Nginx as reverse proxy

## Deployment Steps

1. Buy domain (careerarena.in or placeright.in)
2. Provision VPS (Hetzner/DigitalOcean)
3. Point domain DNS to VPS IP
4. Clone repo on VPS
5. `pip install -r requirements.txt`
6. `cd frontend && npm install && npm run build`
7. Configure Nginx reverse proxy
8. Set up SSL with Certbot
9. Start backend + frontend with PM2/systemd
10. Set `.env` with your LLM API key

## Git Push Command

```bash
git push -u origin main
```

It will prompt for your GitHub username and password (use a Personal Access Token as the password).

## TODO

- [ ] Create Nginx config file
- [ ] Create systemd service files for backend + frontend
- [ ] Create `.env.example` template
- [ ] Create deploy.sh automation script
