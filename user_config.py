"""
User Profile Configuration Module
Manages user profile and preferences from JSON configuration
"""

import json
import os
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UserProfile:
    """Represents user profile for job matching"""
    name: str = ""
    email: str = ""
    skills: List[str] = field(default_factory=list)
    experience_years: int = 0
    preferred_locations: List[str] = field(default_factory=list)
    job_titles: List[str] = field(default_factory=list)
    job_types: List[str] = field(default_factory=list)
    salary_min: int = 0
    salary_max: int = 0
    salary_currency: str = "USD"
    remote_only: bool = False
    willing_to_relocate: bool = True
    visa_sponsorship_required: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for backward compatibility"""
        return {
            'name': self.name,
            'email': self.email,
            'skills': ', '.join(self.skills),
            'experience_years': str(self.experience_years),
            'preferred_locations': ', '.join(self.preferred_locations),
            'job_titles': ', '.join(self.job_titles),
            'job_types': ', '.join(self.job_types),
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'salary_currency': self.salary_currency,
            'remote_only': self.remote_only,
            'willing_to_relocate': self.willing_to_relocate,
            'visa_sponsorship_required': self.visa_sponsorship_required
        }


@dataclass
class UserPreferences:
    """Represents user preferences for job filtering"""
    company_size: List[str] = field(default_factory=list)
    industries: List[str] = field(default_factory=list)
    avoid_keywords: List[str] = field(default_factory=list)
    required_keywords: List[str] = field(default_factory=list)
    nice_to_have: List[str] = field(default_factory=list)


class UserConfigManager:
    """Manages user profile and preferences from JSON configuration"""
    
    def __init__(self, config_file: str = 'user_profile.json'):
        """
        Initialize user configuration manager
        
        Args:
            config_file: Path to JSON configuration file
        """
        self.config_file = config_file
        self.profile: Optional[UserProfile] = None
        self.preferences: Optional[UserPreferences] = None
        self.settings: Dict = {}
    
    def load_from_json(self) -> bool:
        """
        Load user profile from JSON configuration file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.config_file):
                logger.warning(f"Config file {self.config_file} not found")
                return False
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Load profile
            profile_data = config.get('profile', {})
            salary_data = profile_data.get('salary_expectations', {})
            work_prefs = profile_data.get('work_preferences', {})
            
            self.profile = UserProfile(
                name=profile_data.get('name', ''),
                email=profile_data.get('email', ''),
                skills=profile_data.get('skills', []),
                experience_years=profile_data.get('experience_years', 0),
                preferred_locations=profile_data.get('preferred_locations', []),
                job_titles=profile_data.get('job_titles', []),
                job_types=profile_data.get('job_types', []),
                salary_min=salary_data.get('min', 0),
                salary_max=salary_data.get('max', 0),
                salary_currency=salary_data.get('currency', 'USD'),
                remote_only=work_prefs.get('remote_only', False),
                willing_to_relocate=work_prefs.get('willing_to_relocate', True),
                visa_sponsorship_required=work_prefs.get('visa_sponsorship_required', False)
            )
            
            # Load preferences
            prefs_data = config.get('preferences', {})
            self.preferences = UserPreferences(
                company_size=prefs_data.get('company_size', []),
                industries=prefs_data.get('industries', []),
                avoid_keywords=prefs_data.get('avoid_keywords', []),
                required_keywords=prefs_data.get('required_keywords', []),
                nice_to_have=prefs_data.get('nice_to_have', [])
            )
            
            # Load settings
            self.settings = config.get('settings', {})
            
            logger.info(f"Loaded user profile from {self.config_file}")
            logger.info(f"  Skills: {len(self.profile.skills)}")
            logger.info(f"  Experience: {self.profile.experience_years} years")
            logger.info(f"  Preferred locations: {len(self.profile.preferred_locations)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return False
    
    def load_from_env(self) -> bool:
        """
        Load user profile from environment variables (fallback)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            skills = os.getenv('YOUR_SKILLS', '')
            experience = os.getenv('YOUR_EXPERIENCE_YEARS', '0')
            locations = os.getenv('YOUR_PREFERRED_LOCATIONS', '')
            titles = os.getenv('YOUR_JOB_TITLES', '')
            
            if not skills and not titles:
                logger.warning("No user profile found in environment variables")
                return False
            
            self.profile = UserProfile(
                skills=skills.split(',') if skills else [],
                experience_years=int(experience) if experience.isdigit() else 0,
                preferred_locations=locations.split(',') if locations else [],
                job_titles=titles.split(',') if titles else []
            )
            
            self.preferences = UserPreferences()
            self.settings = {}
            
            logger.info("Loaded user profile from environment variables")
            return True
            
        except Exception as e:
            logger.error(f"Error loading from environment: {e}")
            return False

