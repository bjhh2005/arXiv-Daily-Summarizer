# arXiv Daily Paper ​​Summarizer

Automatically fetch the latest papers from arXiv, deliver their original abstracts by email, and optionally add Chinese translations powered by DeepSeek AI.

[中文文档](./README_CN.md) | English

## ✨ Features

- 📚 **Smart Paper Selection**: Fetches latest papers from cs.AI, cs.CV, and cs.CL categories
- 🎯 **Category Balance**: Ensures representation from each research area
- 🏆 **Quality Filtering**: Scores papers based on multiple quality indicators
- 🔄 **Intelligent Deduplication**: Detects and removes similar papers automatically
- 📋 **Original Abstracts**: Always includes the complete abstract supplied by arXiv
- 🌐 **Optional Chinese Translation**: Adds a faithful translation when DeepSeek is configured; failures never block email delivery
- 📧 **Email Delivery**: Beautiful HTML email format with date notices and quality badges
- ⏰ **Automated Scheduling**: Runs automatically via GitHub Actions
- 🆓 **Completely Free**: All services within free tier limits

## 🚀 Quick Start

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/RunRiotComeOn/arXiv-Daily-Summarizer.git
cd arxiv-daily-summarizer
```

### 2. Configure GitHub Secrets

Navigate to your GitHub repository: **Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DEEPSEEK_API_KEY` | Official DeepSeek API key (optional, for Chinese translation only) | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `SENDER_EMAIL` | Sender email address | `your-email@gmail.com` |
| `SENDER_PASSWORD` | Email app-specific password | `abcd efgh ijkl mnop` |
| `RECEIVER_EMAIL` | Recipient email address | `receiver@example.com` |
| `SMTP_SERVER` | SMTP server address (optional) | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (optional) | `587` |

#### API Configuration

This project calls the official DeepSeek API directly, using `https://api.deepseek.com` and the `deepseek-chat` model by default. Create an API key on the [DeepSeek Platform](https://platform.deepseek.com/api_keys) and store it as the GitHub Actions secret `DEEPSEEK_API_KEY`. Do not use a ModelScope token.

Without this key, emails are still delivered with the original arXiv abstracts only. When the key is configured, the app attempts to add Chinese translations. The associated DeepSeek account must have available credit.

#### 📮 Email Configuration Guide

**Gmail Users:**
1. Go to [Google Account Security Settings](https://myaccount.google.com/security)
2. Enable "2-Step Verification"
3. Generate an "App Password"
4. Select "Mail" and "Other device"
5. Use the generated 16-character password as `SENDER_PASSWORD`

**QQ Mail Users:**
1. Log in to QQ Mail → Settings → Account
2. Find "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service"
3. Enable "IMAP/SMTP Service"
4. Get authorization code as `SENDER_PASSWORD`
5. Set `SMTP_SERVER` to `smtp.qq.com`

**163 Mail Users:**
1. Log in to 163 Mail → Settings → POP3/SMTP/IMAP
2. Enable "IMAP/SMTP Service"
3. Get authorization code
4. Set `SMTP_SERVER` to `smtp.163.com`

### 3. Enable GitHub Actions

1. Go to the repository's **Actions** tab
2. Click "I understand my workflows, go ahead and enable them"
3. For first-time testing, click "Run workflow" to trigger manually

### 4. Wait for Daily Digest

The system runs automatically at 8:00 AM Beijing Time daily (configurable in `.github/workflows/daily_arxiv.yml`).

## 🛠️ Customization

### Modify Research Areas

Edit the `CATEGORIES` variable in `fetch_papers.py`:

```python
CATEGORIES = ['cs.AI', 'cs.CV', 'cs.CL']  # Add other categories as needed
```

Common arXiv categories:
- `cs.AI` - Artificial Intelligence
- `cs.CV` - Computer Vision
- `cs.CL` - Computation and Language (NLP)
- `cs.LG` - Machine Learning
- `cs.RO` - Robotics
- `cs.NE` - Neural and Evolutionary Computing

### Modify Number of Papers

Edit the `MAX_RESULTS` variable in `fetch_papers.py`:

```python
MAX_RESULTS = 5  # Number of papers to send daily
```

### Modify Category Balance

Edit the `MIN_PAPERS_PER_CATEGORY` variable:

```python
MIN_PAPERS_PER_CATEGORY = 1  # Minimum papers per category
```

### Modify Delivery Time

Edit the cron expression in `.github/workflows/daily_arxiv.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC time, add 8 hours for Beijing Time
```

Time reference:
- `'0 0 * * *'` - 08:00 Beijing Time
- `'0 1 * * *'` - 09:00 Beijing Time
- `'0 12 * * *'` - 20:00 Beijing Time

### Adjust Quality Filtering

Modify thresholds in `fetch_papers.py`:

```python
MIN_ABSTRACT_LENGTH = 100  # Minimum abstract length
SIMILARITY_THRESHOLD = 0.85  # Duplicate detection threshold (0-1)
```

## 📁 Project Structure

```
arxiv-daily-summarizer/
├── .github/
│   └── workflows/
│       └── daily_arxiv.yml    # GitHub Actions workflow config
├── fetch_papers.py            # Main script with quality filtering
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── README.md                 # English documentation
└── README_CN.md              # Chinese documentation
```

## 🔧 Local Testing

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (Windows PowerShell)
# Optional; omit it to send original arXiv abstracts only
$env:DEEPSEEK_API_KEY="your-api-key"
$env:SENDER_EMAIL="your-email@gmail.com"
$env:SENDER_PASSWORD="your-password"
$env:RECEIVER_EMAIL="receiver@example.com"

# Or use .env file (Unix/Linux/Mac)
cp .env.example .env
# Edit .env with your credentials
export $(cat .env | xargs)

# 3. Run the script
python fetch_papers.py
```

## 📊 Quality Scoring System

Papers are scored based on multiple factors:

1. **Abstract Length**: Longer abstracts indicate more detailed work (+0-2 points)
2. **Author Count**: Collaborative work gets bonus (+0-1 points)
3. **Title Keywords**: Important terms like "novel", "efficient", "transformer" (+0.5 points each)
4. **Recency**: Newer papers receive higher scores (+0.5-3 points)
5. **Title Quality**: Appropriate length and structure

High-quality papers (score ≥ 5.0) receive a ⭐ badge in the email.

## 🔍 Smart Deduplication

The system detects similar papers by:
- Calculating title similarity using sequence matching
- Removing duplicates with >85% similarity
- Keeping the higher-quality version when duplicates are found

## ⚖️ Category Balance Algorithm

1. **Guaranteed Minimum**: Each category gets at least 1 paper
2. **Quality Filling**: Remaining slots filled with highest-scoring papers across all categories
3. **Final Sort**: Papers sorted by publication date (newest first)

## 📊 Usage Limits

- **GitHub Actions**: 2000 minutes/month free (this project uses ~2-3 minutes/day)
- **DeepSeek API**: Billed according to current DeepSeek Platform pricing and account credit
- **Email**: Depends on your email provider's limits

## ❓ FAQ

**Q: Why didn't I receive the email?**
- Check GitHub Actions logs for errors
- Verify all Secrets are configured correctly
- Check your spam folder
- Confirm SMTP settings for your email provider

**Q: How do I modify the email design?**
- Edit the `generate_email_content()` function in `fetch_papers.py`
- Modify HTML and CSS code as needed

**Q: Can I send to WeChat or Telegram instead?**
- Yes! Replace the `send_email()` function with the appropriate API calls

**Q: Why are some papers several days old?**
- arXiv releases papers on a schedule, not continuously
- The system shows a date notice when papers are older
- Adjust `MIN_PAPERS_PER_CATEGORY` if you want stricter recency

**Q: How can I increase paper quality?**
- Increase `MIN_ABSTRACT_LENGTH` threshold
- Add more quality keywords in `calculate_paper_quality_score()`
- Increase the quality score threshold for filtering

## 📝 License

MIT License

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) - Open access to scholarly articles
- [DeepSeek](https://www.deepseek.com/) - Powerful AI models
- [GitHub Actions](https://github.com/features/actions) - Free automation service

---

⭐ If this project helps you, please consider giving it a star!

## 🔄 Updates & Changelog

### v2.0 - Enhanced Quality & Intelligence
- ✅ Added quality scoring system
- ✅ Implemented intelligent deduplication
- ✅ Ensured category balance
- ✅ Added high-quality paper badges
- ✅ Improved date notices
- ✅ Full English documentation

### v1.0 - Initial Release
- Basic paper fetching and original-abstract delivery
- Email delivery functionality
- GitHub Actions automation
