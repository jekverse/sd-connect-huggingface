import modules.scripts as scripts
import gradio as gr
import os
import requests

from modules import images, script_callbacks
from modules.processing import process_images, Processed
from modules.shared import opts, cmd_opts, state

class HuggingFaceAutoUploadScript(scripts.Script):
    def __init__(self):
        self.output_folder = "outputs"  # Folder to monitor
        self.hf_token = "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"
        self.hf_repo_id = "oookto/package"
        self.last_seen_files = set(os.listdir(self.output_folder))

    def title(self):
        return "Hugging Face Auto Upload"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion('Hugging Face Auto Upload', open=False):
            with gr.Row():
                angle = gr.Slider(
                    minimum=0.0,
                    maximum=360.0,
                    step=1,
                    value=0,
                    label="Angle"
                )
                checkbox = gr.Checkbox(
                    False,
                    label="Enable Auto Upload"
                )
        return [angle, checkbox]

    def run(self, p, angle, checkbox):
        proc = process_images(p)
        if checkbox:
            self.upload_new_images()
        return proc

    def upload_new_images(self):
        current_files = set(os.listdir(self.output_folder))
        new_files = current_files - self.last_seen_files

        for file_name in new_files:
            file_path = os.path.join(self.output_folder, file_name)
            if os.path.isfile(file_path) and file_path.endswith(('.png', '.jpg', '.jpeg')):
                self.upload_to_huggingface(file_path)

        self.last_seen_files = current_files

    def upload_to_huggingface(self, file_path):
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"https://huggingface.co/api/{self.hf_repo_id}/upload",
                headers={"Authorization": f"Bearer {self.hf_token}"},
                files={"file": f}
            )
            if response.status_code == 200:
                print(f"Successfully uploaded {file_path} to Hugging Face.")
            else:
                print(f"Failed to upload {file_path} to Hugging Face. Status code: {response.status_code}")

script_callbacks.on_ui_tabs(HuggingFaceAutoUploadScript)
