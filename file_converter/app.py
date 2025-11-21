from flask import Flask, render_template, request, send_file
import pypandoc
import os
from werkzeug.utils import secure_filename

pypandoc.download_pandoc()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        target_format = request.form['format']

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(input_path)

            output_filename = os.path.splitext(filename)[0] + f".{target_format}"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)

            try:
                pypandoc.convert_file(input_path, target_format, outputfile=output_path, extra_args=['--standalone'])
                return send_file(output_path, as_attachment=True)
            except Exception as e:
                return f"Conversion failed: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
