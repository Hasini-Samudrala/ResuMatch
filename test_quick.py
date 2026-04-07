import os
import sys
from dotenv import load_dotenv

from text_processor import clean_text, read_from_file, truncate_text, extract_word_count
from gemini_analyzer import initialize_gemini, analyze_resume_match, get_quick_tip
from report_generator import (
    display_results_in_terminal,
    format_analysis_report,
    save_report,
    save_to_history,
)
from datetime import datetime


def main():
    print("=" * 60)
    print("  ResuMatch — Automated Test Run (File Input)")
    print("=" * 60)

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "paste_your_gemini_api_key_here":
        print("No API key found in .env")
        sys.exit(1)
    print(f"API key loaded ({api_key[:8]}...)")

    print("\nReading resume from sample_resume.txt...")
    resume_raw = read_from_file("sample_resume.txt")
    resume = clean_text(resume_raw)
    print(f"Resume loaded: {extract_word_count(resume)} words")

    print("Reading job description from sample_jd.txt...")
    jd_raw = read_from_file("sample_jd.txt")
    jd = clean_text(jd_raw)
    print(f"Job description loaded: {extract_word_count(jd)} words")

    resume = truncate_text(resume, max_words=800)
    jd = truncate_text(jd, max_words=800)
    print("Truncation check passed")

    model = initialize_gemini(api_key)

    print("\nRunning resume analysis (this takes 10-15 seconds)...\n")
    analysis = analyze_resume_match(model, resume, jd)
    print(f"Analysis complete — Match Score: {analysis['match_score']}/100")

    quick_tip = get_quick_tip(model, analysis.get("missing_skills", []))
    print("Quick tip received")

    display_results_in_terminal(analysis, quick_tip)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resume_snippet = resume[:100].replace("\n", " ")
    job_snippet = jd[:100].replace("\n", " ")
    report = format_analysis_report(resume_snippet, job_snippet, analysis, timestamp)
    save_report(report, "test", "reports")
    save_to_history(analysis, timestamp, "history")

    print("\n" + "=" * 60)
    print("  ALL TESTS PASSED — ResuMatch is working!")
    print("=" * 60)


if __name__ == "__main__":
    main()
