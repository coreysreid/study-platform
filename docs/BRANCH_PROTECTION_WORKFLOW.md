# Branch Protection Workflow Visualization

This document provides a visual representation of the protected branch workflow.

## 🔄 Standard Development Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAIN BRANCH (Protected)                      │
│                    🔒 No direct pushes allowed                       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ git pull origin main
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   Your Local Main       │
                    │   (Always sync first!)  │
                    └─────────────────────────┘
                                  │
                                  │ git checkout -b feature/new-feature
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   Feature Branch        │
                    │   (Work happens here)   │
                    └─────────────────────────┘
                                  │
                                  │ Make changes
                                  │ git add .
                                  │ git commit -m "..."
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   Committed Changes     │
                    └─────────────────────────┘
                                  │
                                  │ git push origin feature/new-feature
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   GitHub Repository     │
                    │   (Feature branch)      │
                    └─────────────────────────┘
                                  │
                                  │ Create Pull Request
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         PULL REQUEST                                 │
│                                                                       │
│  📝 Description and checklist completed                              │
│  👥 Code owners automatically notified                               │
│  🤖 Automated checks running:                                        │
│      ├─ Django system checks                                         │
│      ├─ Migration checks                                             │
│      ├─ Tests                                                         │
│      ├─ Code quality (flake8)                                        │
│      └─ Security scans (bandit, safety)                              │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ┌──────────────────┐       ┌──────────────────┐
          │  ❌ Checks Failed │       │  ✅ Checks Passed │
          └──────────────────┘       └──────────────────┘
                    │                           │
                    │                           │
                    ▼                           ▼
          ┌──────────────────┐       ┌──────────────────┐
          │  Fix Issues      │       │  Code Review     │
          │  Push Updates    │       │  by Maintainer   │
          └──────────────────┘       └──────────────────┘
                    │                           │
                    │              ┌────────────┴────────────┐
                    │              │                         │
                    │              ▼                         ▼
                    │    ┌──────────────────┐   ┌─────────────────┐
                    │    │ Changes Requested │   │ ✅ Approved     │
                    │    └──────────────────┘   └─────────────────┘
                    │              │                         │
                    └──────────────┘                         │
                                                             │
                                                             ▼
                                              ┌──────────────────────┐
                                              │  Merge Pull Request  │
                                              └──────────────────────┘
                                                             │
                                                             ▼
                                              ┌──────────────────────┐
                                              │   MAIN BRANCH        │
                                              │   ✨ Updated!        │
                                              └──────────────────────┘
```

## 🎯 Key Decision Points

### 1. Before You Start
```
Question: Is main branch up to date?
├─ YES → Create feature branch
└─ NO  → git pull origin main first
```

### 2. Naming Your Branch
```
What are you doing?
├─ Adding new feature    → feature/descriptive-name
├─ Fixing a bug          → fix/bug-description
├─ Updating docs         → docs/what-you-updated
├─ Refactoring code      → refactor/what-you-refactored
└─ Adding tests          → test/what-you-tested
```

### 3. Ready to Push?
```
Checklist:
├─ [ ] Code follows project style?
├─ [ ] Tests pass locally?
├─ [ ] Changes are tested?
├─ [ ] Documentation updated?
└─ [ ] Commit messages are clear?
     └─ All YES? → Push and create PR
```

### 4. After Creating PR
```
What's the status?
├─ Checks failing?
│  └─ Fix issues → Push updates → Checks run again
│
├─ Review comments?
│  └─ Address feedback → Push updates → Request re-review
│
└─ Approved and passing?
   └─ Merge! → Delete feature branch → Pull main locally
```

## 📊 Automated Check Flow

```
Pull Request Created
        │
        ▼
┌───────────────────┐
│  CI/CD Pipeline   │
│  Starts Running   │
└───────────────────┘
        │
        ├─────────────────────────────┐
        │                             │
        ▼                             ▼
┌──────────────┐            ┌──────────────────┐
│  Test Job    │            │  Lint Job        │
│              │            │                  │
│  ├─ Checkout │            │  ├─ Checkout     │
│  ├─ Setup    │            │  ├─ Setup        │
│  ├─ Install  │            │  ├─ Install      │
│  ├─ Check    │            │  ├─ flake8       │
│  └─ Test     │            │  └─ Report       │
└──────────────┘            └──────────────────┘
        │                             │
        └─────────────┬───────────────┘
                      │
                      ▼
            ┌──────────────────┐
            │  Security Job    │
            │                  │
            │  ├─ Checkout     │
            │  ├─ Setup        │
            │  ├─ bandit       │
            │  └─ safety       │
            └──────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
    All Pass?                   Any Fail?
        │                           │
        ▼                           ▼
    ✅ Ready                    ❌ Fix Required
    for Review                  and Re-run
```

## 🚫 What Branch Protection Prevents

```
Attempt                          Result
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
git push origin main            ❌ BLOCKED
                                "Protected branch hook declined"

Force push                      ❌ BLOCKED
git push --force origin main    "Cannot force push to protected branch"

Delete branch                   ❌ BLOCKED
git push origin --delete main   "Cannot delete protected branch"

Merge without approval          ❌ BLOCKED (on GitHub)
                                "Requires 1 approving review"

Merge with failing checks       ❌ BLOCKED (on GitHub)
                                "Status checks must pass"

Merge with unresolved comments  ❌ BLOCKED (on GitHub)
                                "Conversations must be resolved"
```

## ✅ What You Can Do

```
Action                                      Result
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Create feature branch                      ✅ ALLOWED
git checkout -b feature/my-feature         Always allowed

Push to feature branch                     ✅ ALLOWED
git push origin feature/my-feature         Push your changes

Create Pull Request                        ✅ ALLOWED
(on GitHub)                                Open PR anytime

Request reviews                            ✅ ALLOWED
                                          Get feedback

Update your PR                             ✅ ALLOWED
Push new commits to feature branch         Automatic update

Merge after approval + passing checks      ✅ ALLOWED
(on GitHub, after requirements met)        Complete the process
```

## 🔄 Complete Example Scenario

```
Day 1: Start New Feature
────────────────────────
$ git checkout main
$ git pull origin main
$ git checkout -b feature/add-quiz-mode
$ # ... make changes ...
$ git add .
$ git commit -m "Add quiz mode feature"
$ git push origin feature/add-quiz-mode
→ Create PR on GitHub
→ Fill out PR template
→ CI checks start running

Day 2: Address Review
──────────────────────
→ Reviewer leaves comments
$ # ... fix issues ...
$ git add .
$ git commit -m "Address review comments"
$ git push origin feature/add-quiz-mode
→ CI checks run again
→ Request re-review

Day 3: Merge
────────────
→ Approved ✅
→ All checks passing ✅
→ Click "Merge Pull Request"
→ Delete feature branch on GitHub
$ git checkout main
$ git pull origin main
$ git branch -d feature/add-quiz-mode
✨ Feature is live!
```

## 📚 Additional Resources

- **Quick Start**: `.github/BRANCH_PROTECTION_QUICKSTART.md`
- **Full Guide**: `docs/BRANCH_PROTECTION.md`
- **Contributing**: `CONTRIBUTING.md`
- **GitHub Docs**: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches

---

Remember: Branch protection is about **preventing accidents**, not blocking progress! 🎯
