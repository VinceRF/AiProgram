import openai

openai.api_key = 'YOUR-API-KEY'


def ask_to_gpt_35_turbo(user_input):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        top_p=0.1,
        temperature=0.1,
        messages=[
            {"role": "system", "content": "You are helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content


users_request = '''
테스트 해보는거야
'''

r = ask_to_gpt_35_turbo(users_request)
print(r)


