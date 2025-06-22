# PowerShell script to set up GitHub repository for MarsPro project
# Run this script after creating the repository on GitHub

param(
    [Parameter(Mandatory=$true)]
    [string]$RepositoryUrl,
    
    [Parameter(Mandatory=$false)]
    [string]$BranchName = "main"
)

Write-Host "🚀 Setting up GitHub repository for MarsPro project..." -ForegroundColor Green

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found. Please install Git first:" -ForegroundColor Red
    Write-Host "   Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Initialize git repository
Write-Host "📁 Initializing git repository..." -ForegroundColor Blue
git init

# Add all files
Write-Host "📝 Adding files to repository..." -ForegroundColor Blue
git add .

# Create initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Blue
git commit -m "Initial commit: MarsPro reverse engineering and Home Assistant integration

- Complete static analysis of MarsPro Android app
- Home Assistant integration framework
- Frida hooks for dynamic analysis
- Comprehensive documentation
- Configuration examples

Phase 1: Static analysis complete
Next: Dynamic analysis and protocol discovery"

# Add remote repository
Write-Host "🔗 Adding remote repository..." -ForegroundColor Blue
git remote add origin $RepositoryUrl

# Set branch name
Write-Host "🌿 Setting branch name to '$BranchName'..." -ForegroundColor Blue
git branch -M $BranchName

# Push to GitHub
Write-Host "⬆️ Pushing to GitHub..." -ForegroundColor Blue
git push -u origin $BranchName

Write-Host "✅ Repository setup complete!" -ForegroundColor Green
Write-Host "🌐 Your repository is now available at: $RepositoryUrl" -ForegroundColor Cyan

# Display next steps
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Set up GitHub Pages (optional):" -ForegroundColor White
Write-Host "   - Go to repository Settings > Pages" -ForegroundColor Gray
Write-Host "   - Enable GitHub Pages from main branch" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Set up repository topics:" -ForegroundColor White
Write-Host "   - Go to repository main page" -ForegroundColor Gray
Write-Host "   - Click 'Add topics' and add: home-assistant, reverse-engineering, ble, iot" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Create releases for major versions:" -ForegroundColor White
Write-Host "   - Go to repository > Releases" -ForegroundColor Gray
Write-Host "   - Create new release with version tags" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Set up issue templates (optional):" -ForegroundColor White
Write-Host "   - Create .github/ISSUE_TEMPLATE/ directory" -ForegroundColor Gray
Write-Host "   - Add bug_report.md and feature_request.md" -ForegroundColor Gray 