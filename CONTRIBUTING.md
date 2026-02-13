# Contributing to Study Platform

Thank you for considering contributing to the Study Platform! This document provides guidelines for contributing to this project.

## 🔒 Branch Protection

This repository uses branch protection on the `main` branch to ensure code quality and stability.

### Quick Links
- **5-Minute Setup**: [.github/BRANCH_PROTECTION_QUICKSTART.md](.github/BRANCH_PROTECTION_QUICKSTART.md)
- **Full Guide**: [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md)

### What This Means
- ❌ No direct pushes to `main`
- ✅ All changes via Pull Requests
- ✅ Code review required
- ✅ Automated tests must pass

## 🚀 How to Contribute

### 1. Fork and Clone (External Contributors)

For external contributors:
```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/study-platform.git
cd study-platform
git remote add upstream https://github.com/coreysreid/study-platform.git
```

### 2. Create a Feature Branch

```bash
# Make sure you're on main and it's up to date
git checkout main
git pull origin main

# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features (e.g., `feature/add-quiz-mode`)
- `fix/` - Bug fixes (e.g., `fix/flashcard-flip-animation`)
- `docs/` - Documentation updates (e.g., `docs/update-readme`)
- `refactor/` - Code refactoring (e.g., `refactor/simplify-views`)
- `test/` - Test additions/updates (e.g., `test/add-model-tests`)

### 3. Make Your Changes

```bash
# Make your changes
# Edit files...

# Test your changes locally
python manage.py test
python manage.py check

# Commit your changes
git add .
git commit -m "Add descriptive commit message"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issues if applicable (e.g., "Fix #123: Resolve flashcard bug")

### 4. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name
```

Then on GitHub:
1. Click "Compare & pull request"
2. Fill out the PR template completely
3. Link any related issues
4. Request review from @coreysreid

### 5. Address Review Comments

- Respond to review comments promptly
- Make requested changes in new commits
- Push updates to the same branch
- Mark conversations as resolved when addressed

### 6. Merge

Once approved and all checks pass:
- Maintainer will merge your PR
- You can delete your feature branch

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows existing style and conventions
- [ ] All tests pass locally (`python manage.py test`)
- [ ] New features include tests
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] PR template is filled out completely
- [ ] No merge conflicts with main branch

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test study

# Run specific test
python manage.py test study.tests.TestFlashcard
```

### Writing Tests
- Add tests for new features
- Tests should be in `study/tests.py` or `study/tests/`
- Follow existing test patterns
- Test both success and failure cases

## 🎨 Code Style

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions/classes
- Keep functions focused and small

### Django Conventions
- Follow Django's best practices
- Use Django's built-in features when possible
- Keep views simple, move logic to models/utils
- Use Django's ORM properly

### Templates
- Use consistent indentation (2 spaces)
- Keep templates DRY (Don't Repeat Yourself)
- Use template inheritance appropriately
- Add comments for complex logic

## 🐛 Reporting Bugs

### Before Reporting
- Check if the issue already exists
- Try to reproduce the bug
- Gather relevant information

### Bug Report Should Include
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable
- Error messages/logs

## 💡 Suggesting Features

We welcome feature suggestions! Please:
- Check if the feature is already suggested
- Explain the use case clearly
- Describe the expected behavior
- Consider implementation complexity

## 📚 Documentation

Documentation improvements are always welcome:
- Fix typos and grammar
- Clarify confusing sections
- Add examples
- Update outdated information

Documentation files:
- `README.md` - Main project overview
- `docs/` - Detailed documentation
- Inline code comments
- Docstrings in Python code

## 🔐 Security

If you discover a security vulnerability:
- **DO NOT** open a public issue
- Email the maintainer directly
- Provide details about the vulnerability
- Allow time for a fix before public disclosure

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

## 💬 Communication

- Be respectful and constructive
- Ask questions if something is unclear
- Provide context in your messages
- Be patient with reviews

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## 🙏 Thank You!

Your contributions make this project better. Whether it's code, documentation, bug reports, or feature suggestions - every contribution is valuable!

---

**Questions?** Open an issue or contact @coreysreid
