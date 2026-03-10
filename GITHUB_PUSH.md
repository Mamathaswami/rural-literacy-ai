# How to Push to GitHub

## Option 1: Using Git Commands (Manual)

### Step 1: Initialize Git (if not already done)
```bash
git init
```

### Step 2: Configure Git (if new)
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Step 3: Create .gitignore
Create a `.gitignore` file:
```
__pycache__/
*.pyc
.venv/
venv/
data/*.db
data/*.db-journal
*.log
.env
.DS_Store
.gitignore
```

### Step 4: Add files to Git
```bash
git add .
```

### Step 5: Commit
```bash
git commit -m "Initial commit - Rural Literacy AI Tool"
```

### Step 6: Create repository on GitHub.com
1. Go to https://github.com/new
2. Repository name: `rural-literacy-ai`
3. Click "Create repository"

### Step 7: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/rural-literacy-ai.git
git branch -M main
git push -u origin main
```

---

## Option 2: Using GitHub Desktop
1. Download GitHub Desktop from https://desktop.github.com
2. Open it and sign in
3. File > Add Local Repository
4. Select your project folder
5. Click "Publish repository"
6. Done!

---

## Option 3: Using VS Code
1. Install GitHub extension in VS Code
2. Click on "Source Control" icon in sidebar
3. Click "Initialize Repository"
4. Enter commit message and click ✓
5. Click "Publish to GitHub"
6. Done!

