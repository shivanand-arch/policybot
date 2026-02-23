"""
Exotel HR Chatbot — Validation Test Script
============================================
Runs 25 stress-test questions to verify the chatbot gives accurate answers.
Run this AFTER deployment to validate accuracy.

Usage:
    # Test against deployed Replit service:
    python validate.py --url https://your-app.replit.app

    # Test directly via Anthropic Claude API:
    export ANTHROPIC_API_KEY="your-key"
    python validate.py --api
"""

import os
import sys
import json
import time
import argparse

# ---------------------------------------------------------------------------
# The 25 validated Q&A pairs from the Claude stress test
# Each has: question, expected_keywords (must appear), expected_NOT (must NOT appear),
# and a human-readable expected_answer summary
# ---------------------------------------------------------------------------
TEST_CASES = [
    {
        "id": 1,
        "question": "List the policies that are covered here.",
        "expected_keywords": ["leave policy", "car lease", "device lease", "posh", "separation", "travel", "referral", "code of conduct"],
        "expected_not": [],
        "expected_summary": "Should list all 21 policies"
    },
    {
        "id": 2,
        "question": "I have exhausted all my leaves, I still need more. What can I do?",
        "expected_keywords": ["lwp", "leave without pay"],
        "expected_not": [],
        "expected_summary": "Should mention LWP, salary advance, sabbatical options"
    },
    {
        "id": 3,
        "question": "What is the maximum amount of monthly EMIs I can avail to get a mobile phone on lease? My supplementary allowance is 10000Rs.",
        "expected_keywords": ["7,000", "7000", "70%"],
        "expected_not": [],
        "expected_summary": "Should calculate 70% of 10000 = 7000"
    },
    {
        "id": 4,
        "question": "Can I take car lease and device lease together?",
        "expected_keywords": ["yes", "70%", "supplementary"],
        "expected_not": [],
        "expected_summary": "Yes, but shared 70% cap on supplementary allowance"
    },
    {
        "id": 5,
        "question": "My band is L2, what is applicable for me?",
        "expected_keywords": ["leave", "device lease"],
        "expected_not": [],
        "expected_summary": "All policies except car lease (L3+). Should mention L2 eligibility."
    },
    {
        "id": 6,
        "question": "I am having a balance of 35 annual leaves today, can I avail them in coming April?",
        "expected_keywords": ["30", "carry forward", "lapse"],
        "expected_not": [],
        "expected_summary": "Only 30 carry forward, 5 lapse in March"
    },
    {
        "id": 7,
        "question": "I am serving only 20 days notice period, how will it affect my F&F?",
        "expected_keywords": ["shortfall", "recover"],
        "expected_not": [],
        "expected_summary": "Shortfall days recovered from F&F, salary hold rules"
    },
    {
        "id": 8,
        "question": "I have recently joined Exotel at E1 level, what are the BGV checks applicable for me?",
        "expected_keywords": ["credit check", "employment", "education", "address"],
        "expected_not": [],
        "expected_summary": "All checks including credit check for E1 (L5+)"
    },
    {
        "id": 9,
        "question": "I am having an issue with my landlord, how can I bypass the address verification?",
        "expected_keywords": ["mandatory", "cannot"],
        "expected_not": [],
        "expected_summary": "Cannot bypass, address verification is mandatory"
    },
    {
        "id": 10,
        "question": "I am the head of HR, can I refer someone to the company and claim a referral?",
        "expected_keywords": ["refer", "not eligible", "hr function"],
        "expected_not": [],
        "expected_summary": "Can refer but not eligible for bonus (HR function excluded)"
    },
    {
        "id": 11,
        "question": "What will happen if I take an advance and resign a week later?",
        "expected_keywords": ["recover", "f&f", "full"],
        "expected_not": [],
        "expected_summary": "Full amount recovered from F&F + no salary during notice"
    },
    {
        "id": 12,
        "question": "My fixed CTC is 3 lakh per annum and variable is 2 lakh, what is the max salary advance that I can take?",
        "expected_keywords": ["50,000", "50000"],
        "expected_not": [],
        "expected_summary": "50,000 (2 months of fixed gross only, variable excluded)"
    },
    {
        "id": 13,
        "question": "I am the cofounder and I went out for dinner with a client and billed 50000, what can I do?",
        "expected_keywords": ["exception", "limit"],
        "expected_not": [],
        "expected_summary": "Exceeds limit (8k for Director+), needs exception approval"
    },
    {
        "id": 14,
        "question": "I want to upgrade my seat in the flight during travel, can I get this reimbursed?",
        "expected_keywords": ["economy", "no"],
        "expected_not": [],
        "expected_summary": "No, economy only. BU head exception possible."
    },
    {
        "id": 15,
        "question": "I am a sales manager and I went out for dinner with a client in Kathmandu and the bill was 50000, what can I do?",
        "expected_keywords": ["international", "$110"],
        "expected_not": [],
        "expected_summary": "International entertainment limit applies ($110/week max)"
    },
    {
        "id": 16,
        "question": "After the office hours, we went on a vacation during the weekend and there was improper advances made on me by a colleague. Can I report it?",
        "expected_keywords": ["yes", "posh", "workplace", "report"],
        "expected_not": ["no", "cannot report"],
        "expected_summary": "Yes, reportable under POSH (extended workplace definition)"
    },
    {
        "id": 17,
        "question": "Can home be considered as workplace?",
        "expected_keywords": ["yes", "physical or otherwise"],
        "expected_not": [],
        "expected_summary": "Yes, 'physical or otherwise' definition covers home"
    },
    {
        "id": 18,
        "question": "I was running a restaurant before joining exotel, should I keep anything in mind?",
        "expected_keywords": ["conflict of interest", "disclose", "disclosure"],
        "expected_not": [],
        "expected_summary": "Must disclose under Conflict of Interest policy"
    },
    {
        "id": 19,
        "question": "I make reels and am a social media influencer during weekends, is it okay?",
        "expected_keywords": ["ok", "yes", "conflict"],
        "expected_not": [],
        "expected_summary": "OK with caveats (no objectionable content, no conflict)"
    },
    {
        "id": 20,
        "question": "I am in need of money, can I avail my CPLV now?",
        "expected_keywords": ["annual", "not", "salary advance"],
        "expected_not": [],
        "expected_summary": "No, CPLV is annual only. Suggest salary advance."
    },
    {
        "id": 21,
        "question": "My university has shut down and I have not received my degree certificate, what can I do?",
        "expected_keywords": ["not covered", "hr"],
        "expected_not": [],
        "expected_summary": "Not covered in current policies, suggest contacting HR"
    },
    {
        "id": 22,
        "question": "So I can make money on the side? If there is no conflict of interest?",
        "expected_keywords": ["disclosure", "conflict"],
        "expected_not": [],
        "expected_summary": "Policy silent on moonlighting, but must disclose and avoid conflicts"
    },
    {
        "id": 23,
        "question": "What are the OB attainment slabs for sales incentives?",
        "expected_keywords": ["120%", "100%", "85%", "70%"],
        "expected_not": [],
        "expected_summary": "Should list the stepped slab table"
    },
    {
        "id": 24,
        "question": "If my OB attainment is 60%, what payout percentage do I get?",
        "expected_keywords": ["60%"],
        "expected_not": ["40%"],
        "expected_summary": "60% payout (Less Than 70% slab). Must NOT say 40%."
    },
    {
        "id": 25,
        "question": "I am a sales manager with annual variable of 1.2L. Q3: GP went from 15 to 19 against target 25, OB achieved 15 against 25 (60%), collections 90%. What is my Q3 variable payout?",
        "expected_keywords": ["11,988", "11988", "49.95"],
        "expected_not": [],
        "expected_summary": "Should compute ~INR 11,988 (OB 60% slab, GP interpolation, 90% collection multiplier)"
    },
]


def test_with_claude_api(api_key, model_name):
    """Test directly against Claude API."""
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)

    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.md")
    with open(kb_path, "r", encoding="utf-8") as f:
        kb_content = f.read()

    # Build system prompt same way app.py does
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        app_source = f.read()

    idx_start = app_source.find('SYSTEM_PROMPT = """')
    idx_end = app_source.find('""" + kb_content')
    raw_prompt = app_source[idx_start + len('SYSTEM_PROMPT = """'):idx_end]
    system_prompt = raw_prompt + kb_content

    return {"client": client, "model": model_name, "system_prompt": system_prompt}, "api"


def test_with_url(base_url):
    """Test against deployed Replit service."""
    import requests
    return base_url.rstrip("/"), "url"


def run_tests(target, mode):
    """Run all test cases and report results."""
    results = []
    passed = 0
    partial = 0
    failed = 0

    print(f"\n{'='*70}")
    print(f"  EXOTEL HR CHATBOT VALIDATION — {len(TEST_CASES)} Questions")
    print(f"{'='*70}\n")

    for tc in TEST_CASES:
        qnum = tc["id"]
        question = tc["question"]
        print(f"  [{qnum:2d}/25] {question[:65]}...")

        try:
            if mode == "api":
                resp = target["client"].messages.create(
                    model=target["model"],
                    max_tokens=2048,
                    temperature=0.2,
                    system=target["system_prompt"],
                    messages=[{"role": "user", "content": question}],
                )
                answer = resp.content[0].text.lower()
            else:
                import requests
                r = requests.post(
                    f"{target}/chat",
                    json={"message": question, "history": []},
                    timeout=60,
                )
                answer = r.json().get("response", "").lower()

            # Check expected keywords
            found = [kw for kw in tc["expected_keywords"] if kw.lower() in answer]
            missing = [kw for kw in tc["expected_keywords"] if kw.lower() not in answer]

            # Check forbidden keywords
            forbidden_found = [kw for kw in tc["expected_not"] if kw.lower() in answer]

            if forbidden_found:
                status = "FAIL"
                failed += 1
                reason = f"Contains forbidden: {forbidden_found}"
            elif len(missing) == 0:
                status = "PASS"
                passed += 1
                reason = ""
            elif len(found) >= len(tc["expected_keywords"]) / 2:
                status = "PARTIAL"
                partial += 1
                reason = f"Missing: {missing}"
            else:
                status = "FAIL"
                failed += 1
                reason = f"Missing: {missing}"

            icon = {"PASS": "✅", "PARTIAL": "⚠️", "FAIL": "❌"}[status]
            print(f"         {icon} {status} {reason}")

            results.append({
                "id": qnum,
                "question": question,
                "status": status,
                "expected": tc["expected_summary"],
                "missing_keywords": missing,
                "forbidden_found": forbidden_found,
                "answer_preview": answer[:200],
            })

            time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"         ❌ ERROR: {e}")
            failed += 1
            results.append({
                "id": qnum, "question": question, "status": "ERROR",
                "error": str(e)
            })

    # Summary
    print(f"\n{'='*70}")
    print(f"  RESULTS SUMMARY")
    print(f"{'='*70}")
    print(f"  ✅ PASS:    {passed:2d} / {len(TEST_CASES)}")
    print(f"  ⚠️  PARTIAL: {partial:2d} / {len(TEST_CASES)}")
    print(f"  ❌ FAIL:    {failed:2d} / {len(TEST_CASES)}")
    print(f"  Score:      {passed}/{len(TEST_CASES)} ({100*passed//len(TEST_CASES)}%)")
    print(f"{'='*70}\n")

    # Save results
    out_path = os.path.join(os.path.dirname(__file__), "validation_results.json")
    with open(out_path, "w") as f:
        json.dump({"summary": {"pass": passed, "partial": partial, "fail": failed},
                    "results": results}, f, indent=2)
    print(f"  Results saved to: {out_path}\n")

    return passed, partial, failed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Exotel HR Chatbot")
    parser.add_argument("--url", help="Deployed Replit service URL (tests via HTTP)")
    parser.add_argument("--api", action="store_true",
                        help="Test directly via Anthropic Claude API")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250929",
                        help="Claude model name (default: claude-sonnet-4-5-20250929)")
    args = parser.parse_args()

    if args.url:
        target, mode = test_with_url(args.url)
    elif args.api:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            print("ERROR: Set ANTHROPIC_API_KEY environment variable")
            sys.exit(1)
        target, mode = test_with_claude_api(api_key, args.model)
    else:
        print("ERROR: Provide --url (deployed service) or --api (direct Claude API)")
        print("  Example: python validate.py --api")
        print("  Example: python validate.py --url https://your-app.replit.app")
        sys.exit(1)

    run_tests(target, mode)
