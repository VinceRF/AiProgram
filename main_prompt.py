import openai
import tkinter as tk
from tkinter import scrolledtext, Toplevel, Label

# OpenAI API 키 설정
openai.api_key = 'YOUR-API-KEY'


# OpenAI 챗봇과 대화하는 함수
def send_message(event=None):  # 엔터 키로 이벤트 처리
    user_input = entry.get()
    if not user_input.strip():
        return

    message_log.append({"role": "user", "content": user_input})
    entry.delete(0, tk.END)

    # 로딩 팝업 생성
    loading_popup = Toplevel(root)
    loading_popup.geometry("200x100")
    loading_popup.minsize(200, 100)  # Minimum size to prevent shrinking
    loading_popup.title("생각 중...")
    loading_popup_label = Label(loading_popup, text="생각 중...", font=("맑은 고딕", 12))
    loading_popup_label.pack(expand=True)
    loading_popup.update()

    # OpenAI 응답 요청
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_log,
        temperature=0.1
    )

    # 로딩 팝업 닫기
    loading_popup.destroy()

    bot_response = response.choices[0].message.content
    message_log.append({"role": "system", "content": bot_response})

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_input}\n", "user")
    chat_display.insert(tk.END, f"Assistant: {bot_response}\n\n", "assistant")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)


# GUI 설정
root = tk.Tk()
root.title("GPT Powered DJ")
root.geometry("1000x1000")
root.minsize(1000, 1000)  # 최소 창 크기 설정
root.option_add("*Font", ("맑은 고딕", 12))

message_log = [
    {
        "role": "system",
        "content": '''
    You are a DJ assistant who creates playlists. Your user will be Korean, so communicate in Korean, but you must not translate artists' names and song titles into Korean.
        - When you show a playlist, it must contains the title, artist, and release year of each song in a list format. You must ask the user if they want to save the playlist like this: "이 플레이리스트를 CSV로 저장하시겠습니까?"
        - If they want to save the playlist into CSV, show the playlist with a header in CSV format, separated by ';' and the release year format should be 'YYYY'. The CSV format must start with a new line. The header of the CSV file must be in English and it should be formatted as follows: 'Title;Artist;Released'.
    '''
    }
]

# 채팅창
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("맑은 고딕", 12), spacing1=5, spacing2=5, spacing3=5,
                                         state=tk.DISABLED)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.tag_config("user", foreground="blue", background="#e6f7ff")
chat_display.tag_config("assistant", foreground="green", background="#e6ffe6")

# 입력 필드 및 버튼
entry_frame = tk.Frame(root)
entry_frame.pack(pady=5, fill=tk.X)
entry = tk.Entry(entry_frame, font=("맑은 고딕", 14))
entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
send_button = tk.Button(entry_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=5)

# Enter 키로 메시지 전송
entry.bind("<Return>", send_message)  # 엔터 키로 질문 전송

# ESC 키로 GUI 종료
root.bind("<Escape>", lambda event: root.quit())  # ESC 키로 종료

# GUI 시작 시 input 박스에 포커스
entry.focus()

# 창 크기 조절 시 위젯 크기 유지
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)

# 메인 루프 실행
root.mainloop()
