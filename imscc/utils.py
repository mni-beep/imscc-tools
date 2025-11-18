"""Utility functions for IMSCC package."""

import uuid
import zipfile
import os
import re
from pathlib import Path
from typing import Optional


def generate_identifier(prefix: str = "g") -> str:
    """
    Generate a unique identifier for IMSCC resources.
    
    Args:
        prefix: Prefix for the identifier (default: 'g')
    
    Returns:
        A unique identifier string like 'gaad660d2e4344089643a13af565b974a'
    """
    # Generate UUID and remove hyphens to match Canvas format
    unique_id = uuid.uuid4().hex
    return f"{prefix}{unique_id}"


def extract_imscc(imscc_path: str, output_dir: str) -> None:
    """
    Extract an IMSCC file to a directory for inspection/templating.
    
    Args:
        imscc_path: Path to the .imscc file
        output_dir: Directory to extract to
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(imscc_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)
    
    print(f"Extracted {imscc_path} to {output_dir}")


def ensure_dir(path: str) -> None:
    """Ensure a directory exists, creating it if necessary."""
    Path(path).mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for file systems.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Replace spaces and special characters
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
    sanitized = "".join(c if c in safe_chars else "-" for c in filename)
    # Remove consecutive hyphens
    while "--" in sanitized:
        sanitized = sanitized.replace("--", "-")
    return sanitized.strip("-").lower()


def slugify(text: str) -> str:
    """
    Convert text to a Canvas-compatible slug.
    Canvas converts titles to lowercase, replaces spaces and special chars with hyphens.
    
    Args:
        text: Text to slugify
    
    Returns:
        Slugified text
    """
    # Convert to lowercase
    slug = text.lower()
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars except spaces and hyphens
    slug = re.sub(r'[-\s]+', '-', slug)    # Replace spaces and multiple hyphens with single hyphen
    slug = slug.strip('-')                  # Remove leading/trailing hyphens
    return slug
