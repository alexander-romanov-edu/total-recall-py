# TOTAL RECALL

A minimal, fast, and slightly cinematic way to memorize English words.
The aim of this project is to solve the lack of word-recalling applications
that allow you to enter your own words and form personal dictionaries.

Inspired by active recall learning and the _“memory implant”_ vibe of the
movie **Total Recall**.

## ![](./examples/totalrecall.png)

## ✨ Features

- 📚 Create custom word collections
- ✍️ Add words quickly with a clean UI
- 🧠 Train using **active recall** (type the answer)
- ⚡ Instant feedback + scoring
- 🎬 Fun “Total Recall” themed study intro

---

## 🧪 How it works

Instead of passively reading words, you:

1. See a **masked word**
1. Type your answer
1. Get **immediate feedback**
1. Repeat

This reinforces memory much more effectively than flashcards alone.

---

## 🚀 Getting started

### 1. Enter development shell (Nix)

```bash
nix develop
```

### 2. Run migrations

```bash
python manage.py migrate
```

### 3. Create admin user

This is needed to add word collections that are shown for all users.

### 4. Start server

```bash
python manage.py runserver
```

### 5. Open admin panel in browser

```
http://localhost:8000/admin
```

Here you can configure global word collections

### 6. Open regular panel

(optionaly): sing up as a new user

```
http://localhost:8000/
```

![](./examples/homepage.png)

---

## 🧠 Training flow

- Click **Study**
- Get a short cinematic intro
- Type answers continuously
- Track your score

No distractions. Just recall.

---

## 📜 License

MIT License with AI Restriction
