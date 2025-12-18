import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Папка для загрузки
UPLOAD_FOLDER = 'static/iMAGE'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Какие файлы можно загружать
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_images():
    """Получить все изображения из папки"""
    images = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath) and allowed_file(filename):
                images.append({
                    'name': filename,
                    'path': f'iMAGE/{filename}',
                    'size': os.path.getsize(filepath)
                })
    # Сортируем по имени
    images.sort(key=lambda x: x['name'])
    return images


@app.route('/')
def home():
    images = get_images()
    return render_template('index.html', images=images)


@app.route('/upload', methods=['POST'])
def upload():
    """Загрузка изображений"""
    # Проверяем файлы
    if 'files[]' not in request.files:
        return redirect('/')

    files = request.files.getlist('files[]')

    # Создаем папку если нет
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Сохраняем каждый файл
    uploaded = 0
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Если файл с таким именем уже есть - добавляем номер
            counter = 1
            original_name, ext = os.path.splitext(filename)
            while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                filename = f"{original_name}_{counter}{ext}"
                counter += 1

            file.save(os.path.join(UPLOAD_FOLDER, filename))
            uploaded += 1

    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    """Удалить изображение"""
    filename = request.form.get('filename')
    if filename:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    return redirect('/')


if __name__ == '__main__':
    # Создаем папку для загрузок при запуске
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)