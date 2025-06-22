# GitHub Repository Setup Instructions

This guide will help you create a GitHub repository and push the MarsPro project to it.

## Prerequisites

1. **Git installed** on your system
   - Download from: https://git-scm.com/download/win
   - Or install via package manager: `winget install Git.Git`

2. **GitHub account** with repository creation permissions

## Method 1: Using the Setup Scripts (Recommended)

### Windows (PowerShell)
```powershell
# Run the PowerShell script
.\scripts\setup_github_repo.ps1 -RepositoryUrl "https://github.com/your-username/marspro-analysis.git"
```

### Windows (Command Prompt)
```cmd
# Run the batch script
scripts\setup_github_repo.bat
```

## Method 2: Manual Setup

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon in the top right
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `marspro-analysis` (or your preferred name)
   - **Description**: `MarsPro reverse engineering and Home Assistant integration`
   - **Visibility**: Public (recommended) or Private
   - **Initialize with**: Leave unchecked (we'll push our existing code)
5. Click "Create repository"

### Step 2: Initialize Local Repository

Open a terminal in your project directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: MarsPro reverse engineering and Home Assistant integration

- Complete static analysis of MarsPro Android app
- Home Assistant integration framework
- Frida hooks for dynamic analysis
- Comprehensive documentation
- Configuration examples

Phase 1: Static analysis complete
Next: Dynamic analysis and protocol discovery"

# Add remote repository (replace with your actual URL)
git remote add origin https://github.com/your-username/marspro-analysis.git

# Set branch name to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## Method 3: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Create repository
gh repo create marspro-analysis --public --description "MarsPro reverse engineering and Home Assistant integration"

# Initialize and push
git init
git add .
git commit -m "Initial commit: MarsPro reverse engineering and Home Assistant integration"
git branch -M main
git push -u origin main
```

## Post-Setup Tasks

After successfully pushing to GitHub, consider these optional enhancements:

### 1. Set Repository Topics

Go to your repository page and add these topics:
- `home-assistant`
- `reverse-engineering`
- `ble`
- `iot`
- `smart-home`
- `python`

### 2. Enable GitHub Pages (Optional)

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: main
4. Folder: / (root)
5. Click Save

### 3. Create a Release

1. Go to repository → Releases
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Initial Release - Static Analysis Complete`
5. Description: Include the project summary and features

### 4. Set Up Issue Templates

The repository already includes issue templates in `.github/ISSUE_TEMPLATE/`:
- `bug_report.md`
- `feature_request.md`

### 5. Add Repository Description

Update your repository description to:
```
MarsPro reverse engineering and Home Assistant integration for local device control without cloud dependency. Features BLE communication, comprehensive analysis tools, and complete documentation.
```

## Troubleshooting

### Git Not Found
- Install Git from https://git-scm.com/download/win
- Restart your terminal after installation

### Authentication Issues
- Use GitHub CLI: `gh auth login`
- Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Large File Issues
- The `.gitignore` file excludes large APK files and analysis outputs
- If you still have issues, use Git LFS: `git lfs install`

### Push Permission Denied
- Check your repository URL
- Ensure you have write access to the repository
- Verify your GitHub authentication

## Repository Structure

Your repository will contain:

```
marspro-analysis/
├── .github/                    # GitHub templates and workflows
├── custom_components/marspro/  # Home Assistant integration
├── docs/                       # Documentation
├── scripts/                    # Setup and analysis scripts
├── configuration_samples/      # Configuration examples
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT license
├── README.md                   # Project documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
└── .pre-commit-config.yaml     # Code quality hooks
```

## Next Steps

1. **Share your repository** with the community
2. **Set up development environment** using the instructions in README.md
3. **Continue development** with Phase 2 (dynamic analysis)
4. **Contribute** to the project following CONTRIBUTING.md guidelines

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review GitHub's documentation: https://docs.github.com/
3. Create an issue in your repository for specific problems 