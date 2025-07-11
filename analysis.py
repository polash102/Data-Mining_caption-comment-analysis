import matplotlib.pyplot as plt
from collections import Counter
import os

# File paths (adjust if needed)
CAPTIONS_PATH = "data/captions.vtt.en.vtt"
COMMENTS_PATH = "data/comments.txt"

# Load captions
def load_vtt_captions(filepath=CAPTIONS_PATH):
    captions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '-->' not in line and line and not line.isdigit() and 'WEBVTT' not in line:
                captions.append(line)
    return captions

# Load comments
def load_raw_commentstxt(filepath=COMMENTS_PATH):
    comments = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0 and not line.endswith('ago') and not line.lower() == 'reply':
                comments.append(line)
    return comments

# TTR calculation
def type_token_ratio(lines):
    words = [word.lower() for line in lines for word in line.split()]
    unique = set(words)
    return len(unique) / len(words) if words else 0

# Top N frequent words (excluding stopwords)
stopwords = set([
    'the', 'and', 'a', 'is', 'in', 'to', 'of', 'that', 'it', 'on', 'for',
    'with', 'as', 'this', 'was', 'but', 'are', 'not', 'be', 'at', 'by',
    'an', 'if', 'or', 'from', 'so', 'we'
])

def top_n_words(lines, n=20):
    words = [word.lower() for line in lines for word in line.split() if word.lower() not in stopwords]
    return Counter(words).most_common(n)

# Main logic
if __name__ == "__main__":
    raw_captions = load_vtt_captions()
    raw_commentstxt = load_raw_commentstxt()

    print(f"Loaded {len(raw_captions)} caption lines.")
    print(raw_captions[:5])
    
    print(f"\nLoaded {len(raw_commentstxt)} comment lines.")
    print(raw_commentstxt[:5])

    # Histogram: caption vs. comment lengths
    caption_lengths = [len(x) for x in raw_captions]
    comment_lengths = [len(x) for x in raw_commentstxt]

    plt.hist(caption_lengths, bins=20, alpha=0.7, label='Captions')
    plt.hist(comment_lengths, bins=20, alpha=0.7, label='Comments')
    plt.legend()
    plt.xlabel('Length (characters)')
    plt.ylabel('Frequency')
    plt.title('Caption vs. Comment Lengths')
    plt.tight_layout()
    plt.show()

    # Type-token ratios
    print("\nCaption TTR:", type_token_ratio(raw_captions))
    print("Comment TTR:", type_token_ratio(raw_commentstxt))

    # Top words
    print("\nTop 20 caption words:", top_n_words(raw_captions))
    print("Top 20 comment words:", top_n_words(raw_commentstxt))
