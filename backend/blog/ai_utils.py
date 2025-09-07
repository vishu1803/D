from transformers import pipeline

# Load model once (global) so it doesn’t reload on every request
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",  # specify model
    revision="a4f8f3e",
    device=-1  # -1 for CPU, 0 for GPU
)

def generate_summary(text):
    """
    Summarize given text using BART summarizer.
    """
    if not text:
        return ""
    
    # Hugging Face models have length limits, so keep input reasonable
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
