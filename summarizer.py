from transformers import pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_form(data):
    text = f"Patient: {data['name']}, Age: {data['age']}, Symptoms: {data['symptoms']}, Duration: {data['duration']}."
    summary = summarizer(text, max_length=50, min_length=10, do_sample=False)
    return summary[0]['summary_text']