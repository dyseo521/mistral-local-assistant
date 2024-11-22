import gradio as gr
import requests
from pathlib import Path

API_URL = "http://localhost:8000"

def generate_response(prompt, template):
    response = requests.post(
        f"{API_URL}/api/generate",
        json={"prompt": prompt, "template": template}
    )
    return response.json()["response"]

def load_chat_history():
    try:
        response = requests.get(f"{API_URL}/api/history")
        history = response.json()
        formatted_history = ""
        for entry in history:
            formatted_history += f"시간: {entry['timestamp']}\n"
            formatted_history += f"질문: {entry['prompt']}\n"
            formatted_history += f"답변: {entry['response']}\n"
            formatted_history += "-" * 50 + "\n"
        return formatted_history if formatted_history else "대화 기록이 없습니다."
    except Exception as e:
        return f"대화 기록을 불러오는 중 오류가 발생했습니다: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="slate",
)) as demo:
    gr.Markdown("# 🤖 오픈ㅡ소스 AI 어시스턴트")
    
    with gr.Tab("대화하기"):
        with gr.Row():
            with gr.Column(scale=3):
                prompt_input = gr.Textbox(
                    label="질문을 입력하세요 ( 영어 권장 )",
                    placeholder="무엇이든 물어보세요...",
                    lines=3
                )
                template_select = gr.Dropdown(
                    choices=["default", "code", "analysis", "creative"],
                    value="default",
                    label="템플릿 선택"
                )
                submit_btn = gr.Button("전송", variant="primary")
            
            with gr.Column(scale=4):
                output = gr.Textbox(
                    label="AI 응답",
                    lines=10,
                    show_copy_button=True
                )
    
    with gr.Tab("대화 기록"):
        history_output = gr.Textbox(
            label="이전 대화 기록",
            lines=20,
            value=load_chat_history()
        )
        refresh_btn = gr.Button("새로고침")

    submit_btn.click(
        generate_response,
        inputs=[prompt_input, template_select],
        outputs=output
    )
    
    refresh_btn.click(
        load_chat_history,
        outputs=history_output
    )

if __name__ == "__main__":
    demo.queue().launch(
        share=False,
        show_api=None
    )