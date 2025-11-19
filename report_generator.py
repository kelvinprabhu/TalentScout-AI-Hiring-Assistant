# ============================================================================
# File: report_generator.py
"""PDF and JSON report generation."""

import os
import json
from datetime import datetime
from typing import Dict, List
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from config import AppConfig


def ensure_reports_folder():
    """Create Reports folder if it doesn't exist."""
    config = AppConfig()
    if not os.path.exists(config.REPORTS_FOLDER):
        os.makedirs(config.REPORTS_FOLDER)


def generate_pdf_report(candidate_info: Dict, qa_pairs: List[Dict], analysis: str, filename: str):
    """
    Generate PDF report for candidate assessment.
    """
    ensure_reports_folder()
    config = AppConfig()
    filepath = os.path.join(config.REPORTS_FOLDER, filename)

    # Create PDF
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    elements = []

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1E88E5'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1E88E5'),
        spaceBefore=12,
        spaceAfter=12
    )

    # Title
    elements.append(Paragraph("🎯 TalentScout Candidate Assessment Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Metadata
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    elements.append(Paragraph(f"<b>Report Generated:</b> {report_date}", styles['Normal']))
    elements.append(Spacer(1, 0.3 * inch))

    # Candidate Information
    elements.append(Paragraph("📋 Candidate Information", heading_style))

    # -------------------------
    # BUILD INFO TABLE DATA
    # -------------------------
    info_data = []

    if candidate_info.get('full_name'):
        info_data.append(['Full Name:', candidate_info['full_name']])

    if candidate_info.get('email'):
        info_data.append(['Email:', candidate_info['email']])

    if candidate_info.get('phone_number'):
        info_data.append(['Phone:', candidate_info['phone_number']])

    if candidate_info.get('years_of_experience'):
        info_data.append(['Experience:', f"{candidate_info['years_of_experience']} years"])

    if candidate_info.get('desired_positions'):
        pos = candidate_info['desired_positions']
        if isinstance(pos, list):
            pos = ', '.join(pos)
        info_data.append(['Desired Role(s):', pos])

    if candidate_info.get('current_location'):
        info_data.append(['Location:', candidate_info['current_location']])

    if candidate_info.get('tech_stack'):
        tech = candidate_info['tech_stack']
        if isinstance(tech, dict):
            collected = []
            for _, items in tech.items():
                if isinstance(items, list):
                    collected.extend(items)
                else:
                    collected.append(str(items))
            tech = ', '.join(collected)
        info_data.append(['Tech Stack:', tech])

    # ---- SAFETY GUARD: no empty table ----
    if not info_data:
        info_data = [["Info", "Not provided"]]

    # Table creation
    info_table = Table(info_data, colWidths=[2 * inch, 4.5 * inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 0.4 * inch))

    # Technical Assessment Section
    elements.append(Paragraph("💻 Technical Assessment Q&A", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    for i, qa in enumerate(qa_pairs, 1):
        elements.append(Paragraph(f"<b>Question {i}:</b>", styles['Normal']))
        elements.append(Paragraph(qa['question'], styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))

        elements.append(Paragraph(f"<b>Answer:</b>", styles['Normal']))
        elements.append(Paragraph(qa['answer'], styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))

    elements.append(PageBreak())

    # Analysis Section
    elements.append(Paragraph("📊 Candidate Analysis", heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    for para in analysis.split("\n\n"):
        if para.strip():
            elements.append(Paragraph(para, styles['Normal']))
            elements.append(Spacer(1, 0.15 * inch))

    elements.append(Spacer(1, 0.5 * inch))

    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Generated by TalentScout AI Hiring Assistant", footer_style))

    doc.build(elements)

    return filepath

def generate_json_report(candidate_info: Dict, qa_pairs: List[Dict], analysis: str, filename: str):
    """
    Generate JSON report for candidate assessment.
    
    :param candidate_info: Dictionary containing candidate information
    :param qa_pairs: List of question-answer pairs
    :param analysis: AI-generated analysis text
    :param filename: Output filename
    """
    ensure_reports_folder()
    config = AppConfig()
    filepath = os.path.join(config.REPORTS_FOLDER, filename)
    
    report_data = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "report_type": "Technical Screening Assessment",
            "generated_by": "TalentScout AI"
        },
        "candidate_information": candidate_info,
        "technical_assessment": {
            "total_questions": len(qa_pairs),
            "qa_pairs": qa_pairs
        },
        "ai_analysis": analysis
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    return filepath


def generate_reports(candidate_info: Dict, qa_pairs: List[Dict], analysis: str) -> tuple:
    """
    Generate both PDF and JSON reports.
    
    :return: Tuple of (pdf_filepath, json_filepath)
    """
    from utils import generate_filename
    
    candidate_name = candidate_info.get('full_name', 'Unknown_Candidate')
    
    pdf_filename = generate_filename(candidate_name, 'pdf')
    json_filename = generate_filename(candidate_name, 'json')
    
    pdf_path = generate_pdf_report(candidate_info, qa_pairs, analysis, pdf_filename)
    json_path = generate_json_report(candidate_info, qa_pairs, analysis, json_filename)
    
    return pdf_path, json_path


