import modules.scripts as scripts
import gradio as gr
import os

from modules import script_callbacks

def calculate(a, b, operation):
    try:
        if operation == "Tambah":
            return a + b
        elif operation == "Kurang":
            return a - b
        elif operation == "Kali":
            return a * b
        elif operation == "Bagi":
            return a / b if b != 0 else "Error: Pembagian dengan nol"
    except Exception as e:
        return f"Error: {str(e)}"

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            with gr.Column():
                num1 = gr.Number(value=0, label="Angka 1")
                num2 = gr.Number(value=0, label="Angka 2")
                operation = gr.Radio(
                    ["Tambah", "Kurang", "Kali", "Bagi"], 
                    label="Operasi",
                    value="Tambah"
                )
                result = gr.Textbox(label="Hasil")
                calc_button = gr.Button("Hitung")

                calc_button.click(
                    fn=calculate, 
                    inputs=[num1, num2, operation], 
                    outputs=[result]
                )

    return [(ui_component, "Kalkulator", "calculator_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
