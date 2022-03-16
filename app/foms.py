
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, IntegerField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired




class AddPropertyForm(FlaskForm):
    title = StringField(
        name='title', 
        label='Property Title', 
        # validators=[DataRequired()] 
    )
    
    rooms = IntegerField(
        name='bedrooms',
        label='Number of Bedrooms',
        # validators=[DataRequired()] 
    )
    
    baths = IntegerField(
        name='bathrooms',
        label='Number of Bathrooms',
        # validators=[DataRequired()] 
    )
    
    
    location = StringField(
        name='location',
        label='Property Location',
        # validators=[DataRequired()] 
    )
    
    
    price = StringField(
        name='price',
        label='Property Asking Price',
        # validators=[DataRequired()] 
    )
    
    propertyType = SelectField(
        name='type',
        label='Property Type',
        # validators=[DataRequired()],
        choices=['Residential', 'Commercial']
    )
    
    description = TextAreaField(
        name='description',
        label='Prperty Description'
    )
    
    propertyImage = FileField(
        name='image',
        label='Upload Property Images',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    
    