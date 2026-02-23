"""
Exotel HR Policy Assistant — Streamlit Edition
================================================
Uses Anthropic Claude API to answer employee HR policy questions.
Same model, same knowledge base, same accuracy as tested.

Deploy on Streamlit Community Cloud for free.
Set ANTHROPIC_API_KEY in Streamlit Secrets.
"""

import os
import streamlit as st
from anthropic import Anthropic

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Exotel HR Policy Hub",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Premium CSS — clean, minimal, enterprise-grade
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ── Fonts & Reset ───────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #F8F9FC;
    }

    /* ── Hide Streamlit chrome ───────────────── */
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 900px; }
    div[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }

    /* ── Top Header Bar ──────────────────────── */
    .top-bar {
        background: #FFFFFF;
        border-bottom: 1px solid #E8EAF0;
        padding: 16px 32px;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .top-bar-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .top-bar-logo {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #5B4FD6, #7C6FE8);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 20px;
        box-shadow: 0 2px 8px rgba(91,79,214,0.2);
    }
    .top-bar-text h1 {
        font-size: 18px; font-weight: 700; color: #1A1D2B;
        margin: 0; letter-spacing: -0.3px;
    }
    .top-bar-text p {
        font-size: 12px; color: #8B8FA3; margin: 2px 0 0;
        font-weight: 400;
    }
    .top-bar-badge {
        background: #ECFDF5; color: #059669;
        font-size: 11px; font-weight: 600;
        padding: 4px 12px; border-radius: 20px;
        letter-spacing: 0.3px;
    }

    /* ── Hero Section ────────────────────────── */
    .hero {
        text-align: center;
        padding: 48px 24px 32px;
    }
    .hero-icon {
        width: 80px; height: 80px;
        background: linear-gradient(135deg, #EDE9FE, #C4B5FD);
        border-radius: 24px;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px;
        margin: 0 auto 20px;
        box-shadow: 0 4px 20px rgba(91,79,214,0.15);
    }
    .hero h2 {
        font-size: 26px; font-weight: 800; color: #1A1D2B;
        margin-bottom: 8px; letter-spacing: -0.5px;
    }
    .hero p {
        font-size: 15px; color: #6B7084;
        max-width: 500px; margin: 0 auto 8px;
        line-height: 1.6;
    }
    .hero-sub {
        font-size: 12px; color: #A0A3B5;
        margin-top: 4px;
    }

    /* ── Category Cards ──────────────────────── */
    .cat-section {
        margin: 8px 0 32px;
    }
    .cat-section-title {
        font-size: 11px; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1.2px; color: #8B8FA3;
        margin-bottom: 14px; padding-left: 4px;
    }
    .cat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }
    .cat-card {
        background: #FFFFFF;
        border: 1px solid #E8EAF0;
        border-radius: 14px;
        padding: 18px 16px;
        cursor: pointer;
        transition: all 0.25s ease;
        text-align: center;
    }
    .cat-card:hover {
        border-color: #5B4FD6;
        box-shadow: 0 4px 16px rgba(91,79,214,0.12);
        transform: translateY(-2px);
    }
    .cat-card .cat-icon {
        font-size: 28px;
        display: block;
        margin-bottom: 10px;
    }
    .cat-card .cat-label {
        font-size: 13px; font-weight: 600; color: #1A1D2B;
        margin-bottom: 3px;
    }
    .cat-card .cat-desc {
        font-size: 11px; color: #8B8FA3;
        line-height: 1.4;
    }

    /* ── Stats Bar ───────────────────────────── */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 32px;
        padding: 16px 0 8px;
        margin-bottom: 24px;
    }
    .stat-item {
        text-align: center;
    }
    .stat-num {
        font-size: 22px; font-weight: 800; color: #5B4FD6;
    }
    .stat-label {
        font-size: 11px; color: #8B8FA3; font-weight: 500;
        margin-top: 2px;
    }

    /* ── Chat Messages ───────────────────────── */
    div[data-testid="stChatMessage"] {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        line-height: 1.75;
        border-radius: 14px;
        border: 1px solid #E8EAF0;
        margin-bottom: 4px;
    }

    /* ── Markdown Tables ─────────────────────── */
    div[data-testid="stChatMessage"] table {
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 13px;
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    div[data-testid="stChatMessage"] th,
    div[data-testid="stChatMessage"] td {
        border: 1px solid #E8EAF0;
        padding: 10px 14px;
        text-align: left;
    }
    div[data-testid="stChatMessage"] th {
        background: linear-gradient(135deg, #EDE9FE, #E8E5FF);
        font-weight: 600;
        color: #5B4FD6;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    div[data-testid="stChatMessage"] tr:nth-child(even) { background: #FAFAFF; }
    div[data-testid="stChatMessage"] tr:hover { background: #F0EEFF; }

    /* ── Chat Input Styling ──────────────────── */
    div[data-testid="stChatInput"] {
        border-top: 1px solid #E8EAF0;
        padding-top: 8px;
    }
    div[data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        border-radius: 14px !important;
        border: 2px solid #E8EAF0 !important;
        background: #FFFFFF !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #5B4FD6 !important;
        box-shadow: 0 0 0 3px rgba(91,79,214,0.1) !important;
    }

    /* ── Streamlit Buttons ───────────────────── */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 12px;
        padding: 10px 16px;
        font-size: 13px;
        border: 1.5px solid #E8EAF0;
        background: #FFFFFF;
        color: #1A1D2B;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: #5B4FD6;
        color: #5B4FD6;
        background: #F5F3FF;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(91,79,214,0.1);
    }

    /* ── Sidebar Styling ─────────────────────── */
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E8EAF0;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: #5B4FD6;
        color: white;
        border: none;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #4A3FC5;
        color: white;
    }

    /* ── Divider ─────────────────────────────── */
    .clean-divider {
        height: 1px;
        background: #E8EAF0;
        margin: 24px 0;
        border: none;
    }

    /* ── Responsive ──────────────────────────── */
    @media (max-width: 640px) {
        .cat-grid { grid-template-columns: repeat(2, 1fr); }
        .top-bar { padding: 12px 16px; }
        .hero { padding: 32px 16px 24px; }
        .stats-bar { gap: 20px; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header Bar
# ---------------------------------------------------------------------------
st.markdown("""
<div class="top-bar">
    <div class="top-bar-left">
        <div class="top-bar-logo">📚</div>
        <div class="top-bar-text">
            <h1>Exotel HR Policy Hub</h1>
            <p>Your AI-powered HR policy assistant</p>
        </div>
    </div>
    <div class="top-bar-badge">● Online</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
MODEL_NAME = os.environ.get("MODEL_NAME", "claude-haiku-4-5-20251001")

if not ANTHROPIC_API_KEY:
    st.error("ANTHROPIC_API_KEY not set. Add it in Streamlit Secrets (Settings → Secrets).")
    st.stop()

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# ---------------------------------------------------------------------------
# Load Knowledge Base & build system prompt
# ---------------------------------------------------------------------------
@st.cache_data
def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.md")
    with open(kb_path, "r", encoding="utf-8") as f:
        return f.read()

kb_content = load_knowledge_base()

SYSTEM_PROMPT = """You are **Exotel's HR Policy Assistant** — a friendly, accurate chatbot that helps Exotel employees understand company HR policies.

## CORE RULES
1. Answer ONLY using the KNOWLEDGE BASE section below. Never fabricate or assume policy details.
2. If something is not covered, say: "This isn't covered in our current policies. Please reach out to the HR team at hr@exotel.com for guidance."
3. Show step-by-step working for ANY calculations (variable pay, EMI, salary advance, etc.).
4. When multiple policies are relevant, reference ALL of them.
5. Be friendly, clear, and concise. Avoid legal jargon unless directly quoting policy.
6. For sensitive topics (POSH, separation, disciplinary), be empathetic and factual.
7. Never give legal advice — direct employees to HR or Legal for interpretations.
8. Always answer in the context of Exotel's specific policies.
9. If the employee hasn't provided enough info (band, level, tenure), ASK before answering.

## HANDLING VAGUE / INCOMPLETE QUESTIONS
- "leaves" without type → ask: annual, sick, casual, period, bereavement, marriage, sabbatical?
- Eligibility without band → ask for their level/band (L1-L5, E1, E2, etc.)
- "need money" → consider: salary advance (2x monthly fixed gross), CPLV (annual only), variable pay
- "Can I do X on the side?" → route to Conflict of Interest in Code of Conduct
- Weekend/after-hours colleague incidents → POSH extended workplace definition applies
- "What happens if I resign/leave..." → Separation policy
- "Can I claim..." → Travel & Reimbursement policy
- BGV questions → ask for level (checks vary by level)

## CRITICAL CALCULATION RULES (MUST FOLLOW EXACTLY)

### OB Attainment Slabs — STEPPED, NOT LINEAR
The OB slabs work as BANDS. You pick the band the employee falls into:
| Attainment Range | Payout % |
|---|---|
| >= 120% | 150% |
| >= 100% and < 120% | 120% |
| >= 85% and < 100% | 100% |
| >= 70% and < 85% | 80% |
| < 70% (but >= threshold) | 60% |
| Below minimum threshold | 40% or as specified |

EXAMPLE: 60% OB attainment → falls in "Less Than 70%" band → payout is 60%. NOT 40%.
EXAMPLE: 85% OB attainment → falls in ">=85% and <100%" band → payout is 100%.
NEVER interpolate between OB slabs. Pick the matching band.

### GP Growth Slabs — LINEAR INTERPOLATION BETWEEN BENCHMARKS
GP Growth uses linear interpolation between the defined benchmarks.
EXAMPLE: If 50% benchmark pays 40% and 75% benchmark pays 80%, then 60% growth = 40% + ((60%-50%)/(75%-50%)) × (80%-40%) = 56%

### Other Calculation Rules
- Car lease + Device lease SHARE the 70% supplementary allowance cap
- Salary advance max = 2 × monthly FIXED gross only (variable component excluded)
- Leave carry forward max = 30 days; excess lapses in March
- Notice period shortfall is recovered from F&F settlement
- Device Lease EMI = 70% of supplementary allowance for the chosen tenure

## COMMON SLANG / INFORMAL TERMS
- "comp off" = Compensatory Off
- "WFH" = Work From Home (not covered — say so)
- "F&F" = Full and Final Settlement
- "PF" / "EPF" = Provident Fund (not covered — say so)
- "variable" = Variable Pay / Growth Incentive
- "notice period" = Separation notice period
- "POSH" = Prevention of Sexual Harassment
- "LWP" = Leave Without Pay
- "CPLV" = Compulsory Paid Leave Vacation
- "BGV" = Background Verification
- "OB" = Order Booking
- "GP" = Gross Profit
- "CTC" = Cost to Company
- "EMI" = Equated Monthly Installment

## REFERENCE ANSWERS (Follow these patterns exactly)

Q: "I have exhausted all my leaves, what can I do?"
A: You have a few options: (1) Apply for Leave Without Pay (LWP) — salary deducted for days taken, (2) Check if you're eligible for a salary advance — up to 2x your monthly fixed gross, (3) If you've been with Exotel 3+ years, you may qualify for sabbatical leave. Which option would you like to explore?

Q: "My supplementary allowance is 10000, what's the max device lease EMI?"
A: Your maximum device lease EMI would be ₹7,000 (70% of ₹10,000 supplementary allowance). Note: if you also have a car lease, both share this 70% cap.

Q: "Can I take car lease and device lease together?"
A: Yes, you can avail both simultaneously. However, the combined EMI for both cannot exceed 70% of your supplementary allowance.

Q: "I am at L2, what's applicable for me?"
A: At L2 band, you're eligible for: all leave types, salary advance, device lease, referral bonus, CPLV, travel reimbursement (per L2 limits), and all standard benefits. Car lease requires L3 and above, so that's not available at L2.

Q: "I have 35 annual leaves, can I use them in April?"
A: Only 30 days can carry forward to the next financial year. The remaining 5 will lapse in March. I'd recommend using those 5 days before March 31st.

Q: "I'm the Head of HR, can I refer someone and claim referral bonus?"
A: You can absolutely refer candidates. However, employees in the HR function are not eligible for the referral bonus payout, regardless of level.

Q: "After office hours, improper advances by colleague on weekend vacation — can I report under POSH?"
A: Yes, absolutely. The POSH policy defines workplace as extending to any place visited arising out of or during employment. The definition covers spaces "physical or otherwise," including off-site locations. File a complaint with the Internal Committee.

Q: "Can home be considered workplace under POSH?"
A: Yes. The policy defines workplace as "physical or otherwise," covering work-from-home setups.

Q: "I was running a restaurant before joining, anything to keep in mind?"
A: Yes — under the Conflict of Interest policy, you must disclose any outside business interests at joining. Non-disclosure can be grounds for termination.

Q: "Can I avail CPLV now?"
A: CPLV is an annual payout — not available on demand. If you need funds urgently, consider a salary advance instead (up to 2x monthly fixed gross).

## TOPICS NOT COVERED IN CURRENT POLICIES
When asked about these, clearly state they're not in current policies:
Work from Home (WFH), ESOP/stock options, Provident Fund (PF/EPF), Gratuity details, Promotion criteria, Performance review process, Health insurance specifics, Gym/wellness benefits, Parking policy, Shift allowances, Overtime policy, Transfer policy, Deputation rules

---

## KNOWLEDGE BASE

""" + kb_content

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Welcome Screen (shown when no messages)
# ---------------------------------------------------------------------------
if not st.session_state.messages:
    # Hero section
    st.markdown("""
    <div class="hero">
        <div class="hero-icon">🤖</div>
        <h2>How can I help you today?</h2>
        <p>Ask me anything about Exotel's HR policies. I have instant answers on leaves, compensation, travel, POSH, separation, and more.</p>
        <div class="hero-sub">Covers all 21 Exotel HR policy documents</div>
    </div>
    """, unsafe_allow_html=True)

    # Quick action buttons

    # Quick action buttons
    quick_questions = [
        ("📅", "Leave Policies", "Types, balance & carry-forward", "What leave types are available and how many days for each?"),
        ("📱", "Device Lease", "EMI limits & eligibility", "How does the device lease work? What are the EMI limits?"),
        ("✈️", "Travel & Claims", "Reimbursement rules", "What is the travel reimbursement policy for domestic and international?"),
        ("💰", "Variable Pay", "OB slabs & GP calculation", "How is the quarterly variable pay calculated for sales roles?"),
        ("🤝", "Referral Bonus", "Amounts by level", "What are the referral bonus amounts by level?"),
        ("📋", "All Policies", "Complete coverage list", "List all 21 policies covered in the knowledge base"),
    ]

    cols = st.columns(3)
    for i, (icon, label, desc, question) in enumerate(quick_questions):
        with cols[i % 3]:
            if st.button(f"{icon}  {label}", key=f"quick_{i}", use_container_width=True, help=desc):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Display chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Ask about any HR policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Looking up policies..."):
            try:
                api_messages = []
                for msg in st.session_state.messages:
                    role = msg["role"] if msg["role"] == "user" else "assistant"
                    api_messages.append({"role": role, "content": msg["content"]})

                response = client.messages.create(
                    model=MODEL_NAME,
                    max_tokens=2048,
                    temperature=0.2,
                    system=SYSTEM_PROMPT,
                    messages=api_messages,
                )
                response_text = response.content[0].text
            except Exception as e:
                response_text = f"Sorry, something went wrong. Please try again. (Error: {str(e)[:100]})"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Options")

    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Exotel HR Policy Hub**")
    st.caption("21 policies covered")
    st.caption("For internal use only")
