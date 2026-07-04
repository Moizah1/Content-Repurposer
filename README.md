# Content Repurposer 🔁

Turn a single blog post into 3 platform-ready formats using the Anthropic API.

**Outputs:**
- 🐦 Twitter/X thread (numbered, under 280 chars per tweet)
- 💼 LinkedIn post (hook + insights + CTA)
- 📧 Email newsletter snippet (subject line + body + CTA)

**Tone options:** professional · casual · witty · inspirational

---

## Requirements
 
- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- The `anthropic` Python SDK


## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."   # Mac/Linux
set ANTHROPIC_API_KEY=sk-ant-...        # Windows
```

## Usage

### Interactive mode (paste content)
```bash
python repurposer.py
```

Paste your content, then press `Enter` twice followed by `Ctrl+D` (Mac/Linux) or `Ctrl+Z` (Windows) to submit. You'll then be asked to pick a tone.

### File mode
```bash
python repurposer.py my_article.txt
```

### Saving output
 
After generation, you'll be prompted to save the results. If you choose yes, three files are created:
 
```
output_twitter.txt
output_linkedin.txt
output_email.txt
```

### As a module in your own code
```python
from repurposer import repurpose

content = open("my_article.txt").read()
results = repurpose(content, tone="casual")

print(results["twitter"])
print(results["linkedin"])
print(results["email"])
```

---

## Key concepts this project teaches

| Concept | Where it appears |
|---|---|
| Anthropic SDK basics | `client.messages.create()` |
| System/user prompts | Each format has its own tailored prompt |
| Parallel API calls | `ThreadPoolExecutor` — 3x faster than sequential |
| Prompt engineering | Tone injection, output format instructions |
| Structured outputs | Each prompt instructs a specific format |

