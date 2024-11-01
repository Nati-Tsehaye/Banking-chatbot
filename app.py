from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class ChatbotPredictor:
    def __init__(self):
        logger.info("Initializing ChatbotPredictor...")
        # Initialize NLTK resources
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            logger.error(f"Error initializing NLTK: {str(e)}")
            self.stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our'])
        
        # Load the saved model and components
        self.load_model()

    def load_model(self):
        try:
            model_dir = os.path.join(os.path.dirname(__file__), 'models')
            
            # Load model files
            self.model = joblib.load(os.path.join(model_dir, 'model_20241029_200521.joblib'))
            self.vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer_20241029_200521.joblib'))
            
            # Load mappings and responses
            with open(os.path.join(model_dir, 'mappings_20241029_093521.json'), 'r') as f:
                mappings = json.load(f)
                self.category_mapping = {int(k): v for k, v in mappings['category_mapping'].items()}
            
            # Define responses dictionary
            self.responses = {
            0: "To activate your new card, you can:\n1. Open the mobile app and go to the 'Cards' section\n2. Select 'Activate Card' and follow the on-screen instructions\n3. Or, you can call our customer support line and they'll be happy to assist you.",
            1: "To ensure you're eligible, please check our age requirements on the website or contact support for assistance.",
            2: "You can use Apple Pay or Google Pay by linking your card in the respective app settings.",
            3: "For ATM support, please visit our nearest branch or contact customer service.",
            4: "To set up automatic top-up, visit the app and choose 'Automatic Top-Up' under account settings.",
            5: "If your balance isn't updated after a bank transfer, please wait a few hours or contact support.",
            6: "Please check with your bank regarding cheque or cash deposit updates.",
            7: "If a beneficiary is not allowed, please review our beneficiary policy or contact customer support.",
            8: "To cancel a transfer, please go to the 'Transfers' section in the app and select 'Cancel'.",
            9: "If your card is about to expire, you will receive a new card automatically before the expiration date.",
            10: "To check card acceptance, please refer to our list of supported merchants on our website.",
            11: "Your card will arrive in 5-7 business days via standard mail.",
            12: "You can expect your card delivery to take up to 10 business days.",
            13: "Follow the app instructions to link your card, or contact support for help.",
            14: "If your card isn't working, please check for any alerts in the app or contact support.",
            15: "Any fees related to card payments will be detailed in your monthly statement.",
            16: "If your card payment isn't recognized, please verify your transaction history in the app.",
            17: "If you believe there’s a wrong exchange rate, please contact our customer support for clarification.",
            18: "If your card was swallowed by an ATM, please report it immediately to customer support.",
            19: "Cash withdrawal charges apply based on your account type; please refer to our fees page.",
            20: "If your cash withdrawal isn't recognized, please check your transaction history or contact support.",
            21: "To change your PIN, please visit the 'Security' section in the app.",
            22: "If you believe your card is compromised, please freeze it in the app and contact support.",
            23: "If your contactless payment isn’t working, please ensure your card is enabled for contactless.",
            24: "For country-specific support, please visit our support page for more details.",
            25: "If your card payment was declined, please check for any alerts or contact support.",
            26: "For declined cash withdrawals, please check your balance and limits in the app.",
            27: "If your transfer was declined, please check the reason in the app or contact support.",
            28: "To verify direct debit payments, please check your account settings or contact support.",
            29: "Disposable card limits can be set in the app under card settings.",
            30: "To edit personal details, go to your profile in the app and make the necessary changes.",
            31: "Exchange charges will be shown during the transaction process.",
            32: "Current exchange rates can be viewed in the app or on our website.",
            33: "You can exchange currency via the app in the 'Exchange' section.",
            34: "Extra charges will be detailed in your monthly statement.",
            35: "If a transfer has failed, please check the details and try again, or contact support.",
            36: "We support various fiat currencies; please check our website for details.",
            37: "To get a disposable virtual card, you can generate one through the app.",
            38: "To get a physical card, please request one in the app under 'Cards'.",
            39: "If you need a spare card, you can request one through the app.",
            40: "You can get a virtual card through the app options.",
            41: "If your card is lost or stolen, please report it immediately through the app.",
            42: "If your phone is lost or stolen, please contact support to secure your account.",
            43: "To order a physical card, please visit the 'Cards' section in the app.",
            44: "If you forgot your passcode, please follow the recovery steps in the app.",
            45: "If your card payment is pending, please check your transaction status in the app.",
            46: "Pending cash withdrawals may take a few moments to process.",
            47: "Pending top-ups can take time; please check your account for updates.",
            48: "Pending transfers will be shown in your transaction history.",
            49: "If your PIN is blocked, please follow the reset instructions in the app.",
            50: "For receiving money, please check the 'Receive' section in the app.",
            51: "If your refund isn't showing up, please verify with the merchant or contact support.",
            52: "To request a refund, please contact support with your transaction details.",
            53: "If your card payment was reverted, please check the transaction history.",
            54: "We support various cards and currencies; please refer to our website.",
            55: "To terminate your account, please follow the instructions in the app.",
            56: "A charge may apply for topping up by bank transfer depending on your account type. Please check our fees page for details.",
            57: "Top-ups made by card may have a fee depending on your card provider. Please check with them or refer to our fee policy.",
            58: "To top up by cash or cheque, please visit a participating branch or refer to our cash top-up options in the app.",
            59: "If your top-up has failed, please double-check the details and try again. Contact support if the issue persists.",
            60: "Top-up limits vary by account type. Please check your app settings under 'Top-Up Limits' or contact support.",
            61: "If your top-up was reverted, please confirm the reason in your transaction history or reach out to support.",
            62: "To top up using a card, please go to the 'Top-Up' section in the app and select 'Top-Up by Card'.",
            63: "If you were charged twice for a transaction, please verify your transaction history and contact support for assistance.",
            64: "Transfer fees are charged based on the currency and transfer type. Please refer to our fees page for more information.",
            65: "To transfer money into your account, please go to the 'Transfer' section in the app for account details.",
            66: "If your transfer hasn't been received by the recipient, please verify the details and contact support if needed.",
            67: "Transfer timing varies by currency and region. Check our website or app for estimated transfer times.",
            68: "If you're unable to verify your identity, please ensure your documents are correct and contact support if needed.",
            69: "To verify your identity, please follow the steps in the app under 'Verify Identity'.",
            70: "To verify the source of funds, please provide supporting documents as requested in the app.",
            71: "To verify your top-up, please follow any prompts in the app or contact support if verification is required.",
            72: "If your virtual card is not working, please check your app settings or contact support for help.",
            73: "We support Visa and Mastercard. Please check the app for card-specific options.",
            74: "We ask to verify your identity to comply with regulations and ensure account security.",
            75: "If you received the wrong amount of cash, please check your transaction history and contact support immediately.",
            76: "If you believe the exchange rate is incorrect for your cash withdrawal, please reach out to support for assistance."
        
        }
            logger.info("Model and components loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def preprocess_text(self, text):
        try:
            text = str(text).lower()
            text = re.sub(r'[^a-z0-9\s?.!,]', '', text)
            tokens = word_tokenize(text)
            
            important_words = {'how', 'what', 'why', 'where', 'when', 'who', 'card', 'money', 'transfer', 'receive', 'exchange', 'rate'}
            tokens = [token for token in tokens if token not in self.stop_words or token in important_words]
            
            processed_text = " ".join(tokens)
            logger.debug(f"Preprocessed text: {processed_text}")
            return processed_text
        except Exception as e:
            logger.error(f"Error during text preprocessing: {str(e)}")
            return text

    def predict(self, input_text):
        try:
            logger.info(f"Received input text: {input_text}")
            input_text = input_text.lower().strip()

            # Custom responses for specific phrases
            if re.search(r'\b(hello|hi|hey)\b', input_text):
                return {
                    "category": "custom",
                    "response": "Hello, valued client!"
                }
            elif re.search(r'\b(thank you|thanks)\b', input_text):
                return {
                    "category": "custom",
                    "response": "You're very welcome! Let me know if there's anything else I can help with."
                }
            elif re.search(r'\bI want to (speak|talk) to a (human|representative|agent)\b', input_text):
                return {
                    "category": "custom",
                    "response": "I'll connect you to a human representative right away."
                }
            elif re.search(r'\b(goodbye|bye|see you)\b', input_text):
                return {
                    "category": "custom",
                    "response": "Goodbye! Have a great day!"
                }
            elif re.search(r'\b(help|assist)\b', input_text):
                return {
                    "category": "custom",
                    "response": "Sure, I'm here to help! Could you please provide more details?"
                }

            # Proceed with model prediction if no custom response matches
            processed_input = self.preprocess_text(input_text)
            X_input = self.vectorizer.transform([processed_input])
            predicted_label = self.model.predict(X_input)[0]
            
            # Fetch response based on prediction
            response = self.responses.get(predicted_label, "I'm sorry, I can't assist with that request.")
            logger.info(f"Prediction successful. Category: {predicted_label}")
            
            return {
                "category": int(predicted_label),
                "response": response
            }
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return None

# Initialize chatbot
try:
    chatbot = ChatbotPredictor()
except Exception as e:
    logger.error(f"Failed to initialize chatbot: {str(e)}")
    chatbot = None

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if chatbot is None:
            return jsonify({"error": "Chatbot not initialized properly"}), 500

        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_message = data.get('message', '')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Received chat request with message: {user_message}")
        prediction = chatbot.predict(user_message)
        
        if prediction is None:
            return jsonify({"error": "Prediction failed"}), 500

        logger.info(f"Sending response: {prediction}")
        return jsonify(prediction)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
