# Kyle 🎮📚

AI-Powered Job Application Assistant for Charles Siboto

## Features

- 📱 **Mobile-friendly PWA** - Install on your phone like an app
- 🔐 **Password protection** - Optional security for deployment
- 👤 **Complete profile** - Experience, skills, education, links
- 📝 **5 Cover letter examples** - Real applications with outcomes
- 🎤 **18 Interview Q&As** - Prepared answers in Charles's voice
- 📊 **Application tracker** - History with learnings
- ✨ **Cover letter generator** - Quick drafts by industry
- 📚 **Published books** - Children's literature showcase
- ✍️ **Writing samples** - Film reviews and cultural commentary

## Quick Start (Local)

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows/GitBash
# or: source venv/bin/activate  # Mac/Linux

# Install & run
pip install -r requirements.txt
python app.py

# Open http://127.0.0.1:8080
```

## Deploy to Render (Free - Access from Phone!)

### 1. Push to GitHub
```bash
cd Kyle
git init
git add .
git commit -m "Kyle"
gh repo create kyle-assistant --public --push
```

### 2. Deploy on Render
- Go to [render.com](https://render.com) → New → Web Service
- Connect your GitHub repo
- Settings will auto-detect from `render.yaml`
- Add environment variable: `PASSWORD` = your secret password
- Click Deploy

### 3. Access from Phone
- Your app will be at: `https://kyle-assistant.onrender.com`
- **iPhone**: Safari → Share → Add to Home Screen
- **Android**: Chrome → Menu → Add to Home Screen
- Works offline after first load

## Files

| File | Description |
|------|-------------|
| `app.py` | Main Flask dashboard |
| `charles_profile.json` | Complete profile data |
| `interview_qa.json` | 18 interview Q&As |
| `cover_letters.json` | 5 cover letter examples |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |

## Data Included

### Profile
- Contact info, links (LinkedIn, Portfolio, GitHub, etc.)
- 10+ years experience across 7 roles
- Skills (core, technical, PM, localisation)
- Education (neuefische AI bootcamp, BA Language Practice)
- Gaming background

### Cover Letters (5 examples)
1. **Freaks 4U Gaming** - Senior PM (pending)
2. **Nintendo of Europe** - Localisation Producer (rejected)
3. **Netflix** - Product Language Manager DACH (applied)
4. **Loewe Verlag** - Rights Manager (rejected - closest call)
5. **Springer Nature** - Product Manager (rejected)

### Interview Q&A (18 questions)
Tell me about yourself, strengths/weaknesses, challenging projects, tight deadlines, cross-functional teams, feedback, localisation experience, Germany move, AI training, organisation, company research, 5-year goals, salary, published books, conflict handling, questions for interviewer

### Books (4 published)
- The Legend of Mamlambo
- The Blacksmith and the Dragonfly (Kwasuka Sukela)
- The Princess and the Sangoma (Kwasuka Sukela)
- Verlore in Duitsland (short story)

### Writing Samples
- Film reviews: Sinners, Dune 2, Oppenheimer, Barbie
- Cultural: #YouthMatters, Jozi commentary

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/profile` - Profile JSON
- `GET /api/interview` - Interview Q&A JSON
- `GET /api/letters` - Cover letters JSON

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PASSWORD` | No | HTTP Basic Auth password |
| `PORT` | No | Server port (default: 8080) |
| `RENDER` | Auto | Set by Render to disable debug |

---

Built with ❤️ for Charles's job search journey
