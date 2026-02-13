# Branch Protection Guide

This guide explains how to protect your main branch in the study-platform repository.

## Why Protect Your Main Branch?

Branch protection rules help you:
- Prevent accidental or unauthorized changes to critical branches
- Enforce code review requirements
- Ensure automated tests pass before merging
- Maintain code quality and stability
- Require specific approvals for sensitive changes

## Setting Up Branch Protection Rules

### Step 1: Access Branch Protection Settings

1. Navigate to your repository on GitHub: `https://github.com/coreysreid/study-platform`
2. Click on **Settings** (you need admin access)
3. In the left sidebar, click **Branches** under "Code and automation"
4. Under "Branch protection rules", click **Add rule** or **Add branch protection rule**

### Step 2: Configure Protection Rules

#### Basic Protection Settings

1. **Branch name pattern**: Enter `main` (or use `main*` for multiple branches)

2. **Protect matching branches** - Enable these recommended options:

   ✅ **Require a pull request before merging**
   - Require approvals: Set to at least 1 approval
   - Dismiss stale pull request approvals when new commits are pushed
   - Require review from Code Owners (if you set up CODEOWNERS file)

   ✅ **Require status checks to pass before merging**
   - Require branches to be up to date before merging
   - Status checks to require (add these if you have CI/CD):
     - `build` (if you have a build workflow)
     - `test` (if you have a test workflow)
     - `lint` (if you have a linting workflow)

   ✅ **Require conversation resolution before merging**
   - All review comments must be resolved

   ✅ **Require signed commits** (optional but recommended)
   - Ensures all commits are cryptographically signed

   ✅ **Require linear history** (optional)
   - Prevents merge commits, requires rebase or squash

   ✅ **Do not allow bypassing the above settings**
   - Applies rules to administrators too

   ✅ **Restrict who can push to matching branches**
   - Limit to specific people or teams
   - Consider allowing only CI/CD bots and release managers

#### Advanced Protection Settings

   ⚙️ **Require deployments to succeed before merging** (optional)
   - For production-grade projects

   ⚙️ **Lock branch** (use with caution)
   - Makes the branch read-only

   ⚙️ **Allow force pushes** (NOT recommended for main branch)
   - Keep this disabled

   ⚙️ **Allow deletions** (NOT recommended for main branch)
   - Keep this disabled

### Step 3: Save Protection Rules

Click **Create** or **Save changes** at the bottom of the page.

## Recommended Configuration for This Project

For the study-platform repository, we recommend:

```
Branch name pattern: main

✅ Require pull request before merging
   - Required approvals: 1
   - Dismiss stale approvals: Yes
   
✅ Require status checks before merging
   - Require branches to be up to date: Yes
   - Status checks: (any CI workflows you create)
   
✅ Require conversation resolution: Yes

✅ Do not allow bypassing settings: Yes

❌ Allow force pushes: No
❌ Allow deletions: No
```

## Working with Protected Branches

Once protection is enabled:

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and commit**:
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**:
   - Go to GitHub and create a PR from your feature branch to `main`
   - Request reviews from team members
   - Wait for required checks to pass

4. **Merge after approval**:
   - Once approved and checks pass, merge the PR
   - Delete the feature branch after merging

### Emergency Hotfixes

For urgent fixes:

1. Create a hotfix branch: `git checkout -b hotfix/critical-bug`
2. Make minimal necessary changes
3. Create PR with "HOTFIX" label
4. Request expedited review
5. Merge once approved

## Code Owners (Optional)

If you've set up a `CODEOWNERS` file (located at `.github/CODEOWNERS`), certain files will automatically require review from specific people.

Example CODEOWNERS file:
```
# Default owners for everything
* @coreysreid

# Django settings and security-critical files
study_platform/settings.py @coreysreid
*/migrations/* @coreysreid

# Documentation
docs/* @coreysreid
*.md @coreysreid
```

## Status Checks with GitHub Actions

To enforce automated checks, create GitHub Actions workflows in `.github/workflows/`:

Example: `.github/workflows/ci.yml`
```yaml
name: CI

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python manage.py test
      - name: Run linting
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

Once this workflow exists, add `test` as a required status check in your branch protection rules.

## Troubleshooting

### "Cannot push to protected branch"
- This is expected. Create a feature branch and submit a PR instead.

### "Status checks are failing"
- Review the CI/CD logs in the PR
- Fix issues in your feature branch
- Push new commits to update the PR

### "Need admin access"
- Only repository admins can configure branch protection
- Contact the repository owner if you need access

### "Want to bypass temporarily"
- Not recommended, but admins can temporarily disable rules if absolutely necessary
- Re-enable immediately after the emergency

## Best Practices

1. **Always work in feature branches** - Never commit directly to main
2. **Keep PRs small and focused** - Easier to review and less likely to break things
3. **Write descriptive commit messages** - Helps with code review and history
4. **Run tests locally first** - Don't rely solely on CI/CD
5. **Review your own PR** - Check the diff before requesting reviews
6. **Address review comments promptly** - Keep the process moving
7. **Keep main branch deployable** - Every merge should leave main in a working state

## Additional Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Code Owners Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Remember**: Branch protection is about preventing mistakes, not blocking progress. Set up rules that work for your team's workflow.
