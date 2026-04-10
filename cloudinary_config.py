"""
Cloudinary configuration for Wine E-commerce
Handles cloud image storage and optimization
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import current_app
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class CloudinaryConfig:
    """Configuration and initialization for Cloudinary"""
    
    @staticmethod
    def initialize():
        """
        Initialize Cloudinary with credentials from environment variables
        
        Required environment variables:
        - CLOUDINARY_CLOUD_NAME: Your Cloudinary cloud name
        - CLOUDINARY_API_KEY: Your Cloudinary API key
        - CLOUDINARY_API_SECRET: Your Cloudinary API secret
        """
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        api_key = os.getenv('CLOUDINARY_API_KEY')
        api_secret = os.getenv('CLOUDINARY_API_SECRET')
        
        if not all([cloud_name, api_key, api_secret]):
            raise ValueError(
                "Missing Cloudinary configuration. "
                "Set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET"
            )
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        logger.info(f"Cloudinary initialized with cloud: {cloud_name}")
    
    @staticmethod
    def get_cloudinary_url():
        """Get Cloudinary URL for image delivery"""
        return f"https://res.cloudinary.com/{cloudinary.config().cloud_name}"
