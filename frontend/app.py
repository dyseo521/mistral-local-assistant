import gradio as gr  # Gradio UI 라이브러리 임포트
import requests     # HTTP 요청을 위한 라이브러리
from pathlib import Path  # 파일 경로 처리를 위한 라이브러리

# FastAPI 백엔드 서버 주소
API_URL = "http://localhost:8000"

def generate_response(prompt, template):
    """
    사용자 입력을 받아 AI 응답을 생성하는 함수
    
    Args:
        prompt (str): 사용자 입력 텍스트
        template (str): 사용할 프롬프트 템플릿 유형
    
    Returns:
        str: AI 모델의 응답 텍스트
    """
    response = requests.post(
        f"{API_URL}/api/generate",
        json={"prompt": prompt, "template": template}
    )
    return response.json()["response"]

def load_chat_history():
    """
    저장된 대화 기록을 불러오는 함수
    
    Returns:
        str: 포맷팅된 대화 기록 또는 에러 메시지
    """
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

# Gradio UI 구성
with gr.Blocks(theme=gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="slate",
)) as demo:
    # 제목 설정
    gr.Markdown("# 🤖 오픈ㅡ소스 AI 어시스턴트")
    
    # 대화하기 탭
    with gr.Tab("대화하기"):
        with gr.Row():
            # 왼쪽 컬럼: 입력 영역
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
            
            # 오른쪽 컬럼: 출력 영역
            with gr.Column(scale=4):
                output = gr.Textbox(
                    label="AI 응답",
                    lines=10,
                    show_copy_button=True  # 복사 버튼 표시
                )
    
    # 대화 기록 탭
    with gr.Tab("대화 기록"):
        history_output = gr.Textbox(
            label="이전 대화 기록",
            lines=20,
            value=load_chat_history()
        )
        refresh_btn = gr.Button("새로고침")

    # 이벤트 핸들러 설정
    submit_btn.click(  # 전송 버튼 클릭 시
        generate_response,
        inputs=[prompt_input, template_select],
        outputs=output
    )
    
    refresh_btn.click(  # 새로고침 버튼 클릭 시
        load_chat_history,
        outputs=history_output
    )

# 메인 실행 부분
if __name__ == "__main__":
    demo.queue().launch(
        share=False,    # 외부 공유 비활성화
        show_api=None   # API 문서 비활성화
    )