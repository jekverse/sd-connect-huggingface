import modules.scripts as scripts
import gradio as gr
import os

from modules import script_callbacks

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            # Input fields
            num1 = gr.Number(label="Number 1", value=0)
            num2 = gr.Number(label="Number 2", value=0)
        with gr.Row():
            # Operation buttons
            add_btn = gr.Button("Add")
            subtract_btn = gr.Button("Subtract")
            multiply_btn = gr.Button("Multiply")
            divide_btn = gr.Button("Divide")
        with gr.Row():
            # Output field
            result = gr.Textbox(label="Result")

        def calculate(op, a, b):
            try:
                a, b = float(a), float(b)
                if op == "add":
                    return a + b
                elif op == "subtract":
                    return a - b
                elif op == "multiply":
                    return a * b
                elif op == "divide":
                    return a / b if b != 0 else "Error: Division by zero"
            except ValueError:
                return "Error: Invalid input"

        # Event handling
        add_btn.click(fn=lambda: calculate("add", num1.value, num2.value), inputs=[], outputs=result)
        subtract_btn.click(fn=lambda: calculate("subtract", num1.value, num2.value), inputs=[], outputs=result)
        multiply_btn.click(fn=lambda: calculate("multiply", num1.value, num2.value), inputs=[], outputs=result)
        divide_btn.click(fn=lambda: calculate("divide", num1.value, num2.value), inputs=[], outputs=result)

        return [(ui_component, "Calculator", "calculator_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
