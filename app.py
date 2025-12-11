from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    img = Image.open(io.BytesIO(img_bytes))
    # 简单处理：三种按钮分别做不同处理
    if action == 'gray':
        img = img.convert('L').convert('RGB')
    elif action == 'flip':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif action == 'blur':
        img = img.filter(Image.BLUR)
    # 返回处理后图片
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    processed_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    return jsonify({'image': f'data:image/png;base64,{processed_img}'})

if __name__ == '__main__':
    app.run(debug=True)
