# Quick Start: Setting Up Branch Protection

This is a quick reference guide for setting up branch protection on your main branch.

## 🎯 5-Minute Setup

### 1. Enable Basic Protection (On GitHub.com)

1. Go to: `https://github.com/coreysreid/study-platform/settings/branches`
2. Click **Add rule**
3. Set **Branch name pattern** to: `main`
4. Check these boxes:
   - ✅ Require a pull request before merging
     - Set **Required approvals** to 1
   - ✅ Require status checks to pass before merging (if you have CI/CD set up)
   - ✅ Require conversation resolution before merging
5. Click **Create**

**Done!** Your main branch is now protected.

## 📋 What This Means

### ❌ You Cannot:
- Push directly to main (`git push origin main` will fail)
- Delete the main branch
- Force push to main

### ✅ You Must:
- Create a feature branch for changes
- Open a Pull Request to merge into main
- Get at least 1 approval before merging
- Resolve all review comments

## 🔄 New Workflow

### Before (Direct push):
```bash
git checkout main
git add .
git commit -m "changes"
git push origin main  # ❌ This will now fail
```

### After (Pull Request workflow):
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "Add my feature"

# Push feature branch
git push origin feature/my-feature

# Then on GitHub: Create Pull Request
# Wait for approval → Merge
```

## 🚀 Working with Feature Branches

### Creating a Feature Branch
```bash
# Start from main
git checkout main
git pull origin main

# Create new branch
git checkout -b feature/add-new-study-mode
```

### Making Changes
```bash
# Edit files, then:
git add .
git commit -m "Add new study mode feature"
git push origin feature/add-new-study-mode
```

### Creating a Pull Request
1. Go to GitHub.com
2. Click **Compare & pull request**
3. Fill out the PR template
4. Click **Create pull request**
5. Request review if needed
6. Wait for approval and status checks
7. Click **Merge pull request**
8. Delete the feature branch

### Cleaning Up
```bash
# After PR is merged, clean up locally
git checkout main
git pull origin main
git branch -d feature/add-new-study-mode
```

## 🔧 Files Included in This Repo

This repository includes several files to help with branch protection:

1. **`.github/CODEOWNERS`** - Automatically assigns reviewers
2. **`.github/workflows/ci.yml`** - Automated testing and linting
3. **`.github/PULL_REQUEST_TEMPLATE.md`** - PR checklist template
4. **`docs/BRANCH_PROTECTION.md`** - Comprehensive guide

## 🎓 Additional Status Checks (Optional)

If you enable the GitHub Actions workflow (`.github/workflows/ci.yml`), you can add these as required status checks:

1. Go to: `https://github.com/coreysreid/study-platform/settings/branches`
2. Edit your branch protection rule
3. Check: **Require status checks to pass before merging**
4. Search and add these status checks:
   - `Run Tests`
   - `Code Quality Checks`
   - `Security Checks`

Now PRs must pass all tests before merging! 🎉

## 📚 Learn More

- Full documentation: `docs/BRANCH_PROTECTION.md`
- GitHub's guide: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches

## ❓ Common Questions

**Q: Can I disable protection temporarily?**  
A: Yes, but not recommended. Repository admins can modify rules at any time.

**Q: What if I need to make an urgent hotfix?**  
A: Create a hotfix branch, make minimal changes, create PR, request expedited review.

**Q: Can I protect multiple branches?**  
A: Yes! Use patterns like `main` and `develop` or `release/*` for multiple branches.

**Q: Do these rules apply to me as the admin?**  
A: Only if you enable "Do not allow bypassing the above settings" (recommended).

---

**Need help?** See the full guide in `docs/BRANCH_PROTECTION.md`
