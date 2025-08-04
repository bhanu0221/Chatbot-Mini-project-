from flask import Flask, request, jsonify, render_template
import pandas as pd
import string

app = Flask(__name__)

data = {
    "question": [
        # Greetings
        "hi", "hello", "hey", "how are you", "good morning", "good evening","good night","what","thanks",

        # Informational
        "who build you?",
        "how to prepare for exams",
        "best programming language to learn",
        "how to improve english",
        "what is python",
        "how to build a website",
        "tips for time management",
        "how to improve programming logic",
        "how to create a chatbot",
        "what is machine learning",
        "how to learn data analysis"
    ],
    "answer": [
        # Greeting responses
        "Hello! How can I help you today?",
        "Hi there! Ask me anything.",
        "Hey! What would you like to know?",
        "I'm just a bot, but I'm doing great! How can I assist you?",
        "Good morning! What can I do for you?",
        "Good evening! Feel free to ask me something.",
        "Good night! take some rest.",
        "Sorry, I didn't understand that. Can you rephrase it?",
        "your welcome.",

        # Informational responses
        "Anup shahi Build me to assist you.",
        "Make a timetable and revise regularly.",
        "Start with Python. Then JavaScript or C++.",
        "Read books, speak often, and use apps like Duolingo.",
        "Python is a programming language used in backd-end ",
        "Learn HTML, CSS, JavaScript, and use Flask or Django for backend.",
        "Use calendars, set deadlines, and avoid multitasking.",
        "Practice solving problems and learn algorithms step by step.",
        "Use Python + Flask for a simple chatbot. Integrate logic and UI.",
        "Machine learning enables computers to learn from data.",
        "Start with Excel, then learn Python, Pandas, and visualization tools."
    ]
}
kb = pd.DataFrame(data)

# Basic preprocessing (lowercase + remove punctuation)
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.strip()

# Clean all questions in the knowledge base
kb['clean_question'] = kb['question'].apply(clean_text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about us')
def aboutus():
    return render_template('about us.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")
    cleaned_input = clean_text(user_msg)

    # Try exact match first
    for i, q in enumerate(kb['clean_question']):
        if cleaned_input == q:
            return jsonify({"response": kb.iloc[i]['answer']})

    # Try partial/keyword match
    user_words = set(cleaned_input.split())
    max_overlap = 0
    best_index = -1

    for i, q in enumerate(kb['clean_question']):
        question_words = set(q.split())
        overlap = len(user_words & question_words)
        if overlap > max_overlap:
            max_overlap = overlap
            best_index = i

    if max_overlap > 0:
        return jsonify({"response": kb.iloc[best_index]['answer']})
    else:
        return jsonify({"response": "Sorry, I didn't understand that. Can you rephrase it?"})

if __name__ == '__main__':
    app.run(debug=True)
