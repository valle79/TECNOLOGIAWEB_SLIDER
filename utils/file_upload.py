"""
File upload utilities
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_wine_image(file):
    """
    Save uploaded wine image
    
    Args:
        file: FileStorage object from request.files
        
    Returns:
        str: URL path to saved image, or None if error
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        logger.error(f"File type not allowed: {file.filename}")
        return None
    
    try:
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        # Ensure upload directory exists
        upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'wines')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Return URL path
        return f"/static/images/wines/{filename}"
        
    except Exception as e:
        logger.error(f"Error saving wine image: {e}")
        return None


def delete_wine_image(image_url):
    """
    Delete wine image file
    
    Args:
        image_url: URL path to image (e.g., /static/images/wines/abc123.jpg)
        
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    if not image_url or not image_url.startswith('/static/images/wines/'):
        return False
    
    try:
        # Extract filename from URL
        filename = image_url.split('/')[-1]
        filepath = os.path.join(current_app.root_path, 'static', 'images', 'wines', filename)
        
        # Delete file if it exists
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Deleted wine image: {filename}")
            return True
            
    except Exception as e:
        logger.error(f"Error deleting wine image: {e}")
    
    return False
