#!/usr/bin/env python3
"""
Generate an elegant PDF resume from _data/cv.yml
"""

import yaml
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import os

class ResumeGenerator:
    def __init__(self, cv_file='_data/cv.yml', output_file='Wei_Fu_Resume.pdf'):
        self.cv_file = cv_file
        self.output_file = output_file
        self.doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Custom styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

        # Story will hold all flowables
        self.story = []

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Name style
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))

        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor('#34495e')
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=16,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=(0, 0, 3, 0),
            leftIndent=0
        ))

        # Entry title style
        self.styles.add(ParagraphStyle(
            name='EntryTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=2
        ))

        # Entry info style
        self.styles.add(ParagraphStyle(
            name='EntryInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=4
        ))

        # Entry description style
        self.styles.add(ParagraphStyle(
            name='EntryDescription',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            leftIndent=0
        ))

        # Publication style
        self.styles.add(ParagraphStyle(
            name='Publication',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=6,
            leftIndent=0
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
        """Add header with name and contact info"""
        # Name
        name = Paragraph(data['name'], self.styles['Name'])
        self.story.append(name)

        # Contact information split into two rows for better formatting
        # First row: basic contact info
        first_row_parts = []
        if data.get('email'):
            first_row_parts.append(f"Email: {data['email'].replace(' AT ', '@').replace(' DOT ', '.')}")
        if data.get('phone'):
            first_row_parts.append(f"Phone: {data['phone']}")
        if data.get('location'):
            first_row_parts.append(f"Location: {data['location']}")

        if first_row_parts:
            first_row = Paragraph(' '.join(first_row_parts), self.styles['ContactInfo'])
            self.story.append(first_row)

        # Second row: website only
        if data.get('website'):
            website_para = Paragraph(f"Website: {data['website']}", self.styles['ContactInfo'])
            self.story.append(website_para)

        # Add a horizontal line
        self.story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3498db')))
        self.story.append(Spacer(1, 6))

    def add_education_section(self, education_data):
        """Add education section"""
        if not education_data:
            return

        self.story.append(Paragraph("EDUCATION", self.styles['SectionHeader']))

        for edu in education_data:
            # Degree and Institution
            title_parts = []
            if edu.get('degree'):
                title_parts.append(edu['degree'])
            if edu.get('institution'):
                title_parts.append(edu['institution'])

            if title_parts:
                title = Paragraph(' '.join(title_parts), self.styles['EntryTitle'])
                self.story.append(title)

            # Location and dates
            info_parts = []
            if edu.get('location'):
                info_parts.append(edu['location'])
            if edu.get('dates'):
                info_parts.append(edu['dates'])

            if info_parts:
                info = Paragraph(' | '.join(info_parts), self.styles['EntryInfo'])
                self.story.append(info)

            # Additional info
            if edu.get('advisor'):
                advisor = Paragraph(f"Advisor: {edu['advisor']}", self.styles['EntryInfo'])
                self.story.append(advisor)

            if edu.get('thesis'):
                thesis = Paragraph(f"Thesis: {edu['thesis']}", self.styles['EntryInfo'])
                self.story.append(thesis)

            if edu.get('research_direction'):
                research = Paragraph(f"Research: {edu['research_direction']}", self.styles['EntryInfo'])
                self.story.append(research)

            self.story.append(Spacer(1, 4))

    def add_publications_section(self, publications_data):
        """Add publications section"""
        if not publications_data:
            return

        self.story.append(Paragraph("PUBLICATIONS", self.styles['SectionHeader']))

        # Group publications by year (descending)
        pub_by_year = {}
        for pub in publications_data:
            year = pub.get('year', 'Unknown')
            if year not in pub_by_year:
                pub_by_year[year] = []
            pub_by_year[year].append(pub)

        # Sort years in descending order
        for year in sorted(pub_by_year.keys(), reverse=True):
            pubs = pub_by_year[year]

            for pub in pubs:
                # Format publication
                parts = []

                # Authors
                if pub.get('authors'):
                    authors = self.clean_html_tags(pub['authors'])
                    parts.append(authors)

                # Title
                if pub.get('title'):
                    title = f'"{pub["title"]}"'
                    parts.append(title)

                # Venue and year
                venue_parts = []
                if pub.get('venue'):
                    venue_parts.append(pub['venue'])
                if pub.get('year'):
                    venue_parts.append(str(pub['year']))

                if venue_parts:
                    parts.append(', '.join(venue_parts))

                # Note
                if pub.get('note'):
                    parts.append(f"({pub['note']})")

                pub_text = '. '.join(parts) + '.'

                pub_para = Paragraph(pub_text, self.styles['Publication'])
                self.story.append(pub_para)

        self.story.append(Spacer(1, 4))

    def add_experience_section(self, experience_data):
        """Add experience section"""
        if not experience_data:
            return

        self.story.append(Paragraph("EXPERIENCE", self.styles['SectionHeader']))

        for exp in experience_data:
            # Position and Company
            title_parts = []
            if exp.get('position'):
                title_parts.append(exp['position'])
            if exp.get('company'):
                title_parts.append(exp['company'])

            if title_parts:
                title = Paragraph(' '.join(title_parts), self.styles['EntryTitle'])
                self.story.append(title)

            # Dates
            if exp.get('dates'):
                dates = Paragraph(exp['dates'], self.styles['EntryInfo'])
                self.story.append(dates)

            # Description with HTML to ReportLab conversion (preserve hyperlinks)
            if exp.get('description'):
                desc = self.convert_html_to_reportlab(exp['description'])
                description = Paragraph(desc, self.styles['EntryDescription'])
                self.story.append(description)

            self.story.append(Spacer(1, 4))

    def add_awards_section(self, awards_data):
        """Add awards section"""
        if not awards_data:
            return

        self.story.append(Paragraph("AWARDS & HONORS", self.styles['SectionHeader']))

        for award in awards_data:
            award_parts = []
            if award.get('name'):
                award_parts.append(award['name'])
            if award.get('year'):
                award_parts.append(str(award['year']))

            if award_parts:
                award_text = ' '.join(award_parts)
                award_para = Paragraph(award_text, self.styles['EntryDescription'])
                self.story.append(award_para)

        self.story.append(Spacer(1, 4))

    def add_service_section(self, service_data):
        """Add service section"""
        if not service_data:
            return

        self.story.append(Paragraph("SERVICE", self.styles['SectionHeader']))

        for service in service_data:
            service_parts = []
            if service.get('role'):
                service_parts.append(service['role'])
            if service.get('venues'):
                service_parts.append(service['venues'])
            if service.get('years'):
                service_parts.append(str(service['years']))

            if service_parts:
                service_text = ' '.join(service_parts)
                service_para = Paragraph(service_text, self.styles['EntryDescription'])
                self.story.append(service_para)

        self.story.append(Spacer(1, 4))

    def generate_pdf(self):
        """Generate the complete PDF resume"""
        print(f"Loading CV data from {self.cv_file}...")
        data = self.load_cv_data()

        print("Building resume content...")

        # Add header
        self.add_header(data)

        # Add sections
        self.add_education_section(data.get('education'))
        self.add_publications_section(data.get('publications'))
        self.add_experience_section(data.get('experience'))
        self.add_awards_section(data.get('awards'))
        self.add_service_section(data.get('service'))

        # Build PDF
        print(f"Generating PDF: {self.output_file}...")
        self.doc.build(self.story)

        print(f"✓ Resume generated successfully: {self.output_file}")
        return self.output_file

def main():
    # Check if cv.yml exists
    cv_file = '_data/cv.yml'
    if not os.path.exists(cv_file):
        print(f"Error: {cv_file} not found!")
        return

    try:
        # Generate resume
        generator = ResumeGenerator(cv_file)
        output_file = generator.generate_pdf()

        print(f"\n✓ PDF resume generated successfully!")
        print(f"Output file: {output_file}")
        print(f"File size: {os.path.getsize(output_file) / 1024:.1f} KB")

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
