# 🚀 Reddit Automation CI/CD Setup

## GitHub Actions Integration

This project includes a complete GitHub Actions workflow for automated testing of the Reddit automation suite.

## 🔧 Setup Instructions

### 1. Repository Setup
```bash
# Push your code to GitHub
git init
git add .
git commit -m "Add Reddit automation test suite"
git remote add origin https://github.com/YOUR_USERNAME/reddit-automation.git
git push -u origin main
```

### 2. Configure Secrets
In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `REDDIT_USERNAME` | Your Reddit username | `your_reddit_username` |
| `REDDIT_PASSWORD` | Your Reddit password | `your_reddit_password` |

⚠️ **Security Note**: Never commit credentials to your repository. Always use GitHub Secrets.

### 3. Workflow Triggers

The GitHub Action runs automatically on:
- ✅ **Push to main/master branch**
- ✅ **Pull requests**
- ✅ **Manual trigger** (workflow_dispatch)
- ✅ **Daily schedule** (9 AM UTC)

## 🎯 Workflow Features

### **Optimized for CI/CD:**
- 🎭 **Headless browser** mode for CI efficiency
- 🚀 **Fast execution** (no video recording in CI)
- 📦 **Dependency caching** for faster builds
- 🐍 **Python 3.10** environment
- 🦊 **Firefox browser** with stealth configuration

### **Test Execution:**
- ✅ Automated Reddit login/logout
- ✅ Gaming subreddit navigation
- ✅ Smart post detection (excludes pinned/ads)
- ✅ Nintendo content analysis and voting
- ✅ BDD scenario validation

### **Error Handling:**
- 📊 **Test failure logs** uploaded as artifacts
- 🔍 **Detailed error reporting** in workflow logs
- ⚡ **Quick feedback** on test results

## 🏃‍♂️ Running Tests

### **Local Development:**
```bash
# Full test with video recording and reports
python test_runner.py

# CI-optimized test (headless, no video)
python ci_test_runner.py
```

### **GitHub Actions:**
- **Automatic**: Triggered by code changes
- **Manual**: Go to Actions tab → "Reddit Automation Test" → "Run workflow"

## 📋 Workflow File

The workflow is defined in `.github/workflows/reddit-automation.yml`:

```yaml
name: Reddit Automation Test
on: [push, pull_request, workflow_dispatch, schedule]
jobs:
  reddit-automation-test:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Python 3.10
      - Install dependencies
      - Install Playwright browsers
      - Run Reddit automation test
      - Handle results and artifacts
```

## 🎨 Status Badge

Add this to your repository README to show test status:

```markdown
[![Reddit Automation Test](https://github.com/YOUR_USERNAME/reddit-automation/workflows/Reddit%20Automation%20Test/badge.svg)](https://github.com/YOUR_USERNAME/reddit-automation/actions)
```

## 🔍 Monitoring

### **GitHub Actions Dashboard:**
- View test execution logs
- Download failure artifacts
- Monitor test history and trends
- Track success/failure rates

### **Notifications:**
- ✅ Success: Green checkmark on commits
- ❌ Failure: Red X with detailed logs
- 📧 Email notifications (configurable)

## ⚡ Performance Optimizations

### **CI Mode Features:**
- **Headless execution**: No GUI overhead
- **Reduced slow-mo**: Faster test execution
- **No video recording**: Saves CI resources
- **Dependency caching**: Faster builds
- **Optimized logging**: Cleaner CI output

### **Typical Execution Time:**
- **Local (with video)**: ~60 seconds
- **CI (headless)**: ~30-45 seconds

## 🛠️ Troubleshooting

### **Common Issues:**

1. **Credentials Error:**
   ```
   Solution: Check GitHub Secrets are properly set
   ```

2. **Browser Installation:**
   ```
   Solution: Workflow includes playwright install steps
   ```

3. **Test Timeout:**
   ```
   Solution: Reddit rate limiting - retry after delay
   ```

## 🎯 Next Steps

- **Parallel testing**: Add matrix strategy for multiple browsers
- **Slack notifications**: Integrate with team communication
- **Test reporting**: Add Allure reports to GitHub Pages
- **Performance monitoring**: Track execution time trends

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Playwright CI Guide](https://playwright.dev/docs/ci)
- [pytest Documentation](https://docs.pytest.org/)

---

**Ready to impress your interviewer with professional CI/CD integration!** 🌟