# ChatBot-Wiki-Agent-Navigator

## Description
ChatBot-Wiki-Agent-Navigator is an intelligent question-answering system that combines the power of a vector store and Wikipedia to provide accurate and contextual responses. It uses a sophisticated routing mechanism to decide whether to retrieve information from a local vector store or to search Wikipedia based on the nature of the question.

## Features

- Intelligent routing of questions to appropriate knowledge sources
- Integration with a vector store for efficient retrieval of pre-stored information
- Wikipedia search capability for general knowledge questions
- FastAPI-based RESTful API for easy integration and real-time query handling
- Langchain-powered workflow for flexible and extensible question-answering pipeline
- Hybrid response generation, dynamically selecting the best data source based on the nature of the query
- Scalable architecture allowing for seamless expansion of knowledge sources
- Efficient processing of both factual and contextual questions, ensuring relevant answers

## Project Structure
```
project_root/
│   ├── config.py
│   ├── models.py
│   ├── routers/
│   │   └── qa.py
│   ├── scripts/
│   │   └── load_documents.py
│   └── services/
│       ├── vector_store.py
│       ├── llm.py
│       └── wikipedia.py
├── frontend/
│   ├── index.html
│   └── static/
│       ├── css/
│       │   └── tailwind.css
│       └── js/
│           └── main.js
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/1666sApple/ChatBot-Wiki-Agent-Navigator.git
   cd ChatBot-Wiki-Agent-Navigator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate` 
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   ASTRA_DB_TOKEN=your_astra_db_token
   ASTRA_DB_ID=your_astra_db_id
   HF_API_KEY=your_huggingface_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn backend.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. Start the local `index.html` file using:
   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

3. Open a web browser and navigate to the given url to use the application. :
   ```
   http://localhost:8080

## Configuration

You can configure the following components in their respective files:

- Vector Store: `backend/services/vector_store.py`
- Language Model: `backend/services/llm.py`
- Wikipedia Tool: `backend/services/wikipedia.py`

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Langchain](https://python.langchain.com/)
- [GroqAPI](https://console.groq.com/)
- [AstraDB](https://astra.datastax.com/)
- [HuggingFace](https://huggingface.co/) 
- [Wikipedia API](https://pypi.org/project/Wikipedia-API/)


## Contributing

We welcome contributions to the ChatBot Wiki Agent Navigator! Please follow these steps to contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some Feature'`)
4. Push to the branch (`git push origin feature/Feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Link: [https://github.com/1666sApple/ChatBot-Wiki-Agent-Navigator](https://github.com/1666sApple/ChatBot-Wiki-Agent-Navigator)

If you have any questions, feel free to open an issue or contact the maintainers directly.

---

Happy coding, and may your chatbot always find the right answers! 🤖📚🔍