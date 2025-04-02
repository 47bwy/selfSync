# -*- encoding: utf-8 -*-
'''
@Time    :   2024/08/28 15:11:05
@Author  :   47bwy
@Desc    :   None
'''

import os

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # 上传文件保存的目录
app.config['MAX_CONTENT_LENGTH'] = 5000 * 1024 * 1024  # 限制上传文件大小为16MB

# 确保上传文件目录存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f'File successfully uploaded to {filepath}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
