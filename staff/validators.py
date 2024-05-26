import os
from typing import List
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_types(file, allowed_types:List[str]):
    """
    example for allowed_types: ['.pdf', '.docx', '.png', '.jpg', '.doc']
    """
    file_type = os.path.splitext(file.name)[1].lower()
    if file_type not in allowed_types:
        error_msg = _("File turlari quyidagilardan biri bo'lishligi kerak {allowed_types}").format(allowed_types=allowed_types)
        raise ValidationError(error_msg)


def validate_file_size(file, max_size:float):
    """max_size should be in MB"""
    max_size *= 1024**2
    if file.size > max_size:
        error_msg = _("Filening maksimal hajmi {max_size} MB bo'lishligi kerak. Lekin sizning faylingiz hajmi {file_size}").format(max_size=max_size, file_size=file.size)
        raise ValidationError(error_msg)


def validate_file(file, allowed_types:List[str], max_size:float=2):
    """
    Validate both file type and size.
    :param file: The uploaded file
    :param allowed_types: List of allowed file extensions (e.g., ['.pdf', '.docx', '.png', '.jpg', '.doc'])
    :param max_size: Maximum file size in MB
    """
    validate_file_types(file, allowed_types)
    validate_file_size(file, max_size)