# Exotel HR Policy Assistant

An AI-powered chatbot that helps Exotel employees understand company HR policies. Built on Anthropic's Claude API with a comprehensive knowledge base covering 21 HR policy documents.

## What It Does

Employees can ask natural-language questions about HR policies and get accurate, sourced answers with step-by-step calculations where applicable. The chatbot handles:

- Leave policies (annual, sick, casual, sabbatical, LWP, carry-forward rules)
- Salary advance eligibility and calculations
- Car lease and device lease rules (EMI caps, supplementary allowance)
- Variable pay / growth incentive calculations (OB slabs, GP interpolation)
- Travel and reimbursement limits (domestic + international)
- POSH (Prevention of Sexual Harassment) — extended workplace definition
- Separation and F&F settlement rules
- Background verification (BGV) by level
- Referral bonus eligibility
- Code of conduct and conflict of interest
- And more across 21 policy documents

## Features

- **Professional chat interface** with Exotel branding
- **Multi-turn conversation** — remembers context within a session
- **PDF export** — export full chat or individual responses as branded PDFs
- **Quick-action cards** — common questions accessible in one click
- **Markdown rendering** — tables, code blocks, and formatted responses
- **Mobile responsive** — works on desktop and mobile browsers

## Deployment Options

### Option 1: Replit (Recommended)

1. Create a new Replit project → Import from GitHub (or upload files)
2. Go to **Secrets** (lock icon) → Add `ANTHROPIC_API_KEY` with your Anthropic API key
3. Click **Run** — the app starts on port 8080
4. Share the Replit URL with your team

**Files used:** `app.py`, `templates/index.html`, `knowledge_base.md`, `requirements.txt`, `.replit`

### Option 2: Claude Platform (Projects)

For a no-code setup using Anthropic's Claude Projects:

1. Go to [claude.ai](https://claude.ai) → Create a new **Project**
2. Paste the contents of `claude-project-instructions.md` as **Custom Instructions**
3. Upload `knowledge_base.md` as a **Project Knowledge** file
4. Share the project with your team

### Option 3: Any Server (Docker / VM / Cloud)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
gunicorn --bind :8080 --workers 2 --threads 4 --timeout 120 app:app
```

## Project Structure

```
exotel-hr-chatbot/
├── app.py                          # Flask backend + Claude API integration
├── templates/
│   └── index.html                  # Professional chat UI with PDF export
├── knowledge_base.md               # Combined knowledge base (21 policies)
├── claude-project-instructions.md  # Custom instructions for Claude Projects
├── validate.py                     # 25-question automated test suite
├── requirements.txt                # Python dependencies
├── .replit                         # Replit configuration
└── .gitignore
```

## Configuration

| Environment Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | — | Your Anthropic API key |
| `MODEL_NAME` | No | `claude-sonnet-4-5-20250929` | Claude model to use |
| `PORT` | No | `8080` | Server port |

## Validation

Run the 25-question stress test to verify accuracy:

```bash
# Test against your deployed instance
python validate.py --url https://your-app.replit.app

# Or test directly via Claude API
export ANTHROPIC_API_KEY="your-key"
python validate.py --api
```

The test suite checks keyword presence, forbidden-word absence, and calculation accuracy across all 21 policy areas. Expected pass rate: 96%+.

## Knowledge Base

The `knowledge_base.md` file contains the combined, structured content from 21 Exotel HR policy documents:

1. Annual Leave Policy
2. Sick Leave Policy
3. Casual Leave Policy
4. Period Leave Policy
5. Bereavement Leave Policy
6. Marriage Leave Policy
7. Sabbatical Leave Policy
8. Compensatory Off Policy
9. Compulsory Paid Leave Vacation (CPLV)
10. Salary Advance Policy
11. Car Lease Policy
12. Device Lease Policy
13. Travel & Reimbursement Policy
14. Employee Referral Policy
15. Background Verification (BGV) Policy
16. Variable Pay / Growth Incentive Plan
17. Separation Policy
18. POSH (Prevention of Sexual Harassment)
19. Code of Conduct
20. Conflict of Interest Policy
21. Disciplinary Action Framework

## Tech Stack

- **Backend:** Python / Flask
- **AI:** Anthropic Claude API (claude-sonnet-4-5-20250929)
- **Frontend:** Vanilla HTML/CSS/JS
- **PDF Export:** html2pdf.js
- **Markdown:** marked.js
- **Production Server:** Gunicorn

## License

Internal use only — Exotel confidential.
