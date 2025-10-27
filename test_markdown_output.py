"""Test script to check Document Intelligence markdown output."""

from dotenv import load_dotenv
load_dotenv()

from src.preprocessing import parse_document_to_markdown

markdown = parse_document_to_markdown('data/sample_cvs/Resume.pdf')

print('=== MARKDOWN OUTPUT (first 4000 chars) ===')
print(markdown[:4000])
print('\n...\n')
print(f'=== TOTAL LENGTH: {len(markdown)} chars ===')

# Save to file for inspection
with open('data/outputs/resume_markdown.md', 'w') as f:
    f.write(markdown)
print('\n✅ Saved full markdown to: data/outputs/resume_markdown.md')
