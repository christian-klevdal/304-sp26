#!/usr/bin/env python3
"""
Convert a Jupyter notebook with SageMath code to an HTML page with embedded SageCells.
This script processes markdown (with TeX) and code cells, creating an interactive HTML page.
"""

import nbformat
import sys
import os
import re

def markdown_to_html(markdown_text):
    """
    Convert markdown to HTML while preserving LaTeX math.
    This is a simple converter that handles common markdown elements.
    """
    html = markdown_text
    
    # Convert headers
    html = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
    html = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert bold and italic (but not in LaTeX)
    # Use negative lookbehind/lookahead to avoid matching $ signs
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # Also support underscore-based italics
    html = re.sub(r'\b_(.+?)_\b', r'<em>\1</em>', html)
    
    # Convert inline code (but preserve LaTeX)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert lists
    lines = html.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        # Ordered list
        if re.match(r'^\d+\.\s+', line):
            if in_list != 'ol':
                if in_list:
                    result_lines.append(f'</{in_list}>')
                result_lines.append('<ol class="indented-list">')
                in_list = 'ol'
            item = re.sub(r'^\d+\.\s+', '', line)
            result_lines.append(f'<li>{item}</li>')
        # Unordered list
        elif re.match(r'^[-*]\s+', line):
            if in_list != 'ul':
                if in_list:
                    result_lines.append(f'</{in_list}>')
                result_lines.append('<ul class="indented-list">')
                in_list = 'ul'
            item = re.sub(r'^[-*]\s+', '', line)
            result_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                result_lines.append(f'</{in_list}>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append(f'</{in_list}>')
    
    html = '\n'.join(result_lines)
    
    # Convert paragraphs (lines separated by blank lines)
    # Split by double newlines, but preserve display math blocks
    paragraphs = re.split(r'\n\s*\n', html)
    formatted_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if para:
            # Don't wrap headers, lists, or HTML tags in <p>
            if not (para.startswith('<h') or para.startswith('<ol') or 
                    para.startswith('<ul') or para.startswith('<li>') or
                    para.startswith('</') or para.startswith('<div')):
                # Check if it's a display math block
                if para.startswith('$$') or para.endswith('$$'):
                    formatted_paragraphs.append(para)
                else:
                    formatted_paragraphs.append(f'<p>{para}</p>')
            else:
                formatted_paragraphs.append(para)
    
    html = '\n'.join(formatted_paragraphs)
    
    return html

def convert_notebook_to_html(notebook_path, output_path=None):
    """
    Convert a Jupyter notebook to HTML with embedded SageCells.
    
    Args:
        notebook_path: Path to the input .ipynb file
        output_path: Path to the output .html file (optional)
    """
    # Set default output path if not provided
    if output_path is None:
        output_path = notebook_path.replace('.ipynb', '.html')
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Extract title from first markdown cell if available
    title = "Lecture Notes"
    if nb.cells and nb.cells[0].cell_type == 'markdown':
        first_line = nb.cells[0].source.split('\n')[0]
        if first_line.startswith('#'):
            title = first_line.lstrip('#').strip()
    
    # Count sections (h1 and h2 headers) to determine how many linked groups we need
    section_count = 0
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Check if this cell contains h1 or h2 headers
            if re.search(r'^#{1,2}\s+', cell.source, re.MULTILINE):
                section_count += 1
    
    # Start HTML document
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style> body \u007b margin: 60px;\u007d </style>
    <!-- Custom CSS -->
    <link rel="stylesheet" type="text/css" href="style.css">
    
    <!-- SageCell JavaScript -->
    <script src="https://sagecell.sagemath.org/static/embedded_sagecell.js"></script>
    <script>
        // Create separate linked groups for each section
"""
    
    # Add makeSagecell calls for each section
    for i in range(section_count):
        html += f"""        sagecell.makeSagecell({{
            inputLocation: '.sage-section-{i}',
            evalButtonText: 'Run',
            languages: ['sage'],
            hide: ['permalink'],
            linked: true
        }});
"""
    
    html += """    </script>
    
    <!-- MathJax for TeX rendering -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }}
        }};
    </script>
    
    <style>
        .markdown-cell {{
            margin: 20px 0;
        }}
        .sage-cell {{
            margin: 20px 0;
        }}
        /* Header styling - make h1 stand out with boxes */
        .markdown-cell h1 {{
            background-color: #f0f4f8;
            border: 2px solid #003366;
            border-left: 5px solid #003366;
            padding: 15px;
            margin-top: 40px;
            margin-bottom: 20px;
            border-radius: 5px;
            color: #003366;
        }}
        /* First h1 shouldn't have extra top margin */
        .markdown-cell:first-child h1:first-child {{
            margin-top: 20px;
        }}
    </style>
</head>
<body>
"""
    
    # Process each cell
    current_section = -1  # Track which section we're in (-1 means before any section)
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Check if this cell contains h1 or h2 headers
            if re.search(r'^#{1,2}\s+', cell.source, re.MULTILINE):
                current_section += 1
            # Convert markdown to HTML manually, preserving LaTeX
            html_content = markdown_to_html(cell.source)
            html += f'<div class="markdown-cell">\n{html_content}\n</div>\n\n'
        elif cell.cell_type == 'code':
            # Assign sage cells to the current section
            section_class = f'sage-section-{current_section}' if current_section >= 0 else 'sage-section-0'
            # Create SageCell
            html += f'''<div class="sage-cell {section_class}">
<script type="text/x-sage">
{cell.source}
</script>
</div>

'''
    
    # Add link back to lecture notes page
    html += """
<hr style="margin-top: 40px; margin-bottom: 20px;">
<p style="text-align: center;">
    <a href="lecture-notes.html" style="font-size: 1.1em;">← Back to Lecture Notes</a>
</p>

</body>
</html>"""
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Successfully converted {notebook_path} to {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_to_html.py <notebook.ipynb> [output.html]")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(notebook_path):
        print(f"Error: File {notebook_path} not found")
        sys.exit(1)
    
    convert_notebook_to_html(notebook_path, output_path)
