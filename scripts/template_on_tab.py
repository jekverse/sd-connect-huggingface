import modules.scripts as scripts
import gradio as gr
import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from huggingface_hub import HfApi
from modules import script_callbacks

# Fungsi untuk mengupload file ke Hugging Face
def upload_to_huggingface(file_path, token, repo_type, repo_id):
    api = HfApi(token=token)
    filename = os.path.basename(file_path)  # Mendapatkan nama file
    if repo_type == "model":
        api.upload_file(path_or_fileobj=file_path, path_in_repo=filename, repo_id=repo_id, repo_type="model")
    elif repo_type == "dataset":
        api.upload_file(path_or_fileobj=file_path, path_in_repo=filename, repo_id=repo_id, repo_type="dataset")

# Fungsi untuk mengupload semua file dalam folder
def upload_folder(folder_path, token, repo_type, repo_id):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Uploading file: {file_path}")
            upload_to_huggingface(file_path, token, repo_type, repo_id)

# Fungsi handler untuk Watchdog
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, token, repo_type, repo_id):
        self.token = token
        self.repo_type = repo_type
        self.repo_id = repo_id
    
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            # Menambahkan jeda untuk memastikan file tersedia sepenuhnya
            time.sleep(2)
            # Upload file tanpa memeriksa ekstensi
            upload_to_huggingface(event.src_path, self.token, self.repo_type, self.repo_id)
        else:
            print(f"New folder detected: {event.src_path}")
            # Upload semua file dalam folder
            upload_folder(event.src_path, self.token, self.repo_type, self.repo_id)

def start_watcher(token, repo_type, repo_id):
    event_handler = WatcherHandler(token, repo_type, repo_id)
    observer = Observer()
    observer.schedule(event_handler, path='/kaggle/working/stable-diffusion-webui/outputs/txt2img-images/2024-08-06', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_monitoring(token, repo_type, repo_id):
    thread = threading.Thread(target=start_watcher, args=(token, repo_type, repo_id))
    thread.daemon = True
    thread.start()
    return "Monitoring started for directory /kaggle/working/stable-diffusion-webui/outputs/txt2img-images/2024-08-06."

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            token_input = gr.Textbox(label="Hugging Face Token", type="password")
            repo_type_input = gr.Radio(["model", "dataset"], label="Repository Type")
            repo_id_input = gr.Textbox(label="Repository ID")
            start_button = gr.Button("Start Monitoring")
        
        output_text = gr.Textbox(label="Status", interactive=False)
        
        start_button.click(
            start_monitoring,
            inputs=[token_input, repo_type_input, repo_id_input],
            outputs=[output_text]
        )
    
    return [(ui_component, "Hugging Face Uploader", "huggingface_uploader_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
