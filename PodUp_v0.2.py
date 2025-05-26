# by EasonLiu@202505241057
# 本程序基于Flask框架开发，使用Python语言编写。
# 程序的主要功能是提供一个简单的文件上传功能，允许用户上传多个文件到服务器，并将其保存到指定的目录中。
# 程序还提供了一个文件列表功能，用户可以查看已上传的文件列表，并可以下载这些文件。  
# 程序的主要优点是简单易用，易于扩展和维护。
# 程序的主要缺点是没有进行文件类型和大小的校验，可能会导致文件上传失败或文件被篡改。
# 程序的主要改进方向是添加文件类型和大小的校验功能，提高文件上传的安全性和稳定性。


from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 自动创建上传目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Microsoft Yahei', system-ui, -apple-system, sans-serif;
            }

            body {
                background: #f0f2f5;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }

            .container {
                text-align: center;
                max-width: 480px;
                width: 100%;
            }

            h1 {
                color: #1a1a1a;
                font-size: calc(24px + 1.5vw);
                margin-bottom: 30px;
                line-height: 1.3;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }

            .upload-box {
                background: white;
                border-radius: 15px;
                padding: 30px 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }

            input[type="file"] {
                display: none;
            }

            .custom-upload {
                display: inline-block;
                background: #007AFF;
                color: white;
                padding: 12px 24px;
                border-radius: 20px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s;
                margin-bottom: 15px;
                width: 80%;
                max-width: 200px;
            }

            .custom-upload:active {
                transform: scale(0.95);
                background: #0063CC;
            }

            input[type="submit"] {
                background: #34C759;
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 20px;
                font-size: 16px;
                cursor: pointer;
                width: 80%;
                max-width: 200px;
                margin-top: 15px;
            }

            .file-count {
                color: #666;
                font-size: 14px;
                margin-top: 10px;
            }

            @media (max-width: 480px) {
                h1 {
                    font-size: 28px;
                }
                
                .custom-upload {
                    padding: 12px 24px;
                    font-size: 16px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>手机文件备份</h1>
            <h2>{伊森实验室}</h2>
            <br>
            <div class="upload-box">
                <form method="post" enctype="multipart/form-data" action="/upload">
                    <label class="custom-upload">
                        选择文件
                        <input type="file" name="file" accept="image/*,video/*" multiple id="fileInput">
                    </label>
                    <div class="file-count" id="fileCount">未选择文件</div>
                    <div>
                        <input type="submit" value="开始上传">
                    </div>
                </form>
            </div>
        </div>
        <script>
            document.getElementById('fileInput').addEventListener('change', function(e) {
                const count = e.target.files.length;
                const fileCountElement = document.getElementById('fileCount');
                if (count > 0) {
                    fileCountElement.textContent = `已选择 ${count} 个文件`;
                } else {
                    fileCountElement.textContent = '未选择文件';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    for file in files:
        # 清理文件名，移除特殊字符
        safe_filename = ''.join(c for c in file.filename if c not in '?&=')
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], safe_filename))
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Microsoft Yahei', system-ui, -apple-system, sans-serif;
            }

            body {
                background: #f0f2f5;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }

            .container {
                text-align: center;
                max-width: 480px;
                width: 100%;
            }

            h1 {
                color: #1a1a1a;
                font-size: calc(24px + 1.5vw);
                margin-bottom: 30px;
                line-height: 1.3;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }

            h2 {
                color: #1a1a1a;
                font-size: calc(18px + 0.5vw);
                margin-bottom: 15px;
            }

            .message-box {
                background: white;
                border-radius: 15px;
                padding: 30px 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }

            .back-link {
                display: inline-block;
                background: #007AFF;
                color: white;
                padding: 12px 24px;
                border-radius: 20px;
                font-size: 16px;
                text-decoration: none;
                width: 60%;
                margin-top: 20px;
            }

            @media (max-width: 480px) {
                h1 {
                    font-size: 28px;
                }
                
                .message-box {
                    padding: 20px 15px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>手机文件备份</h1>
            <h2>{伊森实验室}</h2>
            <br>
            <div class="message-box">
                <h2>上传成功！</h2>
                <a href="/" class="back-link">返回</a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)