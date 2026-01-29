"""
Kyle - AI-Powered Job Application Assistant for Charles Siboto
Mobile-friendly PWA with password protection
"""

from flask import Flask, jsonify, Response, request
from functools import wraps
import json
import os

app = Flask(__name__)

# Load data
def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

PROFILE = load_json('charles_profile.json')
INTERVIEW_QA = load_json('interview_qa.json')
COVER_LETTERS = load_json('cover_letters.json')

# Password protection (optional)
PASSWORD = os.environ.get('PASSWORD')

def check_auth(username, password):
    return password == PASSWORD

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not PASSWORD:
            return f(*args, **kwargs)
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Access denied. Please provide valid credentials.',
                401,
                {'WWW-Authenticate': 'Basic realm="Kyle"'}
            )
        return f(*args, **kwargs)
    return decorated

# Use %% to escape % in CSS, and %(name)s for variables
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Kyle</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Kyle">
    <meta name="theme-color" content="#1a1a2e">
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎮</text></svg>">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%%, #16213e 100%%);
            color: #eee;
            min-height: 100vh;
            padding: 15px;
            padding-top: env(safe-area-inset-top, 15px);
            -webkit-tap-highlight-color: transparent;
        }
        header { text-align: center; padding: 20px 0; border-bottom: 1px solid #333; margin-bottom: 20px; }
        h1 { font-size: 1.8em; color: #00d4ff; }
        h2 { font-size: 1.2em; color: #00d4ff; margin: 15px 0 10px; }
        h3 { font-size: 1em; color: #ffd700; margin: 10px 0 5px; }
        .subtitle { color: #888; font-size: 0.9em; margin-top: 5px; }
        .tabs { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; justify-content: center; }
        .tab { background: #16213e; border: 1px solid #333; color: #ccc; padding: 10px 15px; border-radius: 20px; cursor: pointer; font-size: 0.85em; transition: all 0.2s; }
        .tab:hover, .tab.active { background: #00d4ff; color: #000; border-color: #00d4ff; }
        .content { display: none; }
        .content.active { display: block; }
        .card { background: rgba(255,255,255,0.05); border-radius: 12px; padding: 15px; margin-bottom: 15px; border: 1px solid #333; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        @media (min-width: 768px) { .grid { grid-template-columns: repeat(4, 1fr); } }
        .stat { background: rgba(0,212,255,0.1); padding: 12px; border-radius: 8px; text-align: center; }
        .stat-value { font-size: 1.5em; font-weight: bold; color: #00d4ff; }
        .stat-label { font-size: 0.75em; color: #888; }
        .tag { display: inline-block; background: #00d4ff; color: #000; padding: 3px 8px; border-radius: 12px; font-size: 0.7em; margin: 2px; }
        .tag.pending, .tag.applied { background: #ffd700; }
        .tag.rejected { background: #ff4757; color: #fff; }
        a { color: #00d4ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { padding-left: 20px; }
        li { margin: 5px 0; font-size: 0.9em; line-height: 1.4; }
        .qa-item { margin-bottom: 15px; }
        .qa-q { color: #ffd700; font-weight: bold; margin-bottom: 5px; }
        .qa-a { color: #ccc; font-size: 0.9em; line-height: 1.5; }
        .letter-card { margin-bottom: 20px; }
        .letter-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 5px; }
        .letter-content { background: #111; padding: 15px; border-radius: 8px; margin-top: 10px; white-space: pre-wrap; font-size: 0.85em; line-height: 1.5; max-height: 300px; overflow-y: auto; }
        .btn { background: #00d4ff; color: #000; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-size: 0.85em; }
        .btn:active { transform: scale(0.95); }
        .exp-item { border-left: 3px solid #00d4ff; padding-left: 15px; margin-bottom: 15px; }
        .exp-title { font-weight: bold; color: #fff; }
        .exp-company { color: #ffd700; font-size: 0.9em; }
        .exp-dates { color: #666; font-size: 0.8em; }
        .book-card { display: flex; gap: 15px; margin-bottom: 15px; }
        .book-icon { font-size: 2.5em; }
        .book-info { flex: 1; }
        .book-title { font-weight: bold; color: #fff; }
        .book-author { color: #888; font-size: 0.85em; }
        .book-desc { color: #aaa; font-size: 0.85em; margin-top: 5px; }
        .generator { margin-top: 15px; }
        .generator input, .generator select { width: 100%%; padding: 12px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #333; background: #111; color: #fff; font-size: 16px; }
        #generated-letter { background: #111; padding: 15px; border-radius: 8px; white-space: pre-wrap; font-size: 0.85em; line-height: 1.5; margin-top: 15px; }
        .links a { display: inline-block; margin: 5px 10px 5px 0; padding: 5px 10px; background: rgba(0,212,255,0.2); border-radius: 15px; font-size: 0.85em; }
        .app-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #333; }
        .app-company { font-weight: bold; }
        .app-role { color: #888; font-size: 0.85em; }
        .writing-sample { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #333; }
        .writing-title { color: #ffd700; font-size: 0.9em; }
        .writing-desc { color: #888; font-size: 0.8em; }
    </style>
</head>
<body>
    <header>
        <h1>🎮 Kyle</h1>
        <p class="subtitle">Charles Siboto's Job Application Assistant</p>
    </header>
    
    <div class="tabs">
        <div class="tab active" data-tab="profile">Profile</div>
        <div class="tab" data-tab="experience">Experience</div>
        <div class="tab" data-tab="interview">Interview Q&A</div>
        <div class="tab" data-tab="applications">Applications</div>
        <div class="tab" data-tab="letters">Cover Letters</div>
        <div class="tab" data-tab="generator">Letter Gen</div>
        <div class="tab" data-tab="cvgen">CV Gen</div>
        <div class="tab" data-tab="books">Books</div>
        <div class="tab" data-tab="writing">Writing</div>
    </div>
    
    <div id="profile" class="content active">
        <div class="grid">
            <div class="stat"><div class="stat-value">10+</div><div class="stat-label">Years Experience</div></div>
            <div class="stat"><div class="stat-value">20+</div><div class="stat-label">Books/Year</div></div>
            <div class="stat"><div class="stat-value">4</div><div class="stat-label">Published Books</div></div>
            <div class="stat"><div class="stat-value">12+</div><div class="stat-label">Years Writing</div></div>
        </div>
        
        <div class="card">
            <h2>📋 Contact</h2>
            <p><strong>Name:</strong> %(name)s</p>
            <p><strong>Email:</strong> <a href="mailto:%(email)s">%(email)s</a></p>
            <p><strong>Phone:</strong> %(phone)s</p>
            <p><strong>Location:</strong> %(location)s</p>
            <p><strong>Available:</strong> %(available)s</p>
            <p><strong>Salary:</strong> %(salary)s</p>
            <p><strong>Languages:</strong> English (Native), German (Advanced)</p>
        </div>
        
        <div class="card">
            <h2>🔗 Links</h2>
            <div class="links">
                <a href="%(linkedin)s" target="_blank">LinkedIn</a>
                <a href="%(portfolio)s" target="_blank">Portfolio</a>
                <a href="%(github)s" target="_blank">GitHub</a>
                <a href="%(penguin)s" target="_blank">Penguin Author</a>
                <a href="%(goodreads)s" target="_blank">Goodreads</a>
                <a href="%(bizcommunity)s" target="_blank">Bizcommunity</a>
            </div>
        </div>
        
        <div class="card">
            <h2>💼 Professional Identity</h2>
            <p><strong>%(headline)s</strong></p>
            <p style="margin-top:10px; color:#aaa; font-size:0.9em;">%(about)s</p>
        </div>
        
        <div class="card">
            <h2>🎯 Skills</h2>
            <div>%(skills)s</div>
        </div>
        
        <div class="card">
            <h2>🎓 Education</h2>
            %(education)s
        </div>
        
        <div class="card">
            <h2>🎮 Gaming Background</h2>
            <p><strong>First Game:</strong> The Legend of Zelda: Link's Awakening (Game Boy)</p>
            <p><strong>Favourites:</strong> Zelda, Metroid, Fire Emblem</p>
            <p style="margin-top:10px; color:#aaa; font-size:0.9em;">"Gaming is more than entertainment. It is a storytelling engine, a global community and a space for cultural innovation."</p>
        </div>
    </div>
    
    <div id="experience" class="content">
        <h2>💼 Work History</h2>
        %(experience)s
    </div>
    
    <div id="interview" class="content">
        <h2>🎤 Interview Q&A (%(qa_count)s questions)</h2>
        %(interview_qa)s
    </div>
    
    <div id="applications" class="content">
        <div class="grid">
            <div class="stat"><div class="stat-value">%(app_total)s</div><div class="stat-label">Total</div></div>
            <div class="stat"><div class="stat-value">%(app_pending)s</div><div class="stat-label">Pending</div></div>
            <div class="stat"><div class="stat-value">%(app_rejected)s</div><div class="stat-label">Rejected</div></div>
            <div class="stat"><div class="stat-value">%(success_rate)s%%</div><div class="stat-label">Pending</div></div>
        </div>
        
        <div class="card">
            <h2>📊 Application History</h2>
            %(applications)s
        </div>
        
        <div class="card">
            <h2>📚 Learnings</h2>
            <ul>%(learnings)s</ul>
        </div>
        
        <div class="card">
            <h2>🎯 Target Companies</h2>
            <h3>High Priority</h3>
            <p><strong>German Children's Publishing:</strong> Carlsen, Oetinger, Loewe, Arena, Ravensburger</p>
            <p><strong>German Gaming:</strong> InnoGames, Goodgame, Deck13, Yager, Mimimi, Freaks 4U</p>
            <h3>Medium Priority</h3>
            <p>CD Projekt Red, Remedy, Larian Studios, Hachette Germany</p>
            <h3>Avoid (Too Competitive)</h3>
            <p>Nintendo, Springer Nature, Zalando, Major AAA Studios</p>
        </div>
    </div>
    
    <div id="letters" class="content">
        <h2>📝 Cover Letter Examples (%(letter_count)s)</h2>
        %(cover_letters)s
    </div>
    
    <div id="generator" class="content">
        <h2>✨ Cover Letter Generator</h2>
        <div class="card generator">
            <input type="text" id="gen-company" placeholder="Company name">
            <input type="text" id="gen-role" placeholder="Role title">
            <select id="gen-industry">
                <option value="gaming">Gaming / Esports</option>
                <option value="publishing">Publishing</option>
                <option value="streaming">Streaming / Tech</option>
                <option value="education">Education</option>
            </select>
            <select id="gen-cv">
                <option value="localisation">Localisation & PM CV</option>
                <option value="language">Product Language Manager CV</option>
                <option value="product">Product Manager CV</option>
            </select>
            <button class="btn" onclick="generateLetter()">Generate Letter</button>
            <button class="btn" onclick="copyLetter()" style="background:#ffd700; margin-left:10px;">Copy</button>
            <div id="generated-letter"></div>
        </div>
    </div>
    
    <div id="books" class="content">
        <h2>📚 Published Books</h2>
        %(books)s
    </div>
    
    <div id="cvgen" class="content">
        <h2>📄 CV Generator</h2>
        <div class="card generator">
            <input type="text" id="cv-role" placeholder="Target role (e.g. Localisation Producer)">
            <input type="text" id="cv-company" placeholder="Company name (optional)">
            <select id="cv-type">
                <option value="localisation">Localisation & Project Management</option>
                <option value="language">Product Language Manager</option>
                <option value="product">Product Manager</option>
            </select>
            <button class="btn" onclick="generateCV()">Generate CV</button>
            <button class="btn" onclick="copyCV()" style="background:#ffd700; margin-left:10px;">Copy</button>
            <div id="generated-cv" style="background: #111; padding: 15px; border-radius: 8px; white-space: pre-wrap; font-size: 0.8em; line-height: 1.4; margin-top: 15px; max-height: 500px; overflow-y: auto;"></div>
        </div>
    </div>
    
    <div id="writing" class="content">
        <h2>✍️ Writing Samples</h2>
        <div class="card">
            <h3>🎬 Film Reviews</h3>
            %(film_reviews)s
        </div>
        <div class="card">
            <h3>🌍 Cultural Commentary</h3>
            %(cultural)s
        </div>
    </div>

    <script>
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(tab.dataset.tab).classList.add('active');
            });
        });
        
        function generateLetter() {
            const company = document.getElementById('gen-company').value || '[COMPANY]';
            const role = document.getElementById('gen-role').value || '[ROLE]';
            const industry = document.getElementById('gen-industry').value;
            
            const hooks = {
                gaming: "As a lifelong Nintendo fan whose journey began with the Game Boy and The Legend of Zelda: Link's Awakening, I am genuinely excited by the opportunity to contribute to the gaming industry.",
                publishing: 'With over ten years of experience in publishing and digital content management, I bring both editorial expertise and project management discipline to this role.',
                streaming: 'With a degree in Language Practice, over ten years of editorial experience, and advanced German fluency, I am excited to help deliver authentic language experiences.',
                education: 'As an experienced educator who has improved language proficiency by 30%% through tailored courses, I am passionate about creating engaging learning experiences.'
            };
            
            const date = new Date().toLocaleDateString('en-GB', {day: 'numeric', month: 'long', year: 'numeric'});
            
            const letter = `Charles Siboto
Neu-Eichenberg, Germany
csiboto@gmail.com
+49 176 8787 3255
linkedin.com/in/charlessiboto

${date}

Dear Hiring Team,

I am writing to apply for the ${role} position at ${company}. ${hooks[industry]}

My career has been built on delivering complex projects on time, within budget and to the highest quality standards. At Jonathan Ball Publishers, I managed 20+ book titles annually through the complete production lifecycle, coordinating cross-functional teams and ensuring all deliverables met quality benchmarks. At NB Publishers, I oversaw translation and co-production projects with international publishing partners.

I bring excellent communication skills and experience guiding teams. At ASC Göttingen, I developed and delivered English training courses for 40 colleagues, improving language proficiency by 30%%. My recent AI Project Management training at neuefische GmbH has reinforced my ability to rapidly acquire new technical competencies.

Having lived in Germany since 2018, I am fluent in the working culture and comfortable operating in both English and German. I bring a proactive, positive attitude and a strong work ethic.

I am available to start from 1 March 2026, and my salary expectation is in the range of €50,000 to €58,000 annually. Thank you for considering my application.

Warm regards,

Charles Siboto`;
            
            document.getElementById('generated-letter').textContent = letter;
        }
        
        function copyLetter() {
            const letter = document.getElementById('generated-letter').textContent;
            if (letter) {
                navigator.clipboard.writeText(letter).then(() => alert('Copied to clipboard!'));
            }
        }
        
        function copyExisting(id) {
            const el = document.getElementById('letter-' + id);
            if (el) {
                navigator.clipboard.writeText(el.textContent).then(() => alert('Copied!'));
            }
        }
        
        function generateCV() {
            const role = document.getElementById('cv-role').value || 'Project Manager';
            const company = document.getElementById('cv-company').value;
            const cvType = document.getElementById('cv-type').value;
            
            const summaries = {
                localisation: `Project management and localisation professional with over ten years of experience delivering complex publishing projects on time, within budget and to the highest quality standards. Proven expertise in coordinating cross-functional teams, managing international co-productions, and ensuring editorial excellence across multiple languages. Adept at stakeholder negotiation, risk management and quality assurance. Recently certified in Agile Scrum methodology with practical AI/ML knowledge.`,
                language: `Linguistic and editorial professional with over ten years of experience in publishing, translation oversight and quality frameworks, combining deep expertise in language craft with practical knowledge of AI and machine learning technologies. Skilled in developing style guides, maintaining editorial standards, and ensuring cultural resonance across DACH markets. Bilingual in English (native) and German (advanced), with seven years living and working in Germany.`,
                product: `Product management professional with over ten years of experience in publishing and digital content strategy. Expert in identifying market trends, executing innovative content strategies, and delivering user-focused digital products. Proven track record of increasing engagement by 25%% through data-driven decisions. Recently trained in AI/ML technologies and Agile methodologies.`
            };
            
            const skillSets = {
                localisation: `PROJECT MANAGEMENT: Planning & Scheduling, Budget Control, Quality Assurance, Risk Management, Agile Scrum, Stakeholder Negotiation
LOCALISATION: Translation Oversight, International Co-production, Cultural Adaptation, Multi-language Coordination, Editorial QC
TECHNICAL: Python, Git, Data Visualization, MS Office, WordPress, CMS Platforms
LANGUAGES: English (Native), German (Advanced - daily professional use since 2018)`,
                language: `LINGUISTIC: Style Guide Development, Editorial Standards, Translation QA, Cultural Adaptation, Tone & Voice Consistency
TECHNICAL: Python, ML Pipeline Development, Data Manipulation, PySpark, Git, Bash
PROJECT: Agile Scrum, Cross-functional Collaboration, Stakeholder Management, Quality Frameworks
LANGUAGES: English (Native), German (Advanced - daily professional use since 2018)`,
                product: `PRODUCT: Roadmap Development, User Research, A/B Testing, Data Analysis, Market Research, Feature Prioritisation
TECHNICAL: Python, Data Visualization, Agile Scrum, Git, CMS Platforms, Analytics Tools
LEADERSHIP: Cross-functional Team Coordination, Stakeholder Management, Strategic Planning
LANGUAGES: English (Native), German (Advanced - daily professional use since 2018)`
            };
            
            const headlines = {
                localisation: 'LOCALISATION & PROJECT MANAGEMENT PROFESSIONAL',
                language: 'PRODUCT LANGUAGE MANAGER',
                product: 'PRODUCT MANAGER'
            };
            
            const targetLine = company ? `Target: ${role} at ${company}` : `Target: ${role}`;
            
            const cv = `CHARLES SIBOTO
${headlines[cvType]}

Neu-Eichenberg, Germany | csiboto@gmail.com | +49 176 8787 3255
LinkedIn: linkedin.com/in/charlessiboto | Portfolio: charless-digital-canvas.lovable.app

${targetLine}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL SUMMARY

${summaries[cvType]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SKILLS

${skillSets[cvType]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL EXPERIENCE

ENGLISH EDUCATOR | ASC Göttingen von 1846 e.V.
Göttingen, Germany | Nov 2025 - Present
• Conducting English courses and workshops for colleagues
• Managing lesson planning and resource coordination
• Facilitating activities in aftercare program

CONTRIBUTING WRITER | Bizcommunity.com
Cape Town, South Africa | May 2012 - Mar 2025
• Authored entertainment coverage and game reviews for 12+ years
• Grew readership by 35%% through culturally relevant content
• Led #YouthMonth and #BizTrends campaigns

ONLINE EDITOR | Software & Support Media
Frankfurt, Germany | Jan 2024 - Jun 2024
• Managed content production across web platforms
• Coordinated workshops and online events
• Developed content strategies aligned with marketing campaigns

EDITOR & PROJECT MANAGER | Jonathan Ball Publishers
Cape Town, South Africa | Oct 2021 - Oct 2022
• Managed 20+ book titles annually through complete lifecycle
• Coordinated cross-functional teams (editors, designers, production)
• Spearheaded e-book commissioning and digital asset management

JUNIOR EDITOR | NB Publishers
Cape Town, South Africa | Jun 2013 - Jun 2017
• Managed digital publishing, releasing 20+ EPUB/MOBI titles annually
• Oversaw translation and co-production projects with international publishers
• Delivered projects under tight deadlines while maintaining quality

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EDUCATION & CERTIFICATIONS

AI PROJECT MANAGEMENT | neuefische GmbH / SPICED Academy, Berlin
Jun 2025 - Nov 2025
Focus: AI/ML, Python, Agile Scrum, Data Visualization

BA LANGUAGE PRACTICE | University of Johannesburg
2006 - 2010
Focus: English Literature, Linguistics, Latin

ADVANCED COPY EDITING & PROOFREADING | McGillivray Linnegar Associates
2015

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUBLICATIONS

• The Legend of Mamlambo (Penguin Random House SA, 2024)
• The Blacksmith and the Dragonfly - Kwasuka Sukela series (PRH SA, 2025)
• The Princess and the Sangoma - Kwasuka Sukela series (PRH SA, 2025)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GAMING BACKGROUND

Lifelong Nintendo enthusiast since the Game Boy era. First game: The Legend of Zelda: Link's Awakening. Favourite franchises: Zelda, Metroid, Fire Emblem. Passionate about gaming as a storytelling medium and cultural force.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Available from: 1 March 2026 | Salary expectation: €50,000 - €58,000`;
            
            document.getElementById('generated-cv').textContent = cv;
        }
        
        function copyCV() {
            const cv = document.getElementById('generated-cv').textContent;
            if (cv) {
                navigator.clipboard.writeText(cv).then(() => alert('CV copied to clipboard!'));
            }
        }
        
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js');
        }
    </script>
</body>
</html>'''

@app.route('/')
@requires_auth
def index():
    profile = PROFILE.get('profile', {})
    identity = PROFILE.get('professional_identity', {})
    links = profile.get('links', {})
    
    # Skills
    skills_data = PROFILE.get('skills', {})
    skills_html = ''
    for cat, items in skills_data.items():
        if isinstance(items, list):
            skills_html += ''.join(f'<span class="tag">{s}</span>' for s in items[:8])
    
    # Education
    edu_html = ''
    for edu in PROFILE.get('education', []):
        edu_html += f'''<div style="margin-bottom:10px;">
            <strong>{edu.get('degree', '')}</strong><br>
            <span style="color:#888;">{edu.get('institution', '')} | {edu.get('dates', '')}</span>
        </div>'''
    
    # Experience
    exp_html = ''
    for exp in PROFILE.get('experience', []):
        highlights = ''.join(f'<li>{h}</li>' for h in exp.get('highlights', []))
        exp_html += f'''<div class="exp-item">
            <div class="exp-title">{exp.get('title', '')}</div>
            <div class="exp-company">{exp.get('company', '')}</div>
            <div class="exp-dates">{exp.get('dates', '')} | {exp.get('location', '')}</div>
            <ul style="margin-top:8px;">{highlights}</ul>
        </div>'''
    
    # Interview Q&A
    qa_html = ''
    for qa in INTERVIEW_QA:
        qa_html += f'''<div class="qa-item card">
            <div class="qa-q">Q{qa.get('id', '')}: {qa.get('question', '')}</div>
            <div class="qa-a">{qa.get('answer', '')}</div>
        </div>'''
    
    # Applications
    app_history = PROFILE.get('application_history', {})
    apps = app_history.get('applications', [])
    app_html = ''
    for a in apps:
        status_class = a.get('status', 'pending')
        app_html += f'''<div class="app-row">
            <div>
                <div class="app-company">{a.get('company', '')}</div>
                <div class="app-role">{a.get('role', '')}</div>
            </div>
            <span class="tag {status_class}">{a.get('status', '').upper()}</span>
        </div>'''
    
    learnings_html = ''.join(f'<li>{l}</li>' for l in app_history.get('learnings', []))
    
    # Cover letters
    letters_html = ''
    for letter in COVER_LETTERS:
        status = letter.get('status', 'pending')
        letters_html += f'''<div class="card letter-card">
            <div class="letter-header">
                <div>
                    <strong>{letter.get('company', '')}</strong><br>
                    <span style="color:#888;font-size:0.85em;">{letter.get('role', '')}</span>
                </div>
                <div>
                    <span class="tag {status}">{status.upper()}</span>
                    <button class="btn" onclick="copyExisting('{letter.get('id', '')}')">Copy</button>
                </div>
            </div>
            <div class="letter-content" id="letter-{letter.get('id', '')}">{letter.get('letter', '')}</div>
        </div>'''
    
    # Books
    books_html = ''
    for book in PROFILE.get('books', []):
        authors = book.get('authors', [book.get('author', '')])
        if isinstance(authors, list):
            authors = ', '.join(authors)
        books_html += f'''<div class="card book-card">
            <div class="book-icon">📖</div>
            <div class="book-info">
                <div class="book-title">{book.get('title', '')}</div>
                <div class="book-author">{authors} | {book.get('publisher', '')} ({book.get('year', '')})</div>
                <div class="book-desc">{book.get('description', '')}</div>
            </div>
        </div>'''
    
    # Writing samples
    reviews_html = ''
    for r in PROFILE.get('writing_samples', {}).get('film_reviews', []):
        reviews_html += f'''<div class="writing-sample">
            <div class="writing-title">{r.get('title', '')}</div>
            <div class="writing-desc">{r.get('description', '')}</div>
        </div>'''
    
    cultural_html = ''
    for c in PROFILE.get('writing_samples', {}).get('cultural_commentary', []):
        cultural_html += f'''<div class="writing-sample">
            <div class="writing-title">{c.get('title', '')}</div>
            <div class="writing-desc">{c.get('description', '')}</div>
        </div>'''
    
    # Stats
    pending = len([a for a in apps if a.get('status') in ['pending', 'applied']])
    rejected = len([a for a in apps if a.get('status') == 'rejected'])
    
    data = {
        'name': profile.get('name', 'Charles Siboto'),
        'email': profile.get('email', ''),
        'phone': profile.get('phone', ''),
        'location': profile.get('location', ''),
        'available': profile.get('available_from', ''),
        'salary': profile.get('salary_expectation', ''),
        'linkedin': links.get('linkedin', ''),
        'portfolio': links.get('portfolio', ''),
        'github': links.get('github', ''),
        'penguin': links.get('penguin_author', ''),
        'goodreads': links.get('goodreads', ''),
        'bizcommunity': links.get('bizcommunity', ''),
        'headline': identity.get('headline', ''),
        'about': identity.get('about_me', ''),
        'skills': skills_html,
        'education': edu_html,
        'experience': exp_html,
        'interview_qa': qa_html,
        'qa_count': len(INTERVIEW_QA),
        'app_total': len(apps),
        'app_pending': pending,
        'app_rejected': rejected,
        'success_rate': f'{(pending/len(apps)*100):.0f}' if apps else '0',
        'applications': app_html,
        'learnings': learnings_html,
        'cover_letters': letters_html,
        'letter_count': len(COVER_LETTERS),
        'books': books_html,
        'film_reviews': reviews_html,
        'cultural': cultural_html
    }
    
    return HTML_TEMPLATE % data

@app.route('/api/profile')
@requires_auth
def api_profile():
    return jsonify(PROFILE)

@app.route('/api/interview')
@requires_auth
def api_interview():
    return jsonify(INTERVIEW_QA)

@app.route('/api/letters')
@requires_auth
def api_letters():
    return jsonify(COVER_LETTERS)

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Kyle",
        "short_name": "Kyle",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a1a2e",
        "theme_color": "#1a1a2e",
        "icons": [{"src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎮</text></svg>", "sizes": "any", "type": "image/svg+xml"}]
    })

@app.route('/sw.js')
def service_worker():
    return Response("self.addEventListener('fetch', function(event) {});", mimetype='application/javascript')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('RENDER') is None
    
    print("\n" + "="*50)
    print("KYLE - JOB APPLICATION ASSISTANT")
    print("="*50)
    print(f"\n✓ Profile: {bool(PROFILE)}")
    print(f"✓ Interview Q&A: {len(INTERVIEW_QA)} items")
    print(f"✓ Cover Letters: {len(COVER_LETTERS)} examples")
    if PASSWORD:
        print("✓ Password protection: ENABLED")
    print(f"\n👉 Open: http://127.0.0.1:{port}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
