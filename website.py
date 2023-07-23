import numpy as np
from PIL import Image
from flask import Flask, request, redirect, url_for,render_template
import os

def allowed_file(filename):
    '''if there is "." in file name and file type is in allowed_extensions return True'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_html(colors):
    '''get rgb a list of rbg code as argument and return a paragraph to use in html page'''

    most_color_list = ''
    num = 0
    for color in colors:
        num += 1
        to_tuple = f'{color[0]},{color[1]},{color[2]}'
        most_color_list += f"<p class='result-text' style='background-color:rgb({to_tuple});'> {num}. rgb({to_tuple}) </p><br>"
    return most_color_list

def resize_image(image):
    '''if height or width of an image was grater than given number, function resize it and return image
    if both of width and height was less than spcefic number, the function doesn't change image and return original image'''

    ratio = int(image.width) / int(image.height)
    resized = image

    if image.height > 500:
        new_height = 500
        new_width = int(new_height * ratio)
        resized = image.resize((new_width,new_height))
    if image.width > 500:
        new_width = 500
        new_height = int(new_width * ratio)
        resized = image.resize((new_width,new_height))

    resized_image = resized
    return resized_image

def count_colors(image):
    '''function get image as an argument and turn it to an array then sort unique color of array,
    count frequency of element and return top 5 element with most frequency'''

    img_arr = np.array(image)
    count_uniqe_color = np.unique(img_arr.reshape(-1, img_arr.shape[-1]),axis=0, return_counts=True)
    color = count_uniqe_color[0]
    frequency = count_uniqe_color[1]
    sorted_freq_ind = np.argsort(frequency)
    most_color = color[sorted_freq_ind][::-3000]
    return most_color[:5]


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/",methods=['POST','GET'])
def upload_file():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        if file.filename == '':
            error ='please first select your file'
        
        elif not allowed_file(file.filename):
            error ="only support png, jpg and jpeg files"
        else:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            user_image = Image.open('static/uploads/'+file.filename)
            img = resize_image(user_image)
            most_color = count_colors(img)
            paragraphs = generate_html(most_color)
            return render_template('index.html',file = f'static/uploads/{file.filename}',paragraphs=paragraphs)
   
    #color of defualt and sample iamge of the color picker tool
    most_color = np.array([[21, 22, 26],[20, 26, 29],[97, 100, 107],[34, 42, 54],[209, 205, 184]])
    paragraphs = generate_html(most_color)
    return render_template('index.html',file = "static/images/sample-image2.webp",paragraphs=paragraphs,error=error)

if __name__ == "__main__":
    app.run(host="localhost",port=8080,debug=True)