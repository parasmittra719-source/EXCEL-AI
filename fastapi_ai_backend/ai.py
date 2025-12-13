import openai
openai.api_key = "YOUR_OPENAI_KEY"

def generate_insight(data):
    prompt = f"""
    Analyze this data and give business insights:
    {data}
    """
    res = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content
