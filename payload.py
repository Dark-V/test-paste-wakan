import os

def generate_folder_structure(base_path, blacklist=None):
    folder_structure = {}
    for foldername, subfolders, filenames in os.walk(base_path):
        relative_path = os.path.relpath(foldername, base_path)
        
        # Check if the folder is in the blacklist
        if blacklist and any(item in relative_path.split(os.path.sep) for item in blacklist):
            continue
        
        if relative_path == ".":
            continue  # Skip the base folder itself
        files = [filename for filename in filenames if filename.endswith(".html")]
        folder_structure[relative_path] = files
    return folder_structure

def generate_html_file(folder_structure):
    def generate_folder_html(folder_name, files):
        folder_html = f'''
        <li class="folder-item">
            <span class="folder-name">{folder_name}</span>
            <ul class="file-list" style="display: none;">
        '''
        for file in files:
            folder_html += f'<li class="file-item" data-file="{folder_name}/{file}">{file}</li>'
        
        folder_html += '''
            </ul>
        </li>
        '''
        return folder_html
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>File List</title>
        <style>
            .folder-item {
                padding: 10px;
                border: 1px solid #ccc;
                cursor: pointer;
            }
            
            .folder-name {
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .file-item {
                padding: 5px;
                cursor: pointer;
            }
        
            #preview {
                max-width: 400px;
                overflow-wrap: break-word;
                word-wrap: break-word;
                white-space: pre-wrap;
            }
        </style>
        <script>
            function showPreview(file) {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", file, true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        document.getElementById("preview").innerHTML = xhr.responseText;
                    }
                };
                xhr.send();
            }
            
            function bindClickEvents() {
                var folderItems = document.getElementsByClassName("folder-item");
                for (var i = 0; i < folderItems.length; i++) {
                    folderItems[i].addEventListener("click", function() {
                        var fileList = this.getElementsByClassName("file-list")[0];
                        fileList.style.display = (fileList.style.display === "none") ? "block" : "none";
                    });
                }
                
                var fileItems = document.getElementsByClassName("file-item");
                for (var i = 0; i < fileItems.length; i++) {
                    fileItems[i].addEventListener("click", function(e) {
                        e.stopPropagation(); // Prevent folder toggle when clicking a file
                        showPreview(this.getAttribute("data-file"));
                    });
                }
            }
            
            window.addEventListener("DOMContentLoaded", bindClickEvents);
        </script>
    </head>
    <body>
        <h1>File List</h1>
        <ul class="folder-list">
    '''
    for folder, files in folder_structure.items():
        html += generate_folder_html(folder, files)
    
    html += '''
        </ul>
        <div id="preview"></div>
    </body>
    </html>
    '''
    return html

# Define the base path where the Python script is located
base_path = r"C:\Users\DarkV\Desktop\simple-page-main"

# Define the folders to exclude from the folder structure
blacklist = [".git"]  # Add the folders you want to exclude

# Generate the folder structure
folder_structure = generate_folder_structure(base_path, blacklist)

# Generate the HTML content
html_content = generate_html_file(folder_structure)

# Write the HTML content to a file
with open("file_list.html", "w") as file:
    file.write(html_content)
