# PDF Resume Generator

This repository includes scripts to automatically generate professional PDF resumes from your CV data in `_data/cv.yml`.

## Features

### 🎨 Two Beautiful Styles

- **Basic Resume**: Clean, minimal design with essential information
- **Enhanced Resume**: Premium design with:
  - Professional color scheme (deep blue theme)
  - Enhanced typography and spacing
  - Icons and visual elements
  - Structured publication grouping (conferences vs preprints)
  - Rich text formatting with bold names and italic titles

### 📋 Comprehensive Sections

- Personal information with contact details
- Education history with advisor and research areas
- Publications (automatically grouped by type and sorted by year)
- Research experience with project descriptions
- Awards and honors
- Academic service

### 🔧 Technical Features

- Automatic HTML tag removal from YAML content
- Smart text formatting and justification
- Professional page layout with proper margins
- Consistent styling throughout the document
- Generation timestamp in footer

## Quick Start

### Option 1: Simple Script

```bash
# Generate both versions
./make_resume.sh

# Generate only enhanced version
./make_resume.sh enhanced

# Generate only basic version
./make_resume.sh basic
```

### Option 2: Direct Python

```bash
# Enhanced version (recommended)
python3 generate_resume_enhanced.py

# Basic version
python3 generate_resume.py
```

## Requirements

The generator automatically installs required packages, but you can install them manually:

```bash
pip install reportlab PyYAML
```

## Generated Files

- `Wei_Fu_Resume_Enhanced.pdf` - Premium version with advanced styling
- `Wei_Fu_Resume_Basic.pdf` - Clean minimal version
- `Wei_Fu_Resume.pdf` - Alias for basic version

## Customization

### Modifying Styles

Edit the style definitions in `generate_resume_enhanced.py`:

```python
# Color palette
primary_color = colors.HexColor('#1f4e79')      # Deep blue
secondary_color = colors.HexColor('#2980b9')    # Medium blue
accent_color = colors.HexColor('#3498db')       # Light blue
```

### Adding Sections

The generator reads from `_data/cv.yml`. Add new sections to the YAML file and implement corresponding methods in the Python scripts.

### Layout Adjustments

Modify page margins, fonts, and spacing in the `__init__` method:

```python
self.doc = SimpleDocTemplate(
    output_file,
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    # ... other settings
)
```

## CV Data Format

Your `_data/cv.yml` should follow this structure:

```yaml
name: Your Name
email: your.email@domain.com
location: Your Location
github: yourgithub

education:
  - degree: "Ph.D. in Computer Science"
    institution: "Your University"
    location: "City, Country"
    dates: "2021 - 2025"
    advisor: "Advisor Name"

publications:
  - title: "Your Paper Title"
    authors: "Author List with <strong>Your Name</strong>"
    venue: "Conference Name"
    year: 2024
    type: conference # or preprint
    note: "Special recognition"

experience:
  - position: "Research Intern"
    company: "Company Name"
    dates: "2024.1 - 2024.6"
    description: "Your work description..."

awards:
  - name: "Award Name"
    year: 2024

service:
  - role: "Reviewer"
    venues: "Conference Names"
    years: "2022-2024"
```

## Tips

1. **HTML in YAML**: Use `<strong>Your Name</strong>` to highlight your name in publications
2. **Project Links**: Include HTML links in experience descriptions - they'll be converted to plain text for PDF
3. **Publication Types**: Use `type: conference` for published papers, `type: preprint` for arXiv papers
4. **Regeneration**: Run the generator whenever you update your CV data

## File Organization

```
├── _data/cv.yml                          # Your CV data
├── generate_resume.py                    # Basic resume generator
├── generate_resume_enhanced.py           # Enhanced resume generator
├── make_resume.sh                        # Convenient script
├── RESUME_GENERATOR.md                   # This documentation
└── Wei_Fu_Resume*.pdf                    # Generated PDFs
```

## Troubleshooting

**Missing packages**: The script automatically installs required packages
**PDF not generated**: Check that `_data/cv.yml` exists and is valid YAML
**Styling issues**: Verify color codes and font names in the style definitions
**Long content**: The generator handles page breaks automatically

---

Generated PDFs are ready for job applications, academic submissions, and professional networking! 🚀
