from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="give me the code for fibonacci series"
)

# Print to console
print(response.output_text)

# Write the response to a file
with open("fibonacci_code.txt", "w") as file:
    file.write(response.output_text)
    