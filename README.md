# 304-SP26: Number Theory

Course webpage for Number Theory, Spring 2026  
Johns Hopkins University  
Instructor: Christian Klevdal

## About

This repository contains the course webpage for Math 304: Number Theory (Spring 2026). The course covers elementary number theory including prime numbers, divisibility, congruences, and applications to cryptography.

## Website URL

https://christian-klevdal.github.io/304-sp26/

## Course Pages

- **index.html** - Main course homepage with instructor info and quick links
- **syllabus.html** - Complete course syllabus with grading policies and learning outcomes
- **schedule.html** - Weekly schedule with topics, readings, and problem set due dates
- **lecture-notes.html** - Lecture notes (posted throughout semester)
- **problem-sets.html** - Problem set assignments (posted throughout semester)
- **sagemath.html** - SageMath resources and tutorials
  - **mini-sage-intro.html** - Introduction to SageMath with interactive examples
  - **for-loops.html** - Tutorial on using for loops in SageMath
  - **pythagorean-triples.html** - Exploring Pythagorean triples with SageMath
- **style.css** - Stylesheet for the website

## Lecture Note Workflow

Lecture notes are created using Jupyter notebooks with SageMath code cells, then converted to interactive HTML pages. The workflow is stored in the `lecture-notes/` folder:

1. **Create Content**: Write lecture notes in a Jupyter notebook (`.ipynb`) with:
   - Markdown cells for text, definitions, theorems (with LaTeX math support)
   - SageMath code cells for computational examples

2. **Review**: Open the notebook in SageMath to test code cells and verify mathematical content

3. **Convert to HTML**: Use the `convert_to_html.py` script to generate an interactive HTML page:
   ```bash
   cd lecture-notes
   python3 convert_to_html.py notebook-name.ipynb
   ```
   This creates an HTML file with:
   - MathJax for rendering LaTeX mathematics
   - Embedded SageCells that allow interactive code execution
   - Proper CSS styling

4. **Publish**: Add a link to the new HTML file in `lecture-notes.html`

See `lecture-notes/lecture-note-workflow.ipynb` for detailed formatting guidelines and instructions.

## Technologies Used

- HTML5/CSS3
- SageMath Cell Server for interactive computational examples
- GitHub Pages for hosting

## Course Information

- **Lecture:** Tuesday/Thursday 9:00-10:15 AM, Bloomberg 168
- **Discussion:** Friday 9:00-9:50 AM, Bloomberg 276
- **Textbook:** Silverman, *A Friendly Introduction to Number Theory* (4th Edition)

## Updating the Website

After making changes to any files:

```bash
git add .
git commit -m "Description of changes"
git push
```

The website will automatically update on GitHub Pages within 1-2 minutes.

## Last Updated

January 6, 2026
