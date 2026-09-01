"""
Configuration management for Document Merger.
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration management class."""

    # Default configuration
    DEFAULT_CONFIG = {
        'merge': {
            'output_format': 'pdf',  # 'pdf' or 'docx'
            'preserve_formatting': True,
            'page_numbering': True,
        },
        'toc': {
            'auto_generate': True,
            'auto_refresh': True,
            'max_depth': 3,
            'include_page_numbers': True,
            'style': 'formal',  # 'formal' or 'simple'
        },
        'pdf': {
            'add_bookmarks': True,
            'bookmark_style': 'hierarchical',
            'page_numbering': True,
        },
        'word': {
            'keep_styles': True,
            'merge_styles': True,
            'update_fields': True,
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to YAML configuration file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and Path(config_path).exists():
            self.load_config(config_path)

    def load_config(self, config_path: str) -> None:
        """Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    self._deep_update(self.config, yaml_config)
        except Exception as e:
            print(f"Error loading config file: {e}")
            print("Using default configuration")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation: 'merge.output_format')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
                
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value

    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> None:
        """Deep update dictionary with another dictionary.
        
        Args:
            base_dict: Base dictionary to update
            update_dict: Dictionary with updates
        """
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    def to_dict(self) -> Dict:
        """Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()

    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"Config({self.config})"
