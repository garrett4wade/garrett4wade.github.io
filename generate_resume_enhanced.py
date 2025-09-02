#!/usr/bin/env python3
"""
Generate an enhanced elegant PDF resume from _data/cv.yml
"""

import yaml
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                               PageBreak, KeepTogether)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

class EnhancedResumeGenerator:
    def __init__(self, cv_file='_data/cv.yml', output_file='Wei_Fu_Resume_Enhanced.pdf'):
        self.cv_file = cv_file
        self.output_file = output_file

        # Page setup with better margins
        self.doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.5*inch,
            bottomMargin=0.75*inch
        )

        # Setup styles
        self.styles = getSampleStyleSheet()
        self._setup_enhanced_styles()

        # Story will hold all flowables
        self.story = []

    def _setup_enhanced_styles(self):
        """Setup enhanced paragraph styles with better typography"""

        # Define color palette
        primary_color = colors.HexColor('#1f4e79')      # Deep blue
        secondary_color = colors.HexColor('#2980b9')    # Medium blue
        accent_color = colors.HexColor('#3498db')       # Light blue
        text_color = colors.HexColor('#2c3e50')         # Dark gray
        meta_color = colors.HexColor('#7f8c8d')         # Medium gray
        light_text = colors.HexColor('#34495e')         # Light gray

        # Name style - larger and more prominent
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Title'],
            fontSize=28,
            textColor=primary_color,
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            leading=32
        ))

        # Contact info style - better spacing
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=16,
            textColor=text_color,
            leading=14
        ))

        # Section header style - with underline effect
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=15,
            textColor=primary_color,
            spaceBefore=20,
            spaceAfter=10,
            fontName='Helvetica-Bold',
            leftIndent=0,
            leading=18,
            borderWidth=0,
            borderColor=accent_color
        ))

        # Entry title style - professional look
        self.styles.add(ParagraphStyle(
            name='EntryTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=text_color,
            spaceAfter=3,
            leading=15
        ))

        # Entry subtitle style - for institution/company
        self.styles.add(ParagraphStyle(
            name='EntrySubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Oblique',
            textColor=secondary_color,
            spaceAfter=2,
            leading=14
        ))

        # Entry info style - dates and location
        self.styles.add(ParagraphStyle(
            name='EntryInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=meta_color,
            spaceAfter=6,
            leading=12
        ))

        # Entry description style - better readability
        self.styles.add(ParagraphStyle(
            name='EntryDescription',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=light_text,
            spaceAfter=10,
            leftIndent=0,
            leading=13,
            alignment=TA_JUSTIFY
        ))

        # Publication style - academic format
        self.styles.add(ParagraphStyle(
            name='Publication',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=light_text,
            spaceAfter=8,
            leftIndent=0,
            leading=12,
            alignment=TA_JUSTIFY
        ))

        # Compact list style
        self.styles.add(ParagraphStyle(
            name='CompactList',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=light_text,
            spaceAfter=4,
            leftIndent=0,
            leading=12
        ))

    def load_cv_data(self):
        """Load CV data from YAML file"""
        with open(self.cv_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def clean_html_tags(self, text):
        """Remove HTML tags and convert to plain text for PDF"""
        if not text:
            return ""
        # Remove HTML tags but preserve the text
        clean_text = re.sub(r'<[^>]+>', '', str(text))
        return clean_text

    def convert_html_to_reportlab(self, text):
        """Convert HTML tags to ReportLab markup for hyperlinks and formatting"""
        if not text:
            return ""

        # Convert HTML links to ReportLab links
        # Pattern: <a href="url">text</a> -> <link href="url">text</link>
        text = re.sub(r'<a\s+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>', r'<link href="\1">\2</link>', text)

        # Keep existing strong tags as they work in ReportLab
        # <strong>text</strong> -> <b>text</b>
        text = re.sub(r'<strong>([^<]+)</strong>', r'<b>\1</b>', text)

        return text

    def add_header(self, data):
        """Add enhanced header with name and contact info"""
        # Name with better spacing
        name = Paragraph(data['name'], self.styles['Name'])
        self.story.append(name)

        # Contact information split into two rows for better formatting
        # First row: basic contact info
        first_row_parts = []
        if data.get('email'):
            email = data['email'].replace(' AT ', '@').replace(' DOT ', '.')
            first_row_parts.append(f"📧 {email}")
        if data.get('phone'):
            first_row_parts.append(f"📞 {data['phone']}")
        if data.get('location'):
            first_row_parts.append(f"📍 {data['location']}")

        if first_row_parts:
            first_row = Paragraph(' '.join(first_row_parts), self.styles['ContactInfo'])
            self.story.append(first_row)

        # Second row: website only
        if data.get('website'):
            website_url = data['website']
            # Create clickable link
            website_para = Paragraph(f'🌐 <link href="{website_url}">{website_url}</link>', self.styles['ContactInfo'])
            self.story.append(website_para)

        # Add a styled horizontal line
        self.story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=colors.HexColor('#3498db'),
            spaceAfter=8
        ))

    def add_section_header(self, title):
        """Add a section header with consistent styling"""
        header = Paragraph(title.upper(), self.styles['SectionHeader'])
        self.story.append(header)

        # Add a subtle line under section headers
        self.story.append(HRFlowable(
            width="20%",
            thickness=1,
            color=colors.HexColor('#bdc3c7'),
            spaceAfter=8
        ))

    def add_education_section(self, education_data):
        """Add enhanced education section"""
        if not education_data:
            return

        self.add_section_header("Education")

        for edu in education_data:
            # Degree (main title)
            if edu.get('degree'):
                degree = Paragraph(edu['degree'], self.styles['EntryTitle'])
                self.story.append(degree)

            # Institution (subtitle)
            if edu.get('institution'):
                institution = Paragraph(edu['institution'], self.styles['EntrySubtitle'])
                self.story.append(institution)

            # Location and dates in a structured way
            info_parts = []
            if edu.get('location'):
                info_parts.append(f"📍 {edu['location']}")
            if edu.get('dates'):
                info_parts.append(f"📅 {edu['dates']}")

            if info_parts:
                info = Paragraph(' '.join(info_parts), self.styles['EntryInfo'])
                self.story.append(info)

            # Additional details
            details = []
            if edu.get('advisor'):
                details.append(f"Advisor: {edu['advisor']}")
            if edu.get('thesis'):
                details.append(f"Thesis: \"{edu['thesis']}\"")
            if edu.get('research_direction'):
                details.append(f"Research Areas: {edu['research_direction']}")

            for detail in details:
                detail_para = Paragraph(detail, self.styles['EntryInfo'])
                self.story.append(detail_para)

            self.story.append(Spacer(1, 8))

    def add_publications_section(self, publications_data):
        """Add enhanced publications section with better formatting"""
        if not publications_data:
            return

        self.add_section_header("Publications")

        # Group publications by type and year
        conferences = []
        preprints = []

        for pub in publications_data:
            if pub.get('type') == 'conference':
                conferences.append(pub)
            else:
                preprints.append(pub)

        # Sort by year (descending)
        conferences.sort(key=lambda x: x.get('year', 0), reverse=True)
        preprints.sort(key=lambda x: x.get('year', 0), reverse=True)

        # Add preprints first (requested change)
        if preprints:
            preprint_header = Paragraph("Preprints & Under Review", self.styles['EntrySubtitle'])
            self.story.append(preprint_header)
            self.story.append(Spacer(1, 4))

            for pub in preprints:
                self._format_publication(pub)

        # Add conferences after preprints
        if conferences:
            if preprints:  # Add spacing if we had preprints
                self.story.append(Spacer(1, 8))

            conf_header = Paragraph("Conference Publications", self.styles['EntrySubtitle'])
            self.story.append(conf_header)
            self.story.append(Spacer(1, 4))

            for pub in conferences:
                self._format_publication(pub)

    def _format_publication(self, pub):
        """Format a single publication entry"""
        parts = []

        # Authors (with name highlighting)
        if pub.get('authors'):
            authors = self.clean_html_tags(pub['authors'])
            # Bold the author's name
            authors = authors.replace('Wei Fu', '<b>Wei Fu</b>')
            parts.append(authors)

        # Title in quotes and bold (requested change)
        if pub.get('title'):
            title = f'"{pub["title"]}"'
            parts.append(f"<b><i>{title}</i></b>")

        # Venue and year
        venue_parts = []
        if pub.get('venue'):
            venue_parts.append(f"<b>{pub['venue']}</b>")
        if pub.get('year'):
            venue_parts.append(str(pub['year']))

        if venue_parts:
            parts.append(', '.join(venue_parts))

        # Special notes (awards, etc.)
        if pub.get('note'):
            parts.append(f"<b>[{pub['note']}]</b>")

        # Combine all parts
        pub_text = '. '.join(parts) + '.'

        # Create paragraph with rich formatting
        pub_para = Paragraph(pub_text, self.styles['Publication'])
        self.story.append(pub_para)

    def add_experience_section(self, experience_data):
        """Add enhanced experience section"""
        if not experience_data:
            return

        self.add_section_header("Research Experience")

        for exp in experience_data:
            # Position title
            if exp.get('position'):
                position = Paragraph(exp['position'], self.styles['EntryTitle'])
                self.story.append(position)

            # Company
            if exp.get('company'):
                company = Paragraph(exp['company'], self.styles['EntrySubtitle'])
                self.story.append(company)

            # Dates
            if exp.get('dates'):
                dates = Paragraph(f"📅 {exp['dates']}", self.styles['EntryInfo'])
                self.story.append(dates)

            # Description with HTML to ReportLab conversion (preserve hyperlinks)
            if exp.get('description'):
                desc = self.convert_html_to_reportlab(exp['description'])
                description = Paragraph(desc, self.styles['EntryDescription'])
                self.story.append(description)

            self.story.append(Spacer(1, 10))

    def add_awards_section(self, awards_data):
        """Add awards section with better formatting"""
        if not awards_data:
            return

        self.add_section_header("Awards & Honors")

        for award in awards_data:
            award_parts = []
            if award.get('name'):
                award_parts.append(f"🏆 <b>{award['name']}</b>")
            if award.get('year'):
                award_parts.append(str(award['year']))

            if award_parts:
                award_text = ' '.join(award_parts)
                award_para = Paragraph(award_text, self.styles['CompactList'])
                self.story.append(award_para)

        self.story.append(Spacer(1, 8))

    def add_service_section(self, service_data):
        """Add service section with better formatting"""
        if not service_data:
            return

        self.add_section_header("Academic Service")

        for service in service_data:
            service_parts = []
            if service.get('role'):
                service_parts.append(f"📝 <b>{service['role']}</b>")
            if service.get('venues'):
                service_parts.append(service['venues'])
            if service.get('years'):
                service_parts.append(f"({service['years']})")

            if service_parts:
                service_text = ' '.join(service_parts)
                service_para = Paragraph(service_text, self.styles['CompactList'])
                self.story.append(service_para)

        self.story.append(Spacer(1, 8))

    def add_footer(self):
        """Add a footer with generation date"""
        footer_text = f"<i>Generated on {datetime.now().strftime('%B %d, %Y')}</i>"
        footer = Paragraph(footer_text, self.styles['EntryInfo'])
        footer.hAlign = 'CENTER'
        self.story.append(Spacer(1, 20))
        self.story.append(footer)

    def generate_pdf(self):
        """Generate the complete enhanced PDF resume"""
        print(f"Loading CV data from {self.cv_file}...")
        data = self.load_cv_data()

        print("Building enhanced resume content...")

        # Add header
        self.add_header(data)

        # Add sections in logical order
        self.add_education_section(data.get('education'))
        self.add_publications_section(data.get('publications'))
        self.add_experience_section(data.get('experience'))
        self.add_awards_section(data.get('awards'))
        self.add_service_section(data.get('service'))

        # Add footer
        self.add_footer()

        # Build PDF
        print(f"Generating enhanced PDF: {self.output_file}...")
        self.doc.build(self.story)

        print(f"✓ Enhanced resume generated successfully: {self.output_file}")
        return self.output_file

def main():
    # Check if cv.yml exists
    cv_file = '_data/cv.yml'
    if not os.path.exists(cv_file):
        print(f"Error: {cv_file} not found!")
        return

    try:
        # Generate enhanced resume
        generator = EnhancedResumeGenerator(cv_file)
        output_file = generator.generate_pdf()

        print(f"\n✓ Enhanced PDF resume generated successfully!")
        print(f"Output file: {output_file}")
        print(f"File size: {os.path.getsize(output_file) / 1024:.1f} KB")

        # Also generate the basic version for comparison
        from generate_resume import ResumeGenerator
        basic_generator = ResumeGenerator(cv_file, 'Wei_Fu_Resume_Basic.pdf')
        basic_output = basic_generator.generate_pdf()

        print(f"\n✓ Both versions generated:")
        print(f"Basic: Wei_Fu_Resume_Basic.pdf ({os.path.getsize('Wei_Fu_Resume_Basic.pdf') / 1024:.1f} KB)")
        print(f"Enhanced: {output_file} ({os.path.getsize(output_file) / 1024:.1f} KB)")

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
