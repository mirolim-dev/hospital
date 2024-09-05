from django.core.exceptions import ValidationError

def validate_image_size(image):
    #set limit for 5 mb
    limit = 5*1024*1024
    if image.size > limit:
        raise ValidationError("Image size shouldn't be more then 5 mb.\nCUrrent file size is {} mb".format(image.size))
    

def validate_image_type(image):
    file_type = image.name.split('.')[-1]
    valid_file_types = ['.pbg', '.jpg', '.jpeg']
    if file_type not in valid_file_types:
        raise ValidationError("Image's type should be one of these: [.png, .jpg, .jpeg]. \n\
                              Your current file type is {}".format(file_type))
    
def validate_image(image):
    validate_image_type(image)
    validate_image_size(image)
