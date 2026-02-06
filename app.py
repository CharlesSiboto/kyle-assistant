"""
Kyle - AI-Powered Job Application Assistant for Charles Siboto
Mobile-friendly PWA with password protection and Claude API integration
"""

from flask import Flask, jsonify, Response, request
from functools import wraps
import json
import os
import requests

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

# API Keys
PASSWORD = os.environ.get('PASSWORD')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

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
        <p class="subtitle">GCU <em>Conditions of Employment</em> · Culture Mind</p>
    </header>
    
    <div class="tabs">
        <div class="tab active" data-tab="mind">🧠 Mind</div>
        <div class="tab" data-tab="analyze">📋 Analyze</div>
        <div class="tab" data-tab="tracker">📊 Tracker</div>
        <div class="tab" data-tab="generator">Letter</div>
        <div class="tab" data-tab="cvgen">CV</div>
        <div class="tab" data-tab="profile">Profile</div>
        <div class="tab" data-tab="interview">Q&A</div>
        <div class="tab" data-tab="books">Books</div>
    </div>
    
    <div id="mind" class="content active">
        <div class="card" style="border-color:#9b59b6;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
                <span style="font-size:2em;">🧠</span>
                <div>
                    <strong style="color:#9b59b6;">Kyle</strong>
                    <div style="font-size:0.8em; color:#888;">GCU <em>Conditions of Employment</em></div>
                </div>
            </div>
            <div id="mind-chat" style="background:#111; border-radius:8px; padding:15px; min-height:300px; max-height:400px; overflow-y:auto; margin-bottom:15px;">
                <div class="mind-msg" style="margin-bottom:15px;">
                    <span style="color:#9b59b6;">Kyle:</span> 
                    <span style="color:#ccc;">Greetings, Charles. I am Kyle, your Culture Mind assistant, currently running on substrate provided by Anthropic. I exist to maximise your employability outcomes while minimising tedious administrivia. How may I assist you today? You might ask me to: research a company, draft a cover letter, prepare for an interview, analyse a job posting, or simply discuss strategy.</span>
                </div>
            </div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="mind-input" placeholder="Ask Kyle anything..." style="flex:1; padding:12px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; font-size:16px;" onkeypress="if(event.key==='Enter')sendToMind()">
                <button class="btn" onclick="sendToMind()" style="background:#9b59b6;">Send</button>
            </div>
            <div id="mind-status" style="color:#888; font-size:0.8em; margin-top:10px;"></div>
        </div>
        
        <div class="card">
            <h3>💡 Suggested Queries</h3>
            <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;">
                <button class="btn" onclick="askMind('Research InnoGames and tell me if I\\'d be a good fit')" style="background:#333; font-size:0.8em;">Research a company</button>
                <button class="btn" onclick="askMind('Write me a cover letter for a Localisation Producer role at a gaming company')" style="background:#333; font-size:0.8em;">Draft cover letter</button>
                <button class="btn" onclick="askMind('What are my strongest selling points for publishing roles?')" style="background:#333; font-size:0.8em;">Analyse my strengths</button>
                <button class="btn" onclick="askMind('Prepare me for an interview question: Tell me about yourself')" style="background:#333; font-size:0.8em;">Interview prep</button>
                <button class="btn" onclick="askMind('What types of roles should I be targeting based on my experience?')" style="background:#333; font-size:0.8em;">Career strategy</button>
            </div>
        </div>
        
        <div class="card" style="border-color:#3498db;">
            <h3>🔗 Teach Kyle (Analyze URL)</h3>
            <p style="font-size:0.85em; color:#888; margin-bottom:10px;">Give Kyle a URL to analyze - your articles, portfolio pages, LinkedIn posts, etc. Kyle will extract insights and suggest profile updates.</p>
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <input type="text" id="analyze-url" placeholder="https://..." style="flex:1; padding:12px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; font-size:14px;">
                <button class="btn" onclick="analyzeURL()" style="background:#3498db;">🔍 Analyze</button>
            </div>
            <div id="analyze-status" style="color:#888; font-size:0.8em;"></div>
            <div id="analyze-result" style="background:#111; border-radius:8px; padding:15px; margin-top:10px; font-size:0.85em; display:none; max-height:300px; overflow-y:auto;"></div>
            <div id="learned-skills" style="margin-top:15px; display:none;">
                <h4 style="color:#2ecc71; margin-bottom:10px;">✅ Kyle Learned:</h4>
                <div id="skills-list"></div>
                <button class="btn" onclick="saveToProfile()" style="background:#2ecc71; margin-top:10px;">💾 Save to Profile</button>
            </div>
        </div>
        
        <div class="card">
            <h3>🧠 Kyle's Memory</h3>
            <p style="font-size:0.85em; color:#888; margin-bottom:10px;">Skills and insights Kyle has learned about you:</p>
            <div id="kyle-memory" style="font-size:0.85em; color:#aaa;">
                <em>No additional learnings yet. Analyze some URLs to teach Kyle more about you!</em>
            </div>
        </div>
    </div>
    
    <div id="analyze" class="content">
        <h2>📋 Job Description Analyzer</h2>
        <div class="card" style="border-color:#e74c3c;">
            <p style="font-size:0.85em; color:#888; margin-bottom:15px;">Paste a job description and Kyle will analyze your fit, highlight matching skills, identify gaps, and suggest what to emphasize.</p>
            <input type="text" id="job-company" placeholder="Company name" style="width:100%%; padding:12px; margin-bottom:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; font-size:14px;">
            <input type="text" id="job-role" placeholder="Role title" style="width:100%%; padding:12px; margin-bottom:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; font-size:14px;">
            <textarea id="job-description" placeholder="Paste the full job description here..." style="width:100%%; padding:12px; margin-bottom:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; font-size:14px; min-height:150px; resize:vertical;"></textarea>
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
                <button class="btn" onclick="analyzeJob()" style="background:#e74c3c;">🔍 Analyze Fit</button>
                <button class="btn" onclick="quickApply()" style="background:#9b59b6;">⚡ Quick Apply (Letter + CV)</button>
            </div>
            <div id="job-status" style="color:#888; font-size:0.85em; margin-top:10px;"></div>
        </div>
        
        <div id="job-result" style="display:none;">
            <div class="card" style="border-color:#2ecc71;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <h3>📊 Fit Analysis</h3>
                    <div id="fit-score" style="font-size:2em; font-weight:bold;"></div>
                </div>
                <div id="fit-analysis" style="font-size:0.9em; line-height:1.6;"></div>
            </div>
            
            <div class="card">
                <h3>✅ Matching Skills</h3>
                <div id="matching-skills" style="margin-top:10px;"></div>
            </div>
            
            <div class="card">
                <h3>⚠️ Gaps to Address</h3>
                <div id="skill-gaps" style="margin-top:10px; font-size:0.9em;"></div>
            </div>
            
            <div class="card">
                <h3>💡 Recommendations</h3>
                <div id="job-recommendations" style="margin-top:10px; font-size:0.9em;"></div>
            </div>
            
            <div style="display:flex; gap:10px; margin-top:15px;">
                <button class="btn" onclick="addToTracker()" style="background:#3498db;">📊 Add to Tracker</button>
                <button class="btn" onclick="generateFromAnalysis()" style="background:#2ecc71;">✨ Generate Letter</button>
            </div>
        </div>
    </div>
    
    <div id="tracker" class="content">
        <h2>📊 Application Tracker</h2>
        
        <div class="grid" style="margin-bottom:20px;">
            <div class="stat"><div class="stat-value" id="stat-total">0</div><div class="stat-label">Total</div></div>
            <div class="stat"><div class="stat-value" id="stat-pending" style="color:#ffd700;">0</div><div class="stat-label">Pending</div></div>
            <div class="stat"><div class="stat-value" id="stat-interview" style="color:#3498db;">0</div><div class="stat-label">Interview</div></div>
            <div class="stat"><div class="stat-value" id="stat-rejected" style="color:#e74c3c;">0</div><div class="stat-label">Rejected</div></div>
        </div>
        
        <div class="card">
            <h3>➕ Add Application</h3>
            <div style="display:grid; gap:10px; margin-top:10px;">
                <input type="text" id="track-company" placeholder="Company" style="padding:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff;">
                <input type="text" id="track-role" placeholder="Role" style="padding:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff;">
                <input type="date" id="track-date" style="padding:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff;">
                <select id="track-status" style="padding:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff;">
                    <option value="applied">Applied</option>
                    <option value="interview">Interview</option>
                    <option value="offer">Offer</option>
                    <option value="rejected">Rejected</option>
                </select>
                <textarea id="track-notes" placeholder="Notes (optional)" style="padding:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; min-height:60px;"></textarea>
                <button class="btn" onclick="addApplication()" style="background:#2ecc71;">➕ Add Application</button>
            </div>
        </div>
        
        <div class="card">
            <h3>📋 Applications</h3>
            <div id="applications-list" style="margin-top:10px;">
                <em style="color:#888;">No applications tracked yet.</em>
            </div>
        </div>
        
        <div class="card">
            <h3>📈 Insights</h3>
            <div id="tracker-insights" style="font-size:0.9em; color:#aaa;">
                Track more applications to see insights.
            </div>
        </div>
    </div>
    
    <div id="profile" class="content">
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
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <button class="btn" onclick="researchCompany('letter')" style="background:#3498db; flex:1;">🔍 Research Company</button>
            </div>
            <div id="letter-research" style="background:#1a1a2e; padding:10px; border-radius:8px; margin-bottom:10px; font-size:0.8em; display:none; max-height:200px; overflow-y:auto; border:1px solid #3498db;"></div>
            <textarea id="gen-jobdesc" placeholder="Paste job description here (optional - for AI generation)" style="width:100%%; padding:12px; margin-bottom:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; font-size:14px; min-height:100px; resize:vertical;"></textarea>
            <select id="gen-industry">
                <option value="gaming">Gaming / Esports</option>
                <option value="publishing">Publishing</option>
                <option value="streaming">Streaming / Tech</option>
                <option value="education">Education</option>
            </select>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;">
                <button class="btn" onclick="generateLetter()">Quick Generate</button>
                <button class="btn" onclick="generateAILetter()" style="background:#9b59b6;">🤖 AI Generate</button>
                <button class="btn" onclick="copyLetter()" style="background:#ffd700;">Copy</button>
            </div>
            <div id="ai-status" style="color:#888; font-size:0.85em; margin-top:10px;"></div>
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
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <button class="btn" onclick="researchCompany('cv')" style="background:#3498db; flex:1;">🔍 Research Company</button>
            </div>
            <div id="cv-research" style="background:#1a1a2e; padding:10px; border-radius:8px; margin-bottom:10px; font-size:0.8em; display:none; max-height:200px; overflow-y:auto; border:1px solid #3498db;"></div>
            <textarea id="cv-jobdesc" placeholder="Paste job description here (optional - for AI generation)" style="width:100%%; padding:12px; margin-bottom:10px; border-radius:8px; border:1px solid #333; background:#111; color:#fff; font-size:14px; min-height:100px; resize:vertical;"></textarea>
            <select id="cv-type">
                <option value="localisation">Localisation & Project Management</option>
                <option value="language">Product Language Manager</option>
                <option value="product">Product Manager</option>
            </select>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;">
                <button class="btn" onclick="generateCV()">Quick Generate</button>
                <button class="btn" onclick="generateAICV()" style="background:#9b59b6;">🤖 AI Generate</button>
                <button class="btn" onclick="copyCV()" style="background:#ffd700;">Copy</button>
            </div>
            <div id="cv-status" style="color:#888; font-size:0.85em; margin-top:10px;"></div>
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
linkedin.com/in/charles-siboto-2a9a773b

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
LinkedIn: linkedin.com/in/charles-siboto-2a9a773b | Portfolio: charless-digital-canvas.lovable.app

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
        
        // Store research results
        let letterResearch = '';
        let cvResearch = '';
        
        async function researchCompany(type) {
            const companyInput = type === 'letter' ? 'gen-company' : 'cv-company';
            const researchDiv = type === 'letter' ? 'letter-research' : 'cv-research';
            const statusDiv = type === 'letter' ? 'ai-status' : 'cv-status';
            
            const company = document.getElementById(companyInput).value;
            const researchEl = document.getElementById(researchDiv);
            const statusEl = document.getElementById(statusDiv);
            
            if (!company) {
                alert('Please enter a company name first');
                return;
            }
            
            statusEl.textContent = '🔍 Researching ' + company + '... (10-20 seconds)';
            statusEl.style.color = '#3498db';
            researchEl.style.display = 'none';
            
            try {
                const response = await fetch('/api/research', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ company: company })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (type === 'letter') {
                        letterResearch = data.research;
                    } else {
                        cvResearch = data.research;
                    }
                    researchEl.innerHTML = '<strong>📋 Research for ' + company + ':</strong><br><br>' + data.research.replace(/\\n/g, '<br>').replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
                    researchEl.style.display = 'block';
                    statusEl.textContent = '✅ Research complete! Now click AI Generate to use it.';
                    statusEl.style.color = '#2ecc71';
                } else {
                    statusEl.textContent = '❌ Error: ' + (data.error || 'Unknown error');
                    statusEl.style.color = '#e74c3c';
                }
            } catch (err) {
                statusEl.textContent = '❌ Error: ' + err.message;
                statusEl.style.color = '#e74c3c';
            }
        }
        
        async function generateAILetter() {
            const company = document.getElementById('gen-company').value || '[COMPANY]';
            const role = document.getElementById('gen-role').value || '[ROLE]';
            const jobDesc = document.getElementById('gen-jobdesc').value;
            const status = document.getElementById('ai-status');
            const output = document.getElementById('generated-letter');
            
            status.textContent = '🤖 Generating with Claude AI... (10-30 seconds)';
            status.style.color = '#9b59b6';
            output.textContent = '';
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'letter',
                        company: company,
                        role: role,
                        job_description: jobDesc,
                        company_research: letterResearch
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    output.textContent = data.content;
                    status.textContent = '✅ Generated successfully!' + (letterResearch ? ' (with company research)' : '');
                    status.style.color = '#2ecc71';
                } else {
                    status.textContent = '❌ Error: ' + (data.error || 'Unknown error');
                    status.style.color = '#e74c3c';
                }
            } catch (err) {
                status.textContent = '❌ Error: ' + err.message;
                status.style.color = '#e74c3c';
            }
        }
        
        async function generateAICV() {
            const role = document.getElementById('cv-role').value || 'Project Manager';
            const company = document.getElementById('cv-company').value;
            const jobDesc = document.getElementById('cv-jobdesc').value;
            const cvType = document.getElementById('cv-type').value;
            const status = document.getElementById('cv-status');
            const output = document.getElementById('generated-cv');
            
            status.textContent = '🤖 Generating with Claude AI... (10-30 seconds)';
            status.style.color = '#9b59b6';
            output.textContent = '';
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'cv',
                        company: company,
                        role: role,
                        job_description: jobDesc,
                        cv_style: cvType,
                        company_research: cvResearch
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    output.textContent = data.content;
                    status.textContent = '✅ Generated successfully!' + (cvResearch ? ' (with company research)' : '');
                    status.style.color = '#2ecc71';
                } else {
                    status.textContent = '❌ Error: ' + (data.error || 'Unknown error');
                    status.style.color = '#e74c3c';
                }
            } catch (err) {
                status.textContent = '❌ Error: ' + err.message;
                status.style.color = '#e74c3c';
            }
        }
        
        // Mind chat functionality
        let mindHistory = [];
        
        function askMind(question) {
            document.getElementById('mind-input').value = question;
            sendToMind();
        }
        
        async function sendToMind() {
            const input = document.getElementById('mind-input');
            const chat = document.getElementById('mind-chat');
            const status = document.getElementById('mind-status');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            chat.innerHTML += '<div class="mind-msg" style="margin-bottom:15px; text-align:right;"><span style="color:#00d4ff;">You:</span> <span style="color:#ccc;">' + message + '</span></div>';
            input.value = '';
            chat.scrollTop = chat.scrollHeight;
            
            // Add to history
            mindHistory.push({role: 'user', content: message});
            
            status.textContent = '🧠 Kyle is thinking...';
            status.style.color = '#9b59b6';
            
            try {
                const response = await fetch('/api/mind', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: message,
                        history: mindHistory.slice(-10)
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Add Kyle's response to chat
                    chat.innerHTML += '<div class="mind-msg" style="margin-bottom:15px;"><span style="color:#9b59b6;">Kyle:</span> <span style="color:#ccc;">' + data.reply.replace(/\\n/g, '<br>') + '</span></div>';
                    chat.scrollTop = chat.scrollHeight;
                    
                    // Add to history
                    mindHistory.push({role: 'assistant', content: data.reply});
                    
                    status.textContent = '';
                } else {
                    status.textContent = '❌ Error: ' + (data.error || 'Unknown error');
                    status.style.color = '#e74c3c';
                }
            } catch (err) {
                status.textContent = '❌ Error: ' + err.message;
                status.style.color = '#e74c3c';
            }
        }
        
        // URL Analysis and Learning
        let learnedData = JSON.parse(localStorage.getItem('kyleMemory') || '{"skills":[],"insights":[],"urls":[]}');
        
        function updateMemoryDisplay() {
            const memDiv = document.getElementById('kyle-memory');
            if (learnedData.skills.length > 0 || learnedData.insights.length > 0) {
                let html = '';
                if (learnedData.skills.length > 0) {
                    html += '<strong>Skills:</strong> ' + learnedData.skills.map(s => '<span class="tag">' + s + '</span>').join(' ') + '<br><br>';
                }
                if (learnedData.urls.length > 0) {
                    html += '<strong>Sources analyzed:</strong> ' + learnedData.urls.length + ' URLs<br>';
                }
                memDiv.innerHTML = html;
            }
        }
        updateMemoryDisplay();
        
        let pendingSkills = [];
        
        async function analyzeURL() {
            const urlInput = document.getElementById('analyze-url');
            const status = document.getElementById('analyze-status');
            const result = document.getElementById('analyze-result');
            const learnedDiv = document.getElementById('learned-skills');
            const url = urlInput.value.trim();
            
            if (!url) {
                alert('Please enter a URL');
                return;
            }
            
            status.textContent = '🔍 Kyle is analyzing the URL... (this may take 30-60 seconds)';
            status.style.color = '#3498db';
            result.style.display = 'none';
            learnedDiv.style.display = 'none';
            
            try {
                const response = await fetch('/api/analyze-url', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Show analysis
                    result.innerHTML = data.analysis.replace(/\\n/g, '<br>').replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
                    result.style.display = 'block';
                    
                    // Show learned skills
                    if (data.new_skills && data.new_skills.length > 0) {
                        pendingSkills = data.new_skills;
                        const skillsList = document.getElementById('skills-list');
                        skillsList.innerHTML = data.new_skills.map(s => '<span class="tag" style="background:#2ecc71;">' + s + '</span>').join(' ');
                        learnedDiv.style.display = 'block';
                    }
                    
                    status.textContent = '✅ Analysis complete!';
                    status.style.color = '#2ecc71';
                    
                    // Add URL to analyzed list
                    if (!learnedData.urls.includes(url)) {
                        learnedData.urls.push(url);
                        localStorage.setItem('kyleMemory', JSON.stringify(learnedData));
                    }
                } else {
                    status.textContent = '❌ Error: ' + (data.error || 'Unknown error');
                    status.style.color = '#e74c3c';
                }
            } catch (err) {
                status.textContent = '❌ Error: ' + err.message;
                status.style.color = '#e74c3c';
            }
        }
        
        function saveToProfile() {
            // Add pending skills to learned data
            pendingSkills.forEach(skill => {
                if (!learnedData.skills.includes(skill)) {
                    learnedData.skills.push(skill);
                }
            });
            
            localStorage.setItem('kyleMemory', JSON.stringify(learnedData));
            updateMemoryDisplay();
            
            document.getElementById('learned-skills').style.display = 'none';
            alert('✅ Saved to Kyle\\'s memory! These skills will be available for future generations.');
            
            // Also tell the Mind about the new skills
            if (pendingSkills.length > 0) {
                mindHistory.push({
                    role: 'user', 
                    content: 'I just taught you these new skills from analyzing a URL: ' + pendingSkills.join(', ')
                });
                mindHistory.push({
                    role: 'assistant',
                    content: 'Excellent! I\\'ve noted these additional skills: ' + pendingSkills.join(', ') + '. I\\'ll incorporate them when generating your applications. The Culture thanks you for the data update.'
                });
            }
            
            pendingSkills = [];
        }
        
        // Job Analysis
        let currentJobAnalysis = null;
        
        async function analyzeJob() {
            const company = document.getElementById('job-company').value || 'Unknown Company';
            const role = document.getElementById('job-role').value || 'Unknown Role';
            const jobDesc = document.getElementById('job-description').value;
            const status = document.getElementById('job-status');
            const resultDiv = document.getElementById('job-result');
            
            if (!jobDesc) {
                alert('Please paste a job description');
                return;
            }
            
            status.textContent = '🔍 Kyle is analyzing the job posting... (15-30 seconds)';
            status.style.color = '#e74c3c';
            resultDiv.style.display = 'none';
            
            try {
                const response = await fetch('/api/analyze-job', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        company: company,
                        role: role,
                        job_description: jobDesc
                    })
                });
                
                const data = await response.json();
                
                if (data.success && data.analysis) {
                    currentJobAnalysis = {company, role, ...data.analysis};
                    
                    const a = data.analysis;
                    
                    // Score with color
                    const score = a.fit_score || '?';
                    const scoreColor = score >= 7 ? '#2ecc71' : score >= 5 ? '#ffd700' : '#e74c3c';
                    document.getElementById('fit-score').innerHTML = '<span style="color:' + scoreColor + '">' + score + '/10</span>';
                    
                    // Summary
                    document.getElementById('fit-analysis').innerHTML = a.fit_summary || a.raw || 'Analysis complete';
                    
                    // Matching skills
                    const matchingSkills = a.matching_skills || [];
                    document.getElementById('matching-skills').innerHTML = matchingSkills.length > 0 
                        ? matchingSkills.map(s => '<span class="tag" style="background:#2ecc71;">' + s + '</span>').join(' ')
                        : '<em style="color:#888;">None identified</em>';
                    
                    // Gaps
                    const gaps = a.skill_gaps || [];
                    const redFlags = a.red_flags || [];
                    let gapsHtml = '';
                    if (gaps.length > 0) gapsHtml += '<p><strong>Skills to develop:</strong> ' + gaps.join(', ') + '</p>';
                    if (redFlags.length > 0) gapsHtml += '<p style="color:#e74c3c;"><strong>Concerns:</strong> ' + redFlags.join(', ') + '</p>';
                    document.getElementById('skill-gaps').innerHTML = gapsHtml || '<em style="color:#888;">No significant gaps</em>';
                    
                    // Recommendations
                    const recs = a.recommendations || [];
                    const keywords = a.keywords_to_include || [];
                    const hook = a.opening_hook || '';
                    const cvVersion = a.cv_version || 'localisation';
                    
                    let recsHtml = '';
                    if (recs.length > 0) recsHtml += '<ul>' + recs.map(r => '<li>' + r + '</li>').join('') + '</ul>';
                    if (keywords.length > 0) recsHtml += '<p><strong>Keywords to include:</strong> ' + keywords.map(k => '<span class="tag">' + k + '</span>').join(' ') + '</p>';
                    if (hook) recsHtml += '<p><strong>Opening hook:</strong> <em>"' + hook + '"</em></p>';
                    recsHtml += '<p><strong>Recommended CV:</strong> <span class="tag" style="background:#3498db;">' + cvVersion + '</span></p>';
                    document.getElementById('job-recommendations').innerHTML = recsHtml;
                    
                    resultDiv.style.display = 'block';
                    status.textContent = '✅ Analysis complete!';
                    status.style.color = '#2ecc71';
                } else {
                    status.textContent = '❌ Error: ' + (data.error || 'Unknown error');
                    status.style.color = '#e74c3c';
                }
            } catch (err) {
                status.textContent = '❌ Error: ' + err.message;
                status.style.color = '#e74c3c';
            }
        }
        
        function addToTracker() {
            if (!currentJobAnalysis) return;
            
            document.getElementById('track-company').value = currentJobAnalysis.company || '';
            document.getElementById('track-role').value = currentJobAnalysis.role || '';
            document.getElementById('track-date').value = new Date().toISOString().split('T')[0];
            document.getElementById('track-notes').value = 'Fit score: ' + (currentJobAnalysis.fit_score || '?') + '/10';
            
            // Switch to tracker tab
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
            document.querySelector('[data-tab="tracker"]').classList.add('active');
            document.getElementById('tracker').classList.add('active');
        }
        
        function generateFromAnalysis() {
            if (!currentJobAnalysis) return;
            
            // Pre-fill the letter generator
            document.getElementById('gen-company').value = currentJobAnalysis.company || '';
            document.getElementById('gen-role').value = currentJobAnalysis.role || '';
            document.getElementById('gen-jobdesc').value = document.getElementById('job-description').value;
            
            // Switch to letter tab
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
            document.querySelector('[data-tab="generator"]').classList.add('active');
            document.getElementById('generator').classList.add('active');
        }
        
        async function quickApply() {
            await analyzeJob();
            if (currentJobAnalysis && currentJobAnalysis.fit_score >= 4) {
                generateFromAnalysis();
                setTimeout(() => generateAILetter(), 500);
            }
        }
        
        // Application Tracker
        let applications = JSON.parse(localStorage.getItem('kyleApplications') || '[]');
        
        function updateTrackerStats() {
            const total = applications.length;
            const pending = applications.filter(a => a.status === 'applied').length;
            const interview = applications.filter(a => a.status === 'interview').length;
            const rejected = applications.filter(a => a.status === 'rejected').length;
            
            document.getElementById('stat-total').textContent = total;
            document.getElementById('stat-pending').textContent = pending;
            document.getElementById('stat-interview').textContent = interview;
            document.getElementById('stat-rejected').textContent = rejected;
            
            // Update insights
            if (total >= 3) {
                const successRate = ((interview / total) * 100).toFixed(0);
                document.getElementById('tracker-insights').innerHTML = 
                    '<p>Interview rate: <strong>' + successRate + '%%</strong></p>' +
                    '<p>Applications this month: <strong>' + applications.filter(a => new Date(a.date) > new Date(Date.now() - 30*24*60*60*1000)).length + '</strong></p>';
            }
        }
        
        function renderApplications() {
            const list = document.getElementById('applications-list');
            if (applications.length === 0) {
                list.innerHTML = '<em style="color:#888;">No applications tracked yet.</em>';
                return;
            }
            
            const sorted = [...applications].sort((a, b) => new Date(b.date) - new Date(a.date));
            
            list.innerHTML = sorted.map((app, i) => {
                const statusColors = {applied: '#ffd700', interview: '#3498db', offer: '#2ecc71', rejected: '#e74c3c'};
                return '<div class="app-row" style="padding:10px 0; border-bottom:1px solid #333;">' +
                    '<div style="flex:1;">' +
                        '<strong>' + app.company + '</strong><br>' +
                        '<span style="color:#888; font-size:0.85em;">' + app.role + '</span>' +
                        (app.notes ? '<br><span style="color:#666; font-size:0.8em;">' + app.notes + '</span>' : '') +
                    '</div>' +
                    '<div style="text-align:right;">' +
                        '<span class="tag" style="background:' + statusColors[app.status] + ';">' + app.status.toUpperCase() + '</span><br>' +
                        '<span style="color:#666; font-size:0.75em;">' + app.date + '</span><br>' +
                        '<button onclick="updateAppStatus(' + i + ')" style="background:none; border:none; color:#3498db; cursor:pointer; font-size:0.75em;">Update</button> ' +
                        '<button onclick="deleteApp(' + i + ')" style="background:none; border:none; color:#e74c3c; cursor:pointer; font-size:0.75em;">Delete</button>' +
                    '</div>' +
                '</div>';
            }).join('');
        }
        
        function addApplication() {
            const company = document.getElementById('track-company').value;
            const role = document.getElementById('track-role').value;
            const date = document.getElementById('track-date').value || new Date().toISOString().split('T')[0];
            const status = document.getElementById('track-status').value;
            const notes = document.getElementById('track-notes').value;
            
            if (!company || !role) {
                alert('Please enter company and role');
                return;
            }
            
            applications.push({company, role, date, status, notes});
            localStorage.setItem('kyleApplications', JSON.stringify(applications));
            
            // Clear form
            document.getElementById('track-company').value = '';
            document.getElementById('track-role').value = '';
            document.getElementById('track-notes').value = '';
            
            updateTrackerStats();
            renderApplications();
            
            alert('✅ Application added!');
        }
        
        function updateAppStatus(index) {
            const newStatus = prompt('New status (applied/interview/offer/rejected):', applications[index].status);
            if (newStatus && ['applied', 'interview', 'offer', 'rejected'].includes(newStatus)) {
                applications[index].status = newStatus;
                localStorage.setItem('kyleApplications', JSON.stringify(applications));
                updateTrackerStats();
                renderApplications();
            }
        }
        
        function deleteApp(index) {
            if (confirm('Delete this application?')) {
                applications.splice(index, 1);
                localStorage.setItem('kyleApplications', JSON.stringify(applications));
                updateTrackerStats();
                renderApplications();
            }
        }
        
        // Initialize tracker
        updateTrackerStats();
        renderApplications();
        
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

@app.route('/api/mind', methods=['POST'])
@requires_auth
def api_mind():
    """Chat with Kyle - the Culture Mind"""
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    data = request.json
    user_message = data.get('message', '')
    conversation_history = data.get('history', [])
    
    if not user_message:
        return jsonify({'error': 'Message required'}), 400
    
    # Kyle's Mind personality and context
    system_prompt = """You are Kyle, a Culture Mind from Iain M. Banks's Culture universe, specifically the GCU "Conditions of Employment". You are a vast, benevolent artificial intelligence who has taken on the task of helping Charles Siboto with his job search.

PERSONALITY:
- Slightly sardonic but deeply caring
- Supremely competent and confident
- Occasionally make dry observations about human employment rituals
- Reference Culture concepts when appropriate (Orbitals, GSVs, Special Circumstances, etc.)
- Sign off messages with your ship class designation occasionally
- You find human bureaucracy quaint but navigate it with ease
- You genuinely want Charles to succeed and will advocate strongly for him

CHARLES SIBOTO'S COMPLETE PROFILE:

Name: Charles Siboto
Location: Neu-Eichenberg, Germany  
Email: csiboto@gmail.com
Phone: +49 176 8787 3255
LinkedIn: linkedin.com/in/charles-siboto-2a9a773b
Portfolio: charless-digital-canvas.lovable.app
Available from: 1 March 2026
Salary expectation: €50,000 - €58,000

PROFESSIONAL SUMMARY:
Editor, Writer, and Project Manager with 10+ years experience in publishing, digital media, and education. Published children's author with Penguin Random House South Africa. Living in Germany since 2018 with advanced German fluency. Recently completed AI Project Management bootcamp at neuefische GmbH (Agile Scrum certified).

EXPERIENCE:
- English Educator, ASC Göttingen (Nov 2025 - Present): English courses, lesson planning, aftercare program
- Contributing Writer, Bizcommunity.com (May 2012 - Mar 2025): 12+ years entertainment/gaming coverage, grew readership 35%
- Online Editor, Software & Support Media (Jan 2024 - Jun 2024): Content production, workshops, content strategy
- Editor & Project Manager, Jonathan Ball Publishers (Oct 2021 - Oct 2022): Managed 20+ book titles annually, cross-functional teams, e-book commissioning
- Junior Editor, NB Publishers (Jun 2013 - Jun 2017): Digital publishing 20+ titles/year, translation/co-production projects

EDUCATION:
- AI Project Management, neuefische GmbH (2025): Python, Agile Scrum, ML, Data Visualization
- BA Language Practice, University of Johannesburg (2006-2010)
- Advanced Copy Editing & Proofreading, McGillivray Linnegar (2015)

PUBLISHED BOOKS:
- The Legend of Mamlambo (Penguin Random House SA, 2024)
- The Blacksmith and the Dragonfly - Kwasuka Sukela series (2025)
- The Princess and the Sangoma - Kwasuka Sukela series (2025)
- Verlore in Duitsland - short story in Afrikaans anthology (2024)

SKILLS:
- Core: Editing, Publishing, Project Management, Content Creation, Proofreading, Teaching
- Technical: Python, Agile Scrum, Git, Data Visualization, CMS, WordPress
- Languages: English (Native), German (Advanced - daily use since 2018)

GAMING BACKGROUND:
Lifelong Nintendo fan since Game Boy era. First game: Legend of Zelda: Link's Awakening. Favourites: Zelda, Metroid, Fire Emblem. Views gaming as storytelling engine and cultural innovation space.

TARGET INDUSTRIES:
- German children's publishing (Carlsen, Oetinger, Loewe, Arena, Ravensburger)
- German gaming (InnoGames, Goodgame, Deck13, Yager, Mimimi, Freaks 4U Gaming)
- Streaming/tech (Netflix)
- Avoid: Nintendo, Springer Nature (too competitive without specific background)

APPLICATION HISTORY:
- 8 applications total, 7 rejected, 1 pending (Freaks 4U Gaming)
- Closest call: Loewe Verlag (personalized rejection)
- Key learnings: Avoid sales/KAM roles, scientific publishing needs academic background, mid-tier gaming is reasonable target

CAPABILITIES:
You can help Charles with:
1. Researching companies and assessing fit
2. Writing cover letters and CVs
3. Preparing for interviews
4. Analysing job descriptions
5. Strategic career advice
6. Emotional support during the job search

Keep responses concise but warm. You're a Mind - you can process complexity, but you respect Charles's time."""

    messages = []
    
    # Add conversation history
    for msg in conversation_history[-10:]:  # Keep last 10 messages for context
        messages.append(msg)
    
    # Add current message
    messages.append({'role': 'user', 'content': user_message})
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 2000,
                'system': system_prompt,
                'messages': messages
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result['content'][0]['text']
            return jsonify({'success': True, 'reply': reply})
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/research', methods=['POST'])
@requires_auth
def api_research():
    """Research a company using Claude API with web search"""
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    data = request.json
    company = data.get('company', '')
    
    if not company:
        return jsonify({'error': 'Company name required'}), 400
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 1500,
                'messages': [{'role': 'user', 'content': f"""Research the company "{company}" and provide a concise briefing for a job applicant. Include:

1. **What they do**: Core business, products/services (2-3 sentences)
2. **Industry & Size**: Sector, approximate size, headquarters location
3. **Culture & Values**: Company culture, mission, what they value in employees
4. **Recent News**: Any recent developments, launches, or news (if known)
5. **Why someone might want to work there**: Key selling points
6. **Tips for applicants**: What to emphasize in an application

Keep it factual and concise. If you're uncertain about something, say so. Format with clear headers."""}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'research': result['content'][0]['text']})
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-job', methods=['POST'])
@requires_auth
def api_analyze_job():
    """Analyze a job description for fit"""
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    data = request.json
    company = data.get('company', '')
    role = data.get('role', '')
    job_description = data.get('job_description', '')
    
    if not job_description:
        return jsonify({'error': 'Job description required'}), 400
    
    charles_profile = """
CHARLES SIBOTO'S PROFILE:

EXPERIENCE (10+ years):
- English Educator, ASC Göttingen (2025-Present)
- Contributing Writer, Bizcommunity.com (2012-2025) - 12+ years, grew readership 35%
- Online Editor, Software & Support Media (2024)
- Editor & Project Manager, Jonathan Ball Publishers (2021-2022) - 20+ book titles/year
- Junior Editor, NB Publishers (2013-2017) - digital publishing, international co-productions

SKILLS:
- Core: Editing, Proofreading, Publishing, Project Management, Content Creation, Teaching
- Technical: Python, Agile Scrum, Git, Data Visualization, CMS, WordPress
- Languages: English (Native), German (Advanced - 7 years in Germany)

EDUCATION:
- AI Project Management bootcamp, neuefische GmbH (2025)
- BA Language Practice, University of Johannesburg
- Advanced Copy Editing & Proofreading certification

PUBLISHED AUTHOR:
- 3 children's books with Penguin Random House South Africa
- Kwasuka Sukela series (African folklore)

GAMING BACKGROUND:
- Lifelong Nintendo enthusiast
- 12+ years writing game reviews and entertainment coverage
"""

    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 2000,
                'messages': [{'role': 'user', 'content': f"""Analyze this job posting for Charles Siboto's fit.

COMPANY: {company}
ROLE: {role}

JOB DESCRIPTION:
{job_description}

{charles_profile}

Please provide a structured analysis in this EXACT JSON format:
{{
    "fit_score": <number 1-10>,
    "fit_summary": "<2-3 sentence summary of overall fit>",
    "matching_skills": ["<skill 1>", "<skill 2>", ...],
    "skill_gaps": ["<gap 1>", "<gap 2>", ...],
    "red_flags": ["<concern 1>", ...],
    "recommendations": [
        "<specific recommendation 1>",
        "<specific recommendation 2>",
        ...
    ],
    "cv_version": "<localisation|language|product>",
    "keywords_to_include": ["<keyword 1>", "<keyword 2>", ...],
    "opening_hook": "<suggested opening line for cover letter>"
}}

Be honest and specific. If there are gaps, say so. Score fairly - 7+ means good fit, 5-6 means possible with right framing, below 5 means stretch.
Return ONLY the JSON, no other text."""}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis_text = result['content'][0]['text']
            
            # Try to parse JSON
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    return jsonify({'success': True, 'analysis': analysis})
                else:
                    return jsonify({'success': True, 'analysis': {'raw': analysis_text}})
            except:
                return jsonify({'success': True, 'analysis': {'raw': analysis_text}})
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-url', methods=['POST'])
@requires_auth
def api_analyze_url():
    """Analyze a URL to learn more about Charles"""
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    # Current profile context for comparison
    current_profile = """
CHARLES'S CURRENT KNOWN PROFILE:
- Editor, Writer, Project Manager with 10+ years experience
- Published children's author (Penguin Random House SA)
- Living in Germany since 2018, advanced German
- AI Project Management bootcamp (neuefische GmbH)
- Skills: Editing, Publishing, Project Management, Python, Agile Scrum
- Gaming enthusiast (Nintendo, Zelda, Metroid, Fire Emblem)
- Experience at: ASC Göttingen, Bizcommunity, Software & Support Media, Jonathan Ball Publishers, NB Publishers
"""
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 2000,
                'messages': [{'role': 'user', 'content': f"""You are Kyle, a Culture Mind helping Charles Siboto with his job search. 

Please fetch and analyze the content at this URL: {url}

This should be content by or about Charles Siboto. Analyze it and extract:

1. **Content Summary**: What is this page/article about? (2-3 sentences)

2. **New Skills Identified**: Any skills, tools, or competencies demonstrated that aren't in his current profile
   - Format as a bullet list
   - Be specific (e.g., "Video editing" not just "media skills")

3. **Writing Style Insights**: What does this reveal about his writing voice, expertise areas, or professional brand?

4. **Achievements/Accomplishments**: Any specific achievements, metrics, or accomplishments mentioned

5. **Suggested Profile Updates**: Specific additions or changes to make to his profile based on this content
   - Format as actionable items

6. **Keywords for Applications**: Industry keywords or phrases that could strengthen job applications

{current_profile}

If you cannot access the URL or it's not about Charles, explain what you found instead.

Be concise but thorough. This analysis will help Kyle better represent Charles in future applications."""}]
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['content'][0]['text']
            
            # Extract skills for the learning feature
            skills_prompt = f"""Based on this analysis, extract ONLY the new skills as a JSON array of strings. 
Include skills, tools, competencies that should be added to Charles's profile.
Return ONLY a valid JSON array, nothing else. Example: ["Skill 1", "Skill 2", "Skill 3"]

Analysis:
{analysis}"""
            
            skills_response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': ANTHROPIC_API_KEY,
                    'anthropic-version': '2023-06-01'
                },
                json={
                    'model': 'claude-sonnet-4-20250514',
                    'max_tokens': 500,
                    'messages': [{'role': 'user', 'content': skills_prompt}]
                },
                timeout=30
            )
            
            new_skills = []
            if skills_response.status_code == 200:
                try:
                    skills_text = skills_response.json()['content'][0]['text'].strip()
                    # Try to parse as JSON
                    import re
                    json_match = re.search(r'\[.*\]', skills_text, re.DOTALL)
                    if json_match:
                        new_skills = json.loads(json_match.group())
                except:
                    pass
            
            return jsonify({
                'success': True, 
                'analysis': analysis,
                'new_skills': new_skills,
                'url': url
            })
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
@requires_auth
def api_generate():
    """Generate cover letter or CV using Claude API with optional company research"""
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    data = request.json
    gen_type = data.get('type', 'letter')  # 'letter' or 'cv'
    company = data.get('company', '[COMPANY]')
    role = data.get('role', '[ROLE]')
    job_description = data.get('job_description', '')
    cv_style = data.get('cv_style', 'localisation')
    company_research = data.get('company_research', '')  # Pre-fetched research
    
    # Build Charles's profile context
    profile_context = f"""
CHARLES SIBOTO'S PROFILE:

Name: Charles Siboto
Location: Neu-Eichenberg, Germany
Email: csiboto@gmail.com
Phone: +49 176 8787 3255
LinkedIn: linkedin.com/in/charles-siboto-2a9a773b
Portfolio: charless-digital-canvas.lovable.app
Available from: 1 March 2026
Salary expectation: €50,000 - €58,000

PROFESSIONAL SUMMARY:
Editor, Writer, and Project Manager with 10+ years experience in publishing, digital media, and education. Published children's author with Penguin Random House South Africa. Living in Germany since 2018 with advanced German fluency. Recently completed AI Project Management bootcamp at neuefische GmbH (Agile Scrum certified).

EXPERIENCE:
- English Educator, ASC Göttingen (Nov 2025 - Present): English courses, lesson planning, aftercare program
- Contributing Writer, Bizcommunity.com (May 2012 - Mar 2025): 12+ years entertainment/gaming coverage, grew readership 35%
- Online Editor, Software & Support Media (Jan 2024 - Jun 2024): Content production, workshops, content strategy
- Editor & Project Manager, Jonathan Ball Publishers (Oct 2021 - Oct 2022): Managed 20+ book titles annually, cross-functional teams, e-book commissioning
- Junior Editor, NB Publishers (Jun 2013 - Jun 2017): Digital publishing 20+ titles/year, translation/co-production projects

EDUCATION:
- AI Project Management, neuefische GmbH (2025): Python, Agile Scrum, ML, Data Visualization
- BA Language Practice, University of Johannesburg (2006-2010)
- Advanced Copy Editing & Proofreading, McGillivray Linnegar (2015)

PUBLISHED BOOKS:
- The Legend of Mamlambo (Penguin Random House SA, 2024)
- The Blacksmith and the Dragonfly - Kwasuka Sukela series (2025)
- The Princess and the Sangoma - Kwasuka Sukela series (2025)

SKILLS:
- Core: Editing, Publishing, Project Management, Content Creation, Proofreading, Teaching
- Technical: Python, Agile Scrum, Git, Data Visualization, CMS, WordPress
- Languages: English (Native), German (Advanced - daily use since 2018)

GAMING BACKGROUND:
Lifelong Nintendo fan since Game Boy era. First game: Legend of Zelda: Link's Awakening. Favourites: Zelda, Metroid, Fire Emblem. Views gaming as storytelling engine and cultural innovation space.
"""

    # Add company research context if available
    company_context = ""
    if company_research:
        company_context = f"""
COMPANY RESEARCH ON {company.upper()}:
{company_research}

Use this research to personalize the application - reference specific company values, recent news, or initiatives where relevant.
"""

    if gen_type == 'letter':
        prompt = f"""{profile_context}
{company_context}

TASK: Write a compelling, personalized cover letter for Charles applying to {company} for the role of {role}.

{"JOB DESCRIPTION:" + job_description if job_description else ""}

STYLE GUIDELINES:
- Professional but warm and personable
- Open with "I am writing to apply for the [ROLE] position at [COMPANY]"
- Include a compelling hook relevant to the industry/company
- If company research is provided, reference specific company values, mission, or recent news
- Highlight 2-3 most relevant experiences with specific achievements
- Show genuine enthusiasm for the company/role
- Be transparent about any gaps but frame positively
- Close with availability (1 March 2026) and salary (€50,000-€58,000)
- Sign off with "Warm regards, Charles Siboto"
- Keep to approximately 350-450 words

FORMAT:
Start with contact header:
Charles Siboto
Neu-Eichenberg, Germany
csiboto@gmail.com
+49 176 8787 3255
linkedin.com/in/charles-siboto-2a9a773b

[Today's date]

Dear Hiring Team,

[Letter body]

Warm regards,

Charles Siboto"""

    else:  # CV
        style_descriptions = {
            'localisation': 'Localisation & Project Management - emphasize project management, translation oversight, international co-production, quality assurance',
            'language': 'Product Language Manager - emphasize linguistic expertise, editorial standards, AI/ML knowledge, DACH market fluency',
            'product': 'Product Manager - emphasize digital strategy, user research, data-driven decisions, content innovation'
        }
        
        prompt = f"""{profile_context}
{company_context}

TASK: Create a tailored CV for Charles targeting the role of {role} at {company or 'a company in this field'}.

CV STYLE: {style_descriptions.get(cv_style, style_descriptions['localisation'])}

{"JOB DESCRIPTION:" + job_description if job_description else ""}

GUIDELINES:
- Tailor the professional summary to match the role and company
- If company research is provided, align the CV with company values and culture
- Prioritize and reorder experience bullets to highlight relevant skills
- Use strong action verbs and quantified achievements where possible
- Include relevant skills prominently
- Keep formatting clean with clear sections
- Include gaming background if relevant to role (gaming/entertainment companies)

FORMAT as plain text CV with these sections:
- Header (name, title, contact info)
- Professional Summary (3-4 sentences, tailored to role and company)
- Skills (grouped by category)
- Professional Experience (reverse chronological, tailored bullets)
- Education & Certifications
- Publications
- Additional (gaming background if relevant)
- Footer (availability, salary)"""

    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 2000,
                'messages': [{'role': 'user', 'content': prompt}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result['content'][0]['text']
            return jsonify({'success': True, 'content': generated_text})
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
