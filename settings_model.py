"""
Site Settings Model
"""
from typing import Dict, Optional, List
from database import Database
import logging

logger = logging.getLogger(__name__)


class SiteSettings:
    """Site Settings model for configuration management"""

    @staticmethod
    def get_all() -> Dict[str, str]:
        """Get all settings as a dictionary"""
        query = """
            SELECT setting_key, setting_value, setting_type, description
            FROM site_settings
            ORDER BY setting_key
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Convert to dictionary
                settings = {}
                for row in results:
                    key = row['setting_key']
                    value = row['setting_value']
                    setting_type = row['setting_type']
                    
                    # Convert value based on type
                    if setting_type == 'boolean':
                        settings[key] = value == '1' or value.lower() == 'true'
                    elif setting_type == 'number':
                        try:
                            settings[key] = float(value) if '.' in value else int(value)
                        except:
                            settings[key] = value
                    else:
                        settings[key] = value
                
                return settings
        except Exception as e:
            logger.error(f"Error fetching settings: {e}")
            return {}

    @staticmethod
    def get(setting_key: str, default: str = None) -> Optional[str]:
        """Get a specific setting value"""
        query = """
            SELECT setting_value, setting_type
            FROM site_settings
            WHERE setting_key = %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (setting_key,))
                result = cursor.fetchone()
                
                if not result:
                    return default
                
                value = result['setting_value']
                setting_type = result['setting_type']
                
                # Convert value based on type
                if setting_type == 'boolean':
                    return value == '1' or value.lower() == 'true'
                elif setting_type == 'number':
                    try:
                        return float(value) if '.' in value else int(value)
                    except:
                        return value
                
                return value
        except Exception as e:
            logger.error(f"Error fetching setting {setting_key}: {e}")
            return default

    @staticmethod
    def update(setting_key: str, setting_value: str) -> bool:
        """Update a setting value"""
        query = """
            UPDATE site_settings
            SET setting_value = %s
            WHERE setting_key = %s
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query, (str(setting_value), setting_key))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating setting {setting_key}: {e}")
            return False

    @staticmethod
    def update_multiple(settings: Dict[str, str]) -> bool:
        """Update multiple settings at once"""
        query = """
            UPDATE site_settings
            SET setting_value = %s
            WHERE setting_key = %s
        """

        try:
            with Database.get_cursor() as cursor:
                for key, value in settings.items():
                    cursor.execute(query, (str(value), key))
                return True
        except Exception as e:
            logger.error(f"Error updating multiple settings: {e}")
            return False

    @staticmethod
    def get_by_category() -> Dict[str, List[Dict]]:
        """Get settings grouped by category"""
        all_settings = SiteSettings.get_all_detailed()
        
        categories = {
            'appearance': [],
            'site_info': [],
            'shipping': [],
            'notifications': [],
            'catalog': [],
            'financial': []
        }
        
        # Categorize settings
        for setting in all_settings:
            key = setting['setting_key']
            
            if 'theme' in key or 'color' in key:
                categories['appearance'].append(setting)
            elif 'site_' in key:
                categories['site_info'].append(setting)
            elif 'shipping' in key:
                categories['shipping'].append(setting)
            elif 'notification' in key or 'alert' in key:
                categories['notifications'].append(setting)
            elif 'products' in key or 'stock' in key:
                categories['catalog'].append(setting)
            elif 'currency' in key or 'tax' in key:
                categories['financial'].append(setting)
        
        return categories

    @staticmethod
    def get_all_detailed() -> List[Dict]:
        """Get all settings with full details"""
        query = """
            SELECT setting_key, setting_value, setting_type, description, updated_at
            FROM site_settings
            ORDER BY setting_key
        """

        try:
            with Database.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching detailed settings: {e}")
            return []
