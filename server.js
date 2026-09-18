const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { DatabaseSync } = require('node:sqlite');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-in-production';
const JWT_EXPIRES = '30d';

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Database setup (node:sqlite — built into Node 22.5+, no native compile needed)
const db = new DatabaseSync('cissp_progress.db');

// Foreign keys enforcement
db.exec('PRAGMA foreign_keys = ON;');

// Initialize tables
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    picked TEXT,
    correct INTEGER,
    revealed INTEGER DEFAULT 0,
    marked INTEGER DEFAULT 0,
    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, question_id)
  );

  CREATE TABLE IF NOT EXISTS section_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    section_id TEXT NOT NULL,
    domain_id INTEGER NOT NULL,
    answered INTEGER DEFAULT 0,
    correct INTEGER DEFAULT 0,
    marked INTEGER DEFAULT 0,
    last_question_index INTEGER DEFAULT 0,
    show_guide INTEGER DEFAULT 1,
    filter TEXT DEFAULT 'all',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, section_id)
  );

  CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);
  CREATE INDEX IF NOT EXISTS idx_section_progress_user ON section_progress(user_id);
`);

// Auth middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Access token required' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Invalid or expired token' });
    req.user = user;
    next();
  });
}

// Auth routes
app.get('/api/auth/status', (req, res) => {
  res.json({ available: true });
});

app.post('/api/auth/register', async (req, res) => {
  try {
    let { email, password } = req.body || {};
    if (typeof email !== 'string' || typeof password !== 'string' || !email.trim() || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }
    email = email.trim().toLowerCase();
    if (!/^\S+@\S+\.\S+$/.test(email)) return res.status(400).json({ error: 'Enter a valid email address' });
    if (password.length < 8) return res.status(400).json({ error: 'Password must be at least 8 characters' });

    const existing = db.prepare('SELECT id FROM users WHERE lower(email) = ?').get(email);
    if (existing) return res.status(409).json({ error: 'Email already registered' });

    const passwordHash = await bcrypt.hash(password, 12);
    const result = db.prepare('INSERT INTO users (email, password_hash) VALUES (?, ?)').run(email, passwordHash);
    const user = { id: result.lastInsertRowid, email };

    const token = jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: JWT_EXPIRES });
    res.status(201).json({ user, token });
  } catch (e) {
    console.error('Register error:', e);
    res.status(500).json({ error: 'Registration failed' });
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    let { email, password } = req.body || {};
    if (typeof email !== 'string' || typeof password !== 'string' || !email.trim() || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }
    email = email.trim().toLowerCase();

    const user = db.prepare('SELECT * FROM users WHERE lower(email) = ?').get(email);
    if (!user) return res.status(401).json({ error: 'Invalid credentials' });

    const valid = await bcrypt.compare(password, user.password_hash);
    if (!valid) return res.status(401).json({ error: 'Invalid credentials' });

    const token = jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: JWT_EXPIRES });
    res.json({ user: { id: user.id, email: user.email }, token });
  } catch (e) {
    console.error('Login error:', e);
    res.status(500).json({ error: 'Login failed' });
  }
});

app.get('/api/auth/me', authenticateToken, (req, res) => {
  const user = db.prepare('SELECT id, email, created_at FROM users WHERE id = ?').get(req.user.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json({ user });
});

// Progress routes
app.get('/api/progress', authenticateToken, (req, res) => {
  const progress = db.prepare('SELECT question_id, picked, correct, revealed, marked, answered_at FROM progress WHERE user_id = ?').all(req.user.id);
  const sectionProgress = db.prepare('SELECT section_id, domain_id, answered, correct, marked, last_question_index, show_guide, filter FROM section_progress WHERE user_id = ?').all(req.user.id);
  res.json({ progress, sectionProgress });
});

app.post('/api/progress', authenticateToken, (req, res) => {
  const { progress: progressData, sectionProgress: sectionProgressData } = req.body || {};
  const userId = req.user.id;

  if (progressData !== undefined && !Array.isArray(progressData)) {
    return res.status(400).json({ error: 'Progress must be an array' });
  }
  if (sectionProgressData !== undefined && !Array.isArray(sectionProgressData)) {
    return res.status(400).json({ error: 'Section progress must be an array' });
  }

  try {
    db.exec('BEGIN');
    if (progressData) {
      // The client sends its full merged state. Replacing this user's rows makes
      // reset, unmark and unreveal actions sync correctly as well as additions.
      db.prepare('DELETE FROM progress WHERE user_id = ?').run(userId);
      const upsertProgress = db.prepare(`
        INSERT INTO progress (user_id, question_id, picked, correct, revealed, marked)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, question_id) DO UPDATE SET
          picked = excluded.picked,
          correct = excluded.correct,
          revealed = excluded.revealed,
          marked = excluded.marked,
          answered_at = CURRENT_TIMESTAMP
      `);
      for (const p of progressData) {
        upsertProgress.run(userId, p.questionId, p.picked, p.correct ? 1 : 0, p.revealed ? 1 : 0, p.marked ? 1 : 0);
      }
    }
    if (sectionProgressData) {
      db.prepare('DELETE FROM section_progress WHERE user_id = ?').run(userId);
      const upsertSection = db.prepare(`
        INSERT INTO section_progress (user_id, section_id, domain_id, answered, correct, marked, last_question_index, show_guide, filter)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, section_id) DO UPDATE SET
          answered = excluded.answered,
          correct = excluded.correct,
          marked = excluded.marked,
          last_question_index = excluded.last_question_index,
          show_guide = excluded.show_guide,
          filter = excluded.filter
      `);
      for (const s of sectionProgressData) {
        upsertSection.run(userId, s.sectionId, s.domainId, s.answered, s.correct, s.marked, s.lastQuestionIndex, s.showGuide ? 1 : 0, s.filter);
      }
    }
    db.exec('COMMIT');
    res.json({ success: true });
  } catch (e) {
    db.exec('ROLLBACK');
    console.error('Progress save error:', e);
    res.status(500).json({ error: 'Failed to save progress' });
  }
});

// Serve the main app shell
app.get(['/', '/index.html'], (req, res) => {
  res.sendFile(path.join(__dirname, 'CISSP_Study_Portal.html'));
});

// The question bank lives at the repo root, next to the HTML shell.
app.get('/cissp-data.js', (req, res) => {
  res.type('application/javascript').sendFile(path.join(__dirname, 'cissp-data.js'));
});

app.listen(PORT, () => {
  console.log(`CISSP Study Portal server running on http://localhost:${PORT}`);
});
