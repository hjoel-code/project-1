"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from tokenize import String
from app import app, db
from flask import render_template, request, redirect, send_from_directory, url_for, flash

from app.foms import AddPropertyForm
from app.models import Property
import locale
from decimal import Decimal


from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


def saveImage(files, key):
    try :
        image = files[key]
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
        
    except Exception as e : 
        print(e)
        return None


@app.route('/properties/create', methods=['GET', 'POST'])
def createProperty():
    data = request.form.copy()
    data.update(request.files)
    
    form = AddPropertyForm(data)
    
    if (request.method == 'POST'):
        if (form.validate_on_submit()):
            filename = saveImage(request.files, form.propertyImage.name)
            print(filename)
            property = Property(
                form.title.data,
                form.rooms.data,
                form.baths.data,
                form.location.data,
                form.price.data,
                form.propertyType.data,
                form.description.data,
                filename
            )
            
            db.session.add(property)
            db.session.commit()
            
            flash('New Property Registered', 'success')
            return redirect(url_for('properties'))
        
        flash('Something went wrong', 'error')
    return render_template('create-property.html', form=form)



def formatCurrency(amt: String):
    locale.setlocale( locale.LC_ALL, 'en_US' )
    value = Decimal(amt)
    return locale.currency(value, grouping=True)


@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties = properties, formatCurrency = formatCurrency)


@app.route('/property/<propertyid>')
def property(propertyid):
    property = Property.query.filter_by(id=propertyid).first()
    return render_template('property.html', property = property, formatCurrency = formatCurrency)


def get_uploaded_image():
    rootdir = os.getcwd()
    
    images = []
    
    for subdir, dirs, files in os.walk(rootdir + app.config['UPLOAD_FOLDER']):
        for file in files:
            if (file.endswith(('png', 'jpg', 'jpeg'))):
                images.append(file)
                
    return images


@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)




###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
