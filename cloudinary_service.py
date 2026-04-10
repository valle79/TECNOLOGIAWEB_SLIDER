"""
Cloudinary service for image management
Handles upload, delete, and URL generation for wine images
"""
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
import logging
from typing import Optional, Dict, Tuple
import os
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

# Constants
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
CLOUDINARY_FOLDER = 'wines'  # Folder in Cloudinary to organize images
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def is_allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file to check
        
    Returns:
        bool: True if file is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image_file(file) -> Tuple[bool, Optional[str]]:
    """
    Validate image file before upload
    
    Args:
        file: FileStorage object from request.files
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if file exists
    if not file or file.filename == '':
        return False, "No file selected"
    
    # Check file extension
    if not is_allowed_file(file.filename):
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: 16MB"
    
    # Validate it's actually an image
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
        return True, None
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def upload_wine_image(file, wine_name: str = None, 
                     auto_optimize: bool = True) -> Optional[Dict]:
    """
    Upload wine image to Cloudinary
    
    Args:
        file: FileStorage object from request.files
        wine_name: Optional wine name for organizing images
        auto_optimize: Whether to automatically optimize image
        
    Returns:
        Dictionary with upload result or None if failed:
        {
            'url': 'https://res.cloudinary.com/...',
            'secure_url': 'https://...',
            'public_id': 'wines/abc123',
            'width': 1200,
            'height': 800,
            'format': 'jpg'
        }
    """
    
    # Validate file
    is_valid, error_msg = validate_image_file(file)
    if not is_valid:
        logger.warning(f"Image validation failed: {error_msg}")
        return None
    
    try:
        # Prepare upload options
        upload_options = {
            'folder': CLOUDINARY_FOLDER,
            'resource_type': 'auto',
            'quality': 'auto',
            'transformation': []
        }
        
        # Add wine name as public_id prefix if provided
        if wine_name:
            # Sanitize wine name
            sanitized_name = secure_filename(wine_name.lower())[:30]
            upload_options['public_id'] = f"{sanitized_name}_{int(__import__('time').time())}"
        
        # Auto-optimize image
        if auto_optimize:
            upload_options['transformation'].append({
                'quality': 'auto:good',
                'fetch_format': 'auto',
                'width': 1200,
                'height': 800,
                'crop': 'fill',
                'gravity': 'auto'
            })
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            **upload_options
        )
        
        logger.info(f"Image uploaded successfully: {result['public_id']}")
        
        return {
            'url': result['url'],
            'secure_url': result['secure_url'],
            'public_id': result['public_id'],
            'width': result.get('width'),
            'height': result.get('height'),
            'format': result.get('format')
        }
        
    except Exception as e:
        logger.error(f"Error uploading image to Cloudinary: {str(e)}")
        return None


def delete_wine_image(public_id: str) -> bool:
    """
    Delete wine image from Cloudinary
    
    Args:
        public_id: Public ID of image in Cloudinary (e.g., 'wines/abc123')
        
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    if not public_id:
        return False
    
    try:
        result = cloudinary.uploader.destroy(public_id)
        
        if result.get('result') == 'ok':
            logger.info(f"Image deleted from Cloudinary: {public_id}")
            return True
        else:
            logger.warning(f"Unexpected result deleting {public_id}: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Error deleting image from Cloudinary: {str(e)}")
        return False


def get_optimized_url(public_id: str, width: int = None, 
                      height: int = None, quality: str = 'auto') -> str:
    """
    Generate optimized image URL with transformations
    
    Args:
        public_id: Public ID of image in Cloudinary
        width: Width in pixels (optional)
        height: Height in pixels (optional)
        quality: Quality setting ('auto', 'high', 'low')
        
    Returns:
        str: Optimized image URL
        
    Example:
        >>> url = get_optimized_url('wines/chardonnay_123', width=400, height=300)
        >>> # Returns: https://res.cloudinary.com/.../w_400,h_300,q_auto/wines/chardonnay_123.jpg
    """
    try:
        transformations = []
        
        if width or height:
            t = {}
            if width:
                t['width'] = width
            if height:
                t['height'] = height
            t['crop'] = 'fill'
            t['gravity'] = 'auto'
            transformations.append(t)
        
        if quality and quality != 'auto':
            transformations.append({'quality': quality})
        elif quality == 'auto':
            transformations.append({'quality': 'auto'})
        
        url, _ = cloudinary_url(
            public_id,
            transformations=transformations,
            secure=True,
            fetch_format='auto'
        )
        
        return url
        
    except Exception as e:
        logger.error(f"Error generating optimized URL: {str(e)}")
        return None


def get_thumbnail_url(public_id: str) -> str:
    """
    Generate thumbnail URL for wine images
    
    Args:
        public_id: Public ID of image in Cloudinary
        
    Returns:
        str: Thumbnail URL (400x300)
    """
    return get_optimized_url(public_id, width=400, height=300, quality='auto')


def extract_public_id_from_url(cloudinary_url_str: str) -> Optional[str]:
    """
    Extract public_id from Cloudinary URL
    
    Args:
        cloudinary_url_str: Full Cloudinary URL
        
    Returns:
        str: Public ID or None if invalid URL
        
    Example:
        >>> extract_public_id_from_url('https://res.cloudinary.com/mycloud/image/upload/wines/abc123.jpg')
        >>> # Returns: 'wines/abc123'
    """
    try:
        if 'res.cloudinary.com' not in cloudinary_url_str:
            return None
        
        # Extract the part after /upload/
        parts = cloudinary_url_str.split('/upload/')
        if len(parts) == 2:
            # Remove query parameters and file extension handling
            path = parts[1]
            # Remove file extension
            if '.' in path:
                path = path.rsplit('.', 1)[0]
            return path
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting public_id: {str(e)}")
        return None


def health_check() -> bool:
    """
    Check Cloudinary connection and credentials
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        cloudinary.api.resources(max_results=1)
        logger.info("Cloudinary health check passed")
        return True
    except Exception as e:
        logger.error(f"Cloudinary health check failed: {str(e)}")
        return False
