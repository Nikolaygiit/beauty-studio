# Auto-deploy script for GitHub Pages
# Run: .\deploy.ps1

Write-Host "Preparing deployment to GitHub Pages..." -ForegroundColor Cyan

# Check Git
try {
    $gitVersion = git --version
    Write-Host "[OK] Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git not found. Install Git: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# Check if repository is initialized
if (-not (Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Repository initialized" -ForegroundColor Green
} else {
    Write-Host "[OK] Git repository already exists" -ForegroundColor Green
}

# Add files and auto-commit
Write-Host "Adding files..." -ForegroundColor Yellow
git add .

# Check status
$status = git status --porcelain
if ($status) {
    Write-Host "Changes to commit:" -ForegroundColor Yellow
    git status --short
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commitMessage = "chore: auto-deploy ($timestamp)"
    
    git commit -m $commitMessage
    Write-Host "[OK] Auto-commit completed: $commitMessage" -ForegroundColor Green
} else {
    Write-Host "[INFO] No changes to commit" -ForegroundColor Yellow
}

# Check remote
$remote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Remote origin not configured." -ForegroundColor Red
    Write-Host "Add it once with command:" -ForegroundColor Yellow
    Write-Host "  git remote add origin https://github.com/Nikolaygiit/beauty-studio.git" -ForegroundColor White
    exit 1
} else {
    Write-Host "[OK] Remote configured: $remote" -ForegroundColor Green
}

# Rename branch to main if needed
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "Renaming branch to main..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "[OK] Branch renamed to main" -ForegroundColor Green
}

# Push
Write-Host ""
Write-Host "Uploading to GitHub..." -ForegroundColor Yellow
Write-Host "[WARNING] If authentication required, use Personal Access Token instead of password" -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] Code successfully uploaded to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Open your repository on GitHub" -ForegroundColor White
    Write-Host "2. Go to Settings -> Pages" -ForegroundColor White
    Write-Host "3. Select branch: main, folder: / (root)" -ForegroundColor White
    Write-Host "4. Click Save" -ForegroundColor White
    Write-Host "5. In 1-2 minutes site will be available at:" -ForegroundColor White
    Write-Host "   https://nikolaygiit.github.io/beauty-studio/" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "[ERROR] Upload error. Check:" -ForegroundColor Red
    Write-Host "  - Repository URL is correct" -ForegroundColor White
    Write-Host "  - You have access rights" -ForegroundColor White
    Write-Host "  - Using Personal Access Token" -ForegroundColor White
}
