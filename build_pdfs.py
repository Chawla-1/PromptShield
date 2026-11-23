import os, subprocess, markdown

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

@page {
    size: A4 portrait;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-center {
        content: counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: #718096;
    }
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
}

h1 {
    font-size: 19pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 6px;
    margin-top: 0;
    margin-bottom: 12px;
}

h2 {
    font-size: 14pt;
    font-weight: 600;
    color: #1e293b;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 10px;
    page-break-after: avoid;
}

h3 {
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}

p {
    margin-top: 0;
    margin-bottom: 8px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 9pt;
    page-break-inside: auto;
}

tr {
    page-break-inside: avoid;
    page-break-after: auto;
}

th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
    text-align: left;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
}

td {
    padding: 6px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

pre, code {
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
}

code {
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}

pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 10px 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 8px 0 12px 0;
    line-height: 1.4;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
    border: none;
    font-size: 8.5pt;
}

ul, ol {
    margin-top: 0;
    margin-bottom: 8px;
    padding-left: 20px;
}

li {
    margin-bottom: 4px;
}

.badge-pass {
    background-color: #dcfce7;
    color: #15803d;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8pt;
}

.badge-fail {
    background-color: #fee2e2;
    color: #b91c1c;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8pt;
}

.badge-work {
    background-color: #e0f2fe;
    color: #0369a1;
    font-weight: 600;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8pt;
}

.card {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #3b82f6;
    padding: 10px 14px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
}

.page-break {
    page-break-before: always;
}

.diagram-box {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 14px;
    margin: 14px 0;
    text-align: center;
}
"""

def md_to_pdf(md_file, pdf_file, title):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

    # Post-process badges
    html_content = html_content.replace('**Pass**', '<span class="badge-pass">PASS</span>')
    html_content = html_content.replace('**Fail**', '<span class="badge-fail">FAIL</span>')
    html_content = html_content.replace('**Working**', '<span class="badge-work">WORKING</span>')

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{CSS_STYLES}</style>
</head>
<body>
{html_content}
</body>
</html>"""

    temp_html = pdf_file.replace('.pdf', '_temp.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(full_html)

    abs_html = os.path.abspath(temp_html)
    abs_pdf = os.path.abspath(pdf_file)

    cmd = [EDGE_PATH, '--headless', f'--print-to-pdf={abs_pdf}', abs_html]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Generated {pdf_file} (Status: {res.returncode}, File exists: {os.path.exists(abs_pdf)})")

if __name__ == '__main__':
    os.makedirs('docs', exist_ok=True)
    md_to_pdf('docs/milestone_2_report_draft.md', 'docs/M2_PE-B-65-15_PromptShield.pdf', 'Milestone 2 Project Report - PE-B-65-15')
    md_to_pdf('docs/PromptShield_Technical_Report.md', 'docs/TheHiddenVariable_TechnicalReport.pdf', 'Technical Report - The Hidden Variable')
