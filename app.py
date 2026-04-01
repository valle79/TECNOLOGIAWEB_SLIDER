"""
Flask Modern Slider Application

A modern, interactive slider built with Flask backend and HTML/Tailwind CSS/JavaScript frontend.
"""

from flask import Flask, render_template
from typing import List, Dict

app = Flask(__name__)

# Configure Flask application
app.config['DEBUG'] = True


# Slide data structure
slides_data: List[Dict[str, str]] = [
    {
        'image_url': '/static/images/slide1.jpg',
        'title': 'Discover Amazing Features',
        'description': 'Experience the next generation of web sliders with modern design and smooth animations',
        'button_text': 'Learn More'
    },
    {
        'image_url': '/static/images/slide2.jpg',
        'title': 'Responsive Design',
        'description': 'Works perfectly on all devices from mobile to desktop with adaptive controls',
        'button_text': 'Explore'
    },
    {
        'image_url': '/static/images/slide3.jpg',
        'title': 'Interactive Controls',
        'description': 'Navigate with mouse, keyboard, or touch gestures for maximum flexibility',
        'button_text': 'Try Now'
    },
    {
        'image_url': '/static/images/slide4.jpg',
        'title': 'Modern Aesthetics',
        'description': 'Beautiful glassmorphism effects and smooth transitions create a premium experience',
        'button_text': 'Get Started'
    }
]


def get_slides_data() -> List[Dict[str, str]]:
    """
    Provides validated slide data structure.
    
    Returns:
        List of slide dictionaries with keys:
        - image_url: str (path to image relative to static folder)
        - title: str (slide title)
        - description: str (slide description)
        - button_text: str (CTA button text)
    """
    # Validate that slides_data is not empty
    if not slides_data:
        return []
    
    # Validate each slide has all required fields
    required_fields = ['image_url', 'title', 'description', 'button_text']
    validated_slides = []
    
    for slide in slides_data:
        # Check if all required fields exist and are non-empty strings
        if all(
            field in slide and 
            isinstance(slide[field], str) and 
            slide[field].strip()
            for field in required_fields
        ):
            validated_slides.append(slide)
    
    return validated_slides


@app.route('/')
def index():
    """
    Main route that renders the slider page.
    
    Returns:
        Rendered HTML template for the slider
    """
    slides = get_slides_data()
    return render_template('index.html', slides=slides)


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
