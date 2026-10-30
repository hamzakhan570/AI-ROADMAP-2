# 🗺️ AI Learning Roadmap Generator

A Streamlit web app that creates a personalized learning roadmap for any field. Enter what you want to learn, your skill level, and how much time you have, and an LLM (via the Groq API) generates a phase-by-phase plan with projects and free resources.

## Features

- Choose any field or topic
- Skill level: Beginner, Intermediate, or Advanced
- Set duration (weeks or months) and study hours per week
- Roadmap streams in live as it is generated
- Download the result as a Markdown file

## Tech Stack

- **Python 3.10+**
- **Streamlit** for the user interface
- **Groq API** for the LLM
- **GitHub** for version control and deployment

## Project Structure

```
ai-roadmap-generator/
├── app.py            # Streamlit UI and Groq logic
├── requirements.txt  # Python dependencies
├── .env              # Local API key (never commit this)
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-roadmap-generator.git
cd ai-roadmap-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Get a free key at [console.groq.com](https://console.groq.com), then create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

Make sure `.gitignore` includes:

```
.env
venv/
.streamlit/secrets.toml
```

### 5. Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Push to GitHub

```bash
git add .
git commit -m "Add AI learning roadmap generator"
git push origin main
```

Check that `.env` does not appear in your repository.

## Deploy on Streamlit Community Cloud (free)

1. Push the project to a **public** GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app**, select your repo, branch `main`, and main file `app.py`.
4. Open **Advanced settings → Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
5. Click **Deploy**. Every push to GitHub redeploys automatically.

## Configuration

| Variable       | Purpose                                | Default                   |
| -------------- | -------------------------------------- | ------------------------- |
| `GROQ_API_KEY` | Your Groq API key (required)           | none                      |
| `GROQ_MODEL`   | Groq model name (optional)             | `llama-3.3-70b-versatile` |

Groq model names change over time, so check the [model list](https://console.groq.com/docs/models) if you get a "model not found" error. You can also change the model from the app sidebar.

## Ideas for Improvement

- Return structured JSON and show phases as expandable sections
- Progress tracking with checkboxes
- PDF export
- Save past roadmaps in a database
- Caching to reduce repeated API calls

## License

MIT
