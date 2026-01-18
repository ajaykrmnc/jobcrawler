"""
Job Analyzer Module
Uses Gemini API to analyze job postings and determine suitability
"""

import google.generativeai as genai
from typing import Dict, List, Optional
import os
from logger import get_logger

logger = get_logger(__name__)


class JobAnalyzer:
    """Analyze job postings using Gemini API"""
    
    def __init__(self, api_key: str, user_profile: Dict):
        """
        Initialize job analyzer with Gemini API
        
        Args:
            api_key: Gemini API key
            user_profile: Dictionary containing user's skills, experience, etc.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.user_profile = user_profile
    
    def analyze_job(self, job_content: Dict) -> Optional[Dict]:
        """
        Analyze a single job posting
        
        Args:
            job_content: Dictionary with job title, content, and URL
            
        Returns:
            Dictionary with analysis results including suitability score and reasoning
        """
        try:
            logger.info(f"Analyzing job: {job_content.get('title', 'Unknown')}")
            
            # Create prompt for Gemini
            prompt = self._create_analysis_prompt(job_content)
            
            # Generate analysis
            response = self.model.generate_content(prompt)
            
            # Parse response
            analysis = self._parse_response(response.text, job_content)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing job {job_content.get('url', 'Unknown')}: {str(e)}")
            return None
    
    def _create_analysis_prompt(self, job_content: Dict) -> str:
        """Create prompt for Gemini API"""
        
        prompt = f"""
You are a job matching expert. Analyze the following job posting and determine if it's suitable for the candidate.

CANDIDATE PROFILE:
- Skills: {self.user_profile.get('skills', 'Not specified')}
- Years of Experience: {self.user_profile.get('experience_years', 'Not specified')}
- Preferred Locations: {self.user_profile.get('preferred_locations', 'Not specified')}
- Preferred Job Titles: {self.user_profile.get('job_titles', 'Not specified')}

JOB POSTING:
Title: {job_content.get('title', 'Unknown')}
URL: {job_content.get('url', 'Unknown')}

Content:
{job_content.get('content', 'No content available')[:3000]}

INSTRUCTIONS:
1. Analyze the job requirements and match them against the candidate's profile
2. Provide a suitability score from 0-100 (0 = not suitable, 100 = perfect match)
3. List key matching points
4. List any gaps or concerns
5. Provide a brief recommendation

Format your response EXACTLY as follows:
SCORE: [number 0-100]
MATCHING_POINTS:
- [point 1]
- [point 2]
...
GAPS:
- [gap 1]
- [gap 2]
...
RECOMMENDATION: [brief recommendation in 1-2 sentences]
"""
        return prompt
    
    def _parse_response(self, response_text: str, job_content: Dict) -> Dict:
        """Parse Gemini API response"""
        
        try:
            lines = response_text.strip().split('\n')
            score = 0
            matching_points = []
            gaps = []
            recommendation = ""
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('SCORE:'):
                    score_str = line.replace('SCORE:', '').strip()
                    score = int(''.join(filter(str.isdigit, score_str)))
                elif line.startswith('MATCHING_POINTS:'):
                    current_section = 'matching'
                elif line.startswith('GAPS:'):
                    current_section = 'gaps'
                elif line.startswith('RECOMMENDATION:'):
                    current_section = 'recommendation'
                    recommendation = line.replace('RECOMMENDATION:', '').strip()
                elif line.startswith('-') and current_section == 'matching':
                    matching_points.append(line[1:].strip())
                elif line.startswith('-') and current_section == 'gaps':
                    gaps.append(line[1:].strip())
                elif current_section == 'recommendation' and line:
                    recommendation += ' ' + line
            
            return {
                'title': job_content.get('title', 'Unknown'),
                'url': job_content.get('url', 'Unknown'),
                'score': score,
                'matching_points': matching_points,
                'gaps': gaps,
                'recommendation': recommendation.strip(),
                'suitable': score >= 60  # Consider jobs with 60+ score as suitable
            }
            
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            return {
                'title': job_content.get('title', 'Unknown'),
                'url': job_content.get('url', 'Unknown'),
                'score': 0,
                'matching_points': [],
                'gaps': [],
                'recommendation': 'Error analyzing job',
                'suitable': False
            }
    
    def analyze_multiple_jobs(self, job_contents: List[Dict]) -> List[Dict]:
        """
        Analyze multiple job postings
        
        Args:
            job_contents: List of job content dictionaries
            
        Returns:
            List of analysis results, sorted by suitability score
        """
        analyses = []
        
        for job_content in job_contents:
            analysis = self.analyze_job(job_content)
            if analysis:
                analyses.append(analysis)
        
        # Sort by score (highest first)
        analyses.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"Analyzed {len(analyses)} jobs successfully")
        return analyses

