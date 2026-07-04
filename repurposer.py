
import anthropic 
import concurrent.futures
import sys

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

TONE_OPTIONS = ["professional", "casual", "witty", "inspirational"]

PROMPTS = {
    "twitter": """You are a social media expert. Convert the following blog post into an engaging Twitter/X thread with {tone} tone.
Format it as numbered tweets (1/, 2/, 3/...). Each tweet must be under 280 characters.
Use hooks, line breaks within tweets for readability, and end with a strong CTA.
Output ONLY the thread, no intro text.

BLOG POST:
{content}""",

    "linkedin": """You are a LinkedIn content strategist. Convert the following blog post into a {tone} LinkedIn post.
Structure: strong opening hook (1-2 lines), 3-5 key insights with line breaks, a relatable story or example, CTA at the end.
Use short paragraphs. No hashtag overload (max 3). Around 200-300 words.
Output ONLY the LinkedIn post, no intro text.

BLOG POST:
{content}""",

    "email": """You are an email newsletter writer. Convert the following blog post into a {tone} email newsletter section.
Include: a catchy subject line (prefixed with "Subject: "), a warm opening sentence, the key value in 2-3 short paragraphs, and a CTA button text.
Keep it concise and scannable. Around 150-200 words.
Output ONLY the email content, no intro text.

BLOG POST:
{content}""",
}


def repurpose_single(format_name: str, content: str, tone: str) -> tuple[str, str]:
    """Call the API for a single output format. Returns (format_name, result_text)."""
    prompt = PROMPTS[format_name].format(tone=tone, content=content)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return format_name, message.content[0].text


def repurpose(content: str, tone: str = "professional") -> dict[str, str]:
    """
    Repurpose a blog post into 3 formats in parallel.

    Args:
        content: The blog post text.
        tone:    One of 'professional', 'casual', 'witty', 'inspirational'.

    Returns:
        Dict with keys 'twitter', 'linkedin', 'email'.
    """
    if tone not in TONE_OPTIONS:
        raise ValueError(f"Tone must be one of: {TONE_OPTIONS}")

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(repurpose_single, fmt, content, tone): fmt
            for fmt in PROMPTS
        }
        for future in concurrent.futures.as_completed(futures):
            fmt_name, text = future.result()
            results[fmt_name] = text

    return results


def print_results(results: dict[str, str]) -> None:
    """Pretty-print the repurposed outputs."""
    divider = "\n" + "─" * 60 + "\n"
    labels = {
        "twitter": "🐦  TWITTER / X THREAD",
        "linkedin": "💼  LINKEDIN POST",
        "email": "📧  EMAIL NEWSLETTER",
    }
    for fmt in ["twitter", "linkedin", "email"]:
        print(divider)
        print(labels[fmt])
        print(divider)
        print(results[fmt])
    print("\n" + "─" * 60)


def save_results(results: dict[str, str], base_filename: str = "output") -> None:
    """Save each format to a separate .txt file."""
    for fmt, text in results.items():
        filename = f"{base_filename}_{fmt}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  Saved: {filename}")


# ─── CLI entry point ────────────────────────────────────────────────────────

def main():
    print("\n🔁  Content Repurposer")
    print("─" * 40)

    # Get input
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"Loaded: {filepath} ({len(content)} chars)")
    else:
        print("Paste your blog post below. Press Enter twice then Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) when done:\n")
        lines = []
        try:
            for line in sys.stdin:
                lines.append(line)
        except EOFError:
            pass
        content = "".join(lines).strip()

    if not content:
        print("No content provided. Exiting.")
        sys.exit(1)

    # Choose tone
    print("\nChoose tone:")
    for i, t in enumerate(TONE_OPTIONS, 1):
        print(f"  {i}. {t}")
    choice = input("Enter number (default 1 = professional): ").strip()
    tone = TONE_OPTIONS[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= 4 else "professional"

    print(f"\n⏳  Repurposing with '{tone}' tone (calling API in parallel)...")
    results = repurpose(content, tone)

    print_results(results)

    # Optionally save
    save = input("\nSave to files? (y/n): ").strip().lower()
    if save == "y":
        save_results(results)

    print("\n✅  Done!\n")


if __name__ == "__main__":
    main()
