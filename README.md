Banking Support Chatbot
A full-stack AI-powered customer support chatbot that handles banking-related queries. Built with React and Python, this project combines machine learning capabilities with a modern web interface.
Show Image
✨ Features

Real-time chat interface
77 different banking-related categories
Machine learning-powered responses
Modern, responsive UI
Pre-trained model included
Easy-to-use API endpoints

🚀 Tech Stack
Frontend

React.js
Tailwind CSS
JavaScript/ES6+

Backend

Python/Flask
scikit-learn
NLTK
Pandas

📁 Project Structure
Copybanking-chatbot/
├── backend/
│   ├── app.py              # Flask server
│   ├── chatbot.py          # ML model implementation
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   └── App.js        # Main application
│   └── package.json
│
└── notebook/
    └── training.ipynb     # Model training notebook
⚙️ Setup & Installation
Backend Setup
bashCopycd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Frontend Setup
bashCopycd frontend
npm install
🚀 Running the Application

Start Backend:

bashCopycd backend
python app.py

Start Frontend:

bashCopycd frontend
npm start
Visit http://localhost:3000 to use the chatbot.
🔧 Model Training (Optional)
The project includes a pre-trained model, but you can retrain it:
bashCopycd notebook
jupyter notebook training.ipynb
🌟 Main Features Explained
Chatbot Intelligence

Natural language processing for query understanding
TF-IDF vectorization for text analysis
Logistic Regression model for intent classification
Pre-defined response templates for accuracy

Web Interface

Real-time message updates
Message history
Typing indicators
Mobile-responsive design
Error handling

📡 API Endpoints
javascriptCopyPOST /api/chat
{
    "message": "How do I activate my card?"
}
💡 Use Cases

Card activation queries
Transaction issues
Account management
Balance inquiries
Transfer assistance
General banking support

🤝 Contributing

Fork the repository
Create a feature branch
Commit changes
Push to the branch
Create a Pull Request

📄 License
MIT License
👏 Acknowledgments

Banking77 Dataset from Hugging Face
React.js community
scikit-learn contributors
NLTK team

📞 Support
Open an issue or submit a pull request for any bugs/improvements.
