"""
Email Sender Module
Sends job analysis results via SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """Send email notifications with job analysis results"""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        """
        Initialize email sender
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            username: SMTP username (email)
            password: SMTP password or app password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send_job_report(self, to_email: str, analyses: List[Dict], total_jobs: int) -> bool:
        """
        Send job analysis report via email
        
        Args:
            to_email: Recipient email address
            analyses: List of job analysis results
            total_jobs: Total number of jobs processed
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            logger.info(f"Preparing email report for {to_email}")
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Daily Job Report - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.username
            msg['To'] = to_email
            
            # Create email body
            html_body = self._create_html_body(analyses, total_jobs)
            text_body = self._create_text_body(analyses, total_jobs)
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def _create_text_body(self, analyses: List[Dict], total_jobs: int) -> str:
        """Create plain text email body"""
        
        suitable_jobs = [a for a in analyses if a.get('suitable', False)]
        
        body = f"""
Daily Job Report - {datetime.now().strftime('%Y-%m-%d')}
{'=' * 60}

Summary:
- Total jobs processed: {total_jobs}
- Jobs analyzed: {len(analyses)}
- Suitable jobs found: {len(suitable_jobs)}

"""
        
        if suitable_jobs:
            body += "\nSUITABLE JOBS (Score >= 60):\n"
            body += "=" * 60 + "\n\n"
            
            for i, job in enumerate(suitable_jobs, 1):
                body += f"{i}. {job['title']}\n"
                body += f"   Score: {job['score']}/100\n"
                body += f"   URL: {job['url']}\n"
                body += f"   Recommendation: {job['recommendation']}\n"
                
                if job.get('matching_points'):
                    body += f"   Matching Points:\n"
                    for point in job['matching_points'][:3]:
                        body += f"   - {point}\n"
                
                body += "\n"
        else:
            body += "\nNo suitable jobs found today.\n"
        
        body += "\n" + "=" * 60 + "\n"
        body += "This is an automated report from your Job Automation System.\n"
        
        return body
    
    def _create_html_body(self, analyses: List[Dict], total_jobs: int) -> str:
        """Create HTML email body"""
        
        suitable_jobs = [a for a in analyses if a.get('suitable', False)]
        
        html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .summary {{ background-color: #f4f4f4; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .job-card {{ border: 1px solid #ddd; padding: 15px; margin: 15px 0; border-radius: 5px; }}
        .job-title {{ color: #2196F3; font-size: 18px; font-weight: bold; }}
        .score {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .score-low {{ color: #ff9800; }}
        .matching-points {{ color: #4CAF50; }}
        .gaps {{ color: #f44336; }}
        ul {{ margin: 10px 0; }}
        .footer {{ text-align: center; color: #777; margin-top: 30px; padding: 20px; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Daily Job Report</h1>
        <p>{datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <ul>
            <li><strong>Total jobs processed:</strong> {total_jobs}</li>
            <li><strong>Jobs analyzed:</strong> {len(analyses)}</li>
            <li><strong>Suitable jobs found:</strong> {len(suitable_jobs)}</li>
        </ul>
    </div>
"""
        
        if suitable_jobs:
            html += "<h2>Suitable Jobs (Score >= 60)</h2>"
            
            for job in suitable_jobs:
                score_class = 'score' if job['score'] >= 80 else 'score-low'
                
                html += f"""
    <div class="job-card">
        <div class="job-title">{job['title']}</div>
        <div class="{score_class}">Score: {job['score']}/100</div>
        <p><strong>URL:</strong> <a href="{job['url']}">{job['url']}</a></p>
        <p><strong>Recommendation:</strong> {job['recommendation']}</p>
"""
                
                if job.get('matching_points'):
                    html += '<p class="matching-points"><strong>Matching Points:</strong></p><ul>'
                    for point in job['matching_points']:
                        html += f'<li>{point}</li>'
                    html += '</ul>'
                
                if job.get('gaps'):
                    html += '<p class="gaps"><strong>Gaps/Concerns:</strong></p><ul>'
                    for gap in job['gaps']:
                        html += f'<li>{gap}</li>'
                    html += '</ul>'
                
                html += "</div>"
        else:
            html += "<p>No suitable jobs found today. Keep your skills sharp and check back tomorrow!</p>"
        
        html += """
    <div class="footer">
        <p>This is an automated report from your Job Automation System.</p>
    </div>
</body>
</html>
"""
        
        return html

