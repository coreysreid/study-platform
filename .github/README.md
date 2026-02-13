# GitHub Configuration Files

This directory contains GitHub-specific configuration files for the study-platform repository.

## 📁 Files in This Directory

### 🚀 Quick Start
**[BRANCH_PROTECTION_QUICKSTART.md](BRANCH_PROTECTION_QUICKSTART.md)**
- 5-minute guide to enable branch protection
- Essential steps to get started
- Common workflow examples
- **START HERE** if this is your first time setting up branch protection

### 👥 Code Ownership
**[CODEOWNERS](CODEOWNERS)**
- Automatically assigns reviewers for specific files
- Ensures critical files get proper review
- Configured for Django project structure
- Edit this file to add/change code owners

### 📝 Pull Request Template
**[PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md)**
- Standardized format for all pull requests
- Comprehensive checklist for contributors
- Security and testing considerations
- Automatically appears when creating PRs

### 🤖 CI/CD Workflows
**[workflows/ci.yml](workflows/ci.yml)**
- Automated testing on pull requests
- Code quality checks (flake8)
- Security scanning (bandit, safety)
- Django-specific system checks
- Runs automatically on all PRs to main

## 📚 Additional Documentation

For more detailed information, see:

- **Complete Guide**: [../docs/BRANCH_PROTECTION.md](../docs/BRANCH_PROTECTION.md)
- **Visual Workflow**: [../docs/BRANCH_PROTECTION_WORKFLOW.md](../docs/BRANCH_PROTECTION_WORKFLOW.md)
- **Setup Summary**: [../docs/BRANCH_PROTECTION_SETUP_SUMMARY.md](../docs/BRANCH_PROTECTION_SETUP_SUMMARY.md)
- **Contributing**: [../CONTRIBUTING.md](../CONTRIBUTING.md)

## 🔄 How These Files Work Together

```
Pull Request Created
        ↓
   (PULL_REQUEST_TEMPLATE.md provides checklist)
        ↓
   (CODEOWNERS assigns reviewers)
        ↓
   (workflows/ci.yml runs automated checks)
        ↓
   Branch Protection rules enforce:
   - Required approvals
   - Passing checks
   - Resolved conversations
        ↓
   Merge to main ✅
```

## 🛠️ Customization

### Adding a Code Owner
Edit `CODEOWNERS`:
```
# Make @username review all Python files
*.py @username
```

### Modifying CI Checks
Edit `workflows/ci.yml`:
- Add new jobs
- Change Python version
- Add more security tools
- Adjust test commands

### Updating PR Template
Edit `PULL_REQUEST_TEMPLATE.md`:
- Add project-specific sections
- Modify checklist items
- Add custom fields

## 🔐 Security

All files in this directory follow security best practices:
- ✅ Minimal GitHub Actions permissions
- ✅ Security scanning enabled
- ✅ Code review required for changes
- ✅ Automated vulnerability checks

## 📖 Learn More

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CODEOWNERS Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

---

**Questions?** See the [Quick Start Guide](BRANCH_PROTECTION_QUICKSTART.md) or open an issue!
