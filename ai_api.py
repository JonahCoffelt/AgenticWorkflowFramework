from groq import Groq

user_input = input("Enter something to say: ")

API = ""
client = Groq(api_key=API)

while user_input:
    user_input = input()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama3-8b-8192",
    )
    print(chat_completion.choices[0].message.content)