import cv2
from flask import Flask, render_template, request, jsonify
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def water_effect(img):
    n_img = np.zeros((img.shape[0] * 2, img.shape[1], img.shape[2]), np.uint8)
    n_img[:img.shape[0], :, :] = img[::1, :, :]
    n_img[img.shape[0]:, :, :] = img[::-1, :, :]
    return n_img


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    img_data = data.get('image')
    action = data.get('action')
    if not img_data:
        return jsonify({'error': 'No image provided'}), 400
    # 解码图片
    header, encoded = img_data.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    # 简单处理：三种按钮分别做不同处理
    if action == 'water_effect':
        img = water_effect(img)
    elif action == 'flip':
        # img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img = img.convert('L').convert('RGB')
    elif action == 'blur':
        # img = img.filter(Image.BLUR)
        img = img.convert('L').convert('RGB')

    #编码为JPG字节流
    success, encoded_img = cv2.imencode('.jpg', img)
    if not success:
        raise ValueError("图片编码失败")
    # 如果你只需要返回 BytesIO 对象给其他代码用：
    buf = io.BytesIO(encoded_img.tobytes())
    processed_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.seek(0)  # 可选：指针归零

    return jsonify({'image': f'data:image/png;base64,{processed_img}'})

if __name__ == '__main__':
    app.run(debug=True)
