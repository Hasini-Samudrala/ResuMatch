import os
import sys
import csv
from datetime import datetime

from dotenv import load_dotenv

from text_processor import clean_text, read_from_file, truncate_text, extract_word_count
from gemini_analyzer import initialize_gemini, analyze_resume_match, get_quick_tip
from report_generator import (
    format_analysis_report,
    save_report,
    save_to_history,
    display_results_in_terminal,
)


def print_welcome_banner():
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    print()
    print("=" * 60)
    print()
    print("         RESUMATCH — Resume vs JD Matcher")
    print()
    print("   Analyze how well your resume matches a job description")
    print("   using Google Gemini AI. Get scores, skill analysis,")
    print("   and actionable improvement suggestions.")
    print()
    print(f"   {now}")
    print()
    print("=" * 60)
    print()


def load_api_key():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key.strip() == "" or api_key == "paste_your_gemini_api_key_here":
        print("ERROR: Gemini API key not found!")
        print()
        print("To fix this:")
        print("  1. Go to https://aistudio.google.com/app/apikey")
        print("  2. Sign in with your Google account")
        print("  3. Click 'Create API Key' and copy it")
        print("  4. Open the .env file in this project folder")
        print("  5. Replace 'paste_your_gemini_api_key_here' with your actual key")
        print()
        print("The Gemini API is FREE — no credit card required!")
        sys.exit(1)

    return api_key.strip()


def show_history_summary():
    csv_path = os.path.join("history", "history_log.csv")

    if not os.path.exists(csv_path):
        print("This is your first analysis — let's get started!")
        print()
        return

    try:
        with open(csv_path, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)

        if not rows:
            print("This is your first analysis — let's get started!")
            print()
            return

        scores = []
        for row in rows:
            try:
                scores.append(int(row["match_score"]))
            except (ValueError, KeyError):
                pass

        total_analyses = len(rows)
        best_score = max(scores) if scores else 0

        print(f"You have run {total_analyses} previous analysis(es).")
        print(f"   Your best score so far: {best_score}/100")
        print()

    except (IOError, csv.Error) as error:
        print(f"Could not read history: {error}")
        print()


def collect_input(step_number, total_steps, label):
    print(f"\nSTEP {step_number} of {total_steps}: Provide your {label} file.")
    print(f"   Supported formats: .txt, .md")

    file_path = input(f"   Enter the path to your {label} file: ").strip()

    try:
        raw_text = read_from_file(file_path)
        print(f"   File loaded: {file_path}")
    except FileNotFoundError as error:
        print(f"\n{error}")
        print(f"   Please make sure the file exists and try again.")
        sys.exit(1)
    except ValueError as error:
        print(f"\n{error}")
        sys.exit(1)

    cleaned = clean_text(raw_text)

    word_count = extract_word_count(cleaned)
    print(f"\n{label.capitalize()} received: {word_count} words.")

    if word_count < 50:
        print(f"\nWarning: Your {label} seems very short ({word_count} words).")
        user_choice = input("   Do you want to continue anyway? (yes/no): ").strip().lower()
        if user_choice not in ("yes", "y"):
            print(f"   Please provide a longer {label} file and try again.")
            sys.exit(0)

    return cleaned


def main():
    print_welcome_banner()

    api_key = load_api_key()

    try:
        model = initialize_gemini(api_key)
    except Exception:
        print("\nCould not connect to Gemini. Please check your API key and internet.")
        sys.exit(1)

    while True:
        show_history_summary()

        resume_text = collect_input(step_number=1, total_steps=2, label="resume")

        job_description_text = collect_input(step_number=2, total_steps=2, label="job description")

        resume_truncated = truncate_text(resume_text, max_words=800)
        jd_truncated = truncate_text(job_description_text, max_words=800)

        if resume_truncated != resume_text:
            print("Note: Resume was truncated to 800 words to fit within API limits.")
        if jd_truncated != job_description_text:
            print("Note: Job description was truncated to 800 words to fit within API limits.")

        print("\nAnalyzing your resume against the job description...")
        print("   This may take 10-15 seconds...\n")

        try:
            analysis = analyze_resume_match(model, resume_truncated, jd_truncated)
        except Exception as error:
            print(f"\nAnalysis failed: {error}")
            print("   Please try again. If this keeps happening, check your API key.")
            continue

        missing_skills = analysis.get("missing_skills", [])
        quick_tip = get_quick_tip(model, missing_skills)

        display_results_in_terminal(analysis, quick_tip)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        resume_snippet = resume_text[:100].replace("\n", " ")
        job_snippet = job_description_text[:100].replace("\n", " ")

        report = format_analysis_report(resume_snippet, job_snippet, analysis, timestamp)

        save_report(report, topic_hint="analysis", reports_folder="reports")

        save_to_history(analysis, timestamp, history_folder="history")

        print("\n" + "-" * 60)
        run_again = input("Would you like to analyze another resume? (yes/no): ").strip().lower()

        if run_again not in ("yes", "y"):
            print()
            print("=" * 60)
            print("  Thank you for using ResuMatch!")
            print("  Your reports are saved in the 'reports/' folder.")
            print("  Your history is tracked in 'history/history_log.csv'.")
            print("  Good luck with your job applications!")
            print("=" * 60)
            print()
            break

        print("\n" + "=" * 60)
        print("  Starting a new analysis...\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting ResuMatch. Goodbye!")
        sys.exit(0)
