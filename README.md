# Banking Support Chatbot

A full-stack AI-powered customer support chatbot that handles banking-related queries. Built with React and Python, this project combines machine learning capabilities with a modern web interface.

![Screenshot 2024-10-29 234356](https://github.com/user-attachments/assets/0955a533-1bf6-42a1-8095-60f9aed1a722)

## ✨ Features

- Real-time chat interface
- 77 different banking-related categories
- Machine learning-powered responses
- Modern, responsive UI
- Pre-trained model included
- Easy-to-use API endpoints

## 🚀 Tech Stack

### Frontend
- React.js
- Tailwind CSS
- JavaScript/ES6+

### Backend
- Python/Flask
- scikit-learn
- NLTK
- Pandas

## ⚙️ Setup & Installation

### Backend Setup
1. Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2. Set up a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
   - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
   - On Windows:
      ```bash
      venv\Scripts\activate
      ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Frontend Setup
1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
## 🚀 Running the Application

### Start Backend:
1. Navigate to the `backend` directory and start the backend server:
    ```bash
    cd backend
    python app.py
    ```

### Start Frontend:
1. Navigate to the `frontend` directory and start the frontend:
    ```bash
    cd frontend
    npm start
    ```
Visit [http://localhost:3000](http://localhost:3000) to use the chatbot.

## 🔧 Model Training (Optional)

The project includes a pre-trained model, but you can retrain it:
```bash
cd notebook
jupyter notebook training.ipynb
```
## 🌟 Main Features Explained
### Chatbot Intelligence

- Natural language processing for query understanding
- TF-IDF vectorization for text analysis
- Logistic Regression model for intent classification
- Pre-defined response templates for accuracy

## Web Interface

- Real-time message updates
- Message history
- Typing indicators
- Mobile-responsive design
- Error handling

## 📡 API Endpoints

### Chat Endpoint

- **Endpoint**: `POST /api/chat`
- **Description**: Handles user queries and returns chatbot responses.

#### Example Request
```json
POST /api/chat
{
    "message": "How do I activate my card?"
}
```
## Card activation queries
- Transaction issues
- Account management
- Balance inquiries
- Transfer assistance
- General banking support

## 🤝 Contributing

- Fork the repository
- Create a feature branch
- Commit changes
- Push to the branch
- Create a Pull Request

## 📄 License
MIT License

## 👏 Acknowledgments
- Banking77 Dataset from Hugging Face
- React.js community
- scikit-learn contributors
- NLTK team
