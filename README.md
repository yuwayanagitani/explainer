# AI Card Explainer

AI Card Explainer automatically generates concise, high-quality explanations for flashcards using large language models (OpenAI or Google Gemini). It is designed especially for medical, nursing, and life-science students who want clean, exam-oriented explanations without unnecessary verbosity.

## Features
- Generate concise explanations for card content using AI.
- Supports OpenAI and Google Gemini (or other configured providers).
- Options to keep explanations short (exam-style) or more detailed.
- Insert generated explanations into a target field or show them on demand.

## Requirements
- Anki 2.1+
- API key for the chosen AI provider (unless using local fallback)

## Installation
1. Clone or download the add-on.
2. Copy it into the add-ons folder (Tools → Add-ons → Open Add-ons Folder).
3. Restart Anki.

## Usage
- Select notes in the Browser and run “Generate Explanations”.
- Choose the target field where explanations should be stored (e.g., “Explanation”).
- Configure tone/length options before generation.

## Configuration
Example settings:
- Provider: openai / gemini
- Target field name: Explanation
- Tone: concise / detailed
- Max tokens / length limit

Example config snippet:
```json
{
  "provider": "openai",
  "target_field": "Explanation",
  "tone": "concise"
}
```

## Privacy & Best Practices
- Review generated text before applying to important decks — AI output can occasionally be incorrect.
- Do not send PHI or highly-sensitive data to cloud providers unless permitted by policy.

## Troubleshooting
- If generation fails, verify API key and network access.
- If results are verbose or off-topic, adjust prompt settings or tone.

## Development
- Contributions and issue reports are welcome — include sample note structure when filing a bug.

## License
MIT License — see LICENSE file.

## Contact
Author: yuwayanagitani
