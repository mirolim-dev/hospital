import os
from typing import List
from django.core.exceptions import ValidationError

def validate_file_types(file, allowed_types:List[str]):
    """
    example for allowed_types: ['.pdf', '.docx', '.png', '.jpg', '.doc']
    """
    file_type = os.path.splitext(file.name)[1].lower()
    if file_type not in allowed_types:
        raise ValidationError(f"File turlari quyidagilardan biri bo'lishligi kerak\n{allowed_types}")


def validate_file_size(file, max_size:float):
    """max_size should be in MB"""
    max_size *= 1024**2
    if file.size > max_size:
        raise ValidationError(f"Filening maksimal hajmi {max_size} MB bo'lishligi kerak. Lekin sizning faylingiz hajmi {file.size}")


def validate_file(file, allowed_types:List[str], max_size:float=2):
    """
    Validate both file type and size.
    :param file: The uploaded file
    :param allowed_types: List of allowed file extensions (e.g., ['.pdf', '.docx', '.png', '.jpg', '.doc'])
    :param max_size: Maximum file size in MB
    """
    validate_file_types(file, allowed_types)
    validate_file_size(file, max_size)