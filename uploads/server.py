from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory, abort
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath("../output")  # Set your base directory
PASSWORD = "xyz"

# Ensure the base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# HTML templates
login_template = '''
<!doctype html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h2 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h2>Login</h2>
    <form method="post" action="{{ url_for('login') }}">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <input type="submit" value="Login">
    </form>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

index_template = '''
<!doctype html>
<html>
<head>
    <title>Files</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h2 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h2>Files in {{ current_dir }}</h2>
    <ul>
        {% if parent_dir %}
            <li><a href="{{ url_for('file_list', path=parent_dir) }}">.. (Up one level)</a></li>
        {% endif %}
        {% for file in files %}
            <li><a href="{{ url_for('file_list', path=file['path']) }}">{{ file['name'] }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(login_template)

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == PASSWORD:
        return redirect(url_for('file_list'))
    else:
        return render_template_string(login_template, error="Invalid password")

@app.route('/files', defaults={'path': ''})
@app.route('/files/<path:path>')
def file_list(path):
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    # Check if the requested path is within the BASE_DIR
    if not full_path.startswith(BASE_DIR):
        abort(403)
    if not os.path.exists(full_path):
        abort(404)
    if os.path.isfile(full_path):
        return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path))
    files = []
    for file in os.listdir(full_path):
        file_path = os.path.join(full_path, file)
        if os.path.isdir(file_path):
            files.append({'name': file + '/', 'path': os.path.relpath(file_path, BASE_DIR)})
        else:
            files.append({'name': file, 'path': os.path.relpath(file_path, BASE_DIR)})
    parent_dir = os.path.relpath(os.path.join(full_path, '..'), BASE_DIR) if path else None
    if parent_dir == '.':
        parent_dir = None
    return render_template_string(index_template, files=files, current_dir=path or 'Base Directory', parent_dir=parent_dir)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8111)

