import openai

openai.api_key = 'YOUR-API-KEY'

#OpenAI 챗봇 모델에 메세지를 보내고 응답하는 함수
def send_message(message_log):
    # OpenAi의 ChatCompletion API를 사용해 챗봇의 응답 얻기
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        message=message_log,
        temperature=0.5
    )

    #텍스트가 포함된 챗봇의 첫 번째 응답 찾기(일부 응답에는 텍스트가 없을 수 있음)
    for choice in response.choices:
        if "text" in choice:
            return choice.text
        #텍스트가 포함된 응답이 없을 경우
        return response.choices[0].message.content

def main():
    #챗봇에서 받은 메세지로 대화 기록 초기화
    message_log=[
        {"role":"system","content":"You are a helpful assistant."}
    ]

    #quit를 입력할 때까지 실행되는 루프
    while True:
        #터미널에서 입력
        user_input = input("You: ")

        #quit 입력 시 종료 및 종료 메세지 출력
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        #input을 대화 기록(message_log)에 추가
        message_log.append({"role":"user","content":user_input})

        #챗봇에게 대화기록 전송 및 응답 받기
        response = send_message(message_log)

        #대화 기록에 챗봇의 응답을 추가 및 콘솔에 출력
        message_log.append({"role":"system","content":response})
        print(f"assistant: {response}")

if __name__ == "__main__":
    main()