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
    if repo_type == "model":
        api.upload_file(path_or_fileobj=file_path, path_in_repo=os.path.basename(file_path), repo_id=repo_id, repo_type="model")
    elif repo_type == "dataset":
        api.upload_file(path_or_fileobj=file_path, path_in_repo=os.path.basename(file_path), repo_id=repo_id, repo_type="dataset")

# Fungsi handler untuk Watchdog
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, token, repo_type, repo_id):
        self.token = token
        self.repo_type = repo_type
        self.repo_id = repo_id
    
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            if event.src_path.endswith('.tmp'):
                # Jika file berformat .tmp, tunggu beberapa detik lalu periksa apakah file telah berubah menjadi .png
                time.sleep(3)
                new_file_path = event.src_path.replace('.tmp', '.png')
                if os.path.exists(new_file_path):
                    print(f"File {new_file_path} detected after renaming from .tmp to .png")
                    upload_to_huggingface(new_file_path, self.token, self.repo_type, self.repo_id)
                else:
                    print(f"File {event.src_path} did not change to .png")
            elif event.src_path.endswith('.png'):
                upload_to_huggingface(event.src_path, self.token, self.repo_type, self.repo_id)

def start_watcher(directory, token, repo_type, repo_id):
    event_handler = WatcherHandler(token, repo_type, repo_id)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_monitoring(directory, token, repo_type, repo_id):
    thread = threading.Thread(target=start_watcher, args=(directory, token, repo_type, repo_id))
    thread.daemon = True
    thread.start()
    return f"Monitoring started for directory {directory}."

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            directory_input = gr.Textbox(label="Directory to Monitor", placeholder="Enter the directory path")
            token_input = gr.Textbox(label="Hugging Face Token", type="password")
            repo_type_input = gr.Radio(["model", "dataset"], label="Repository Type")
            repo_id_input = gr.Textbox(label="Repository ID")
            start_button = gr.Button("Start Monitoring")
        
        output_text = gr.Textbox(label="Status", interactive=False)
        
        start_button.click(
            start_monitoring,
            inputs=[directory_input, token_input, repo_type_input, repo_id_input],
            outputs=[output_text]
        )
    
    return [(ui_component, "Hugging Face Uploader", "huggingface_uploader_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
