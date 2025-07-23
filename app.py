#!/usr/bin/env python3
"""
Resume Generator - Simple working version with external CSS
"""

import os
from pathlib import Path
import weasyprint
import markdown

class SimpleResumeGenerator:
    def __init__(self, input_dir="resume_sections", css_file="./assets/css/resume.css", output_file="resume.pdf"):
        self.input_dir = Path(input_dir)
        self.css_file = css_file
        self.output_file = output_file
        
    def read_file(self, filename):
        file_path = self.input_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return ""

    def read_css(self):
        if os.path.exists(self.css_file):
            with open(self.css_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def generate_resume(self):
        # Read files
        header_content = self.read_file("header.md")
        header_lines = [line.strip() for line in header_content.split('\n') if line.strip()]
        
        name = header_lines[0] if len(header_lines) > 0 else "Name"
        title = header_lines[1] if len(header_lines) > 1 else "Title"
        contact_line1 = header_lines[2] if len(header_lines) > 2 else ""
        contact_line2 = header_lines[3] if len(header_lines) > 3 else ""
        
        intro = markdown.markdown(self.read_file("intro.md"))
        experience_1 = markdown.markdown(self.read_file("experience_1.md"))
        experience_2 = markdown.markdown(self.read_file("experience_2.md"))
        skills = markdown.markdown(self.read_file("skills.md"))
        projects = markdown.markdown(self.read_file("projects.md"))
        education = markdown.markdown(self.read_file("education.md"))
        css_content = self.read_css()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{name} - Resume</title>
            <style>{css_content}</style>
        </head>
        <body>
            <div class="page-content">
                <div class="header">
                    <div class="name">{name}</div>
                    <div class="title">{title}</div>
                    <div class="contact">{contact_line1}</div>
                    <div class="contact">{contact_line2}</div>
                </div>
                
                <div class="section">
                    <h2>Professional Summary</h2>
                    {intro}
                </div>
                
                <table>
                    <tr>
                        <td class="left">
                            <h2>Experience</h2>
                            {experience_1}
                        </td>
                        <td class="right">
                            <h2>Skills</h2>
                            {skills}
                        </td>
                    </tr>
                    <tr>
                        <td class="left">
                            {experience_2}
                        </td>
                        <td class="right">
                            <h2>Projects</h2>
                            {projects}
                        </td>
                    </tr>
                </table>
                
                <div class="section education">
                    <h2>Education</h2>
                    {education}
                </div>
            </div>
        </body>
        </html>
        """

        weasyprint.HTML(string=html).write_pdf(self.output_file)
        print(f"Resume generated: {self.output_file}")

def main():
    generator = SimpleResumeGenerator()
    generator.generate_resume()

if __name__ == "__main__":
    main()