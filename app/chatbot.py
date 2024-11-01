import json
import joblib
from .utils import preprocess_text
from typing import Dict, Any

class ChatbotService:
    def __init__(self, model_path: str, vectorizer_path: str, mappings_path: str):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
        with open(mappings_path, 'r') as f:
            mappings = json.load(f)
            self.category_mapping = {int(k): v for k, v in mappings['category_mapping'].items()}
            self.reverse_category_mapping = mappings['reverse_category_mapping']
        
        self.conversations: Dict[str, Dict[str, Any]] = {}

    def create_session(self, session_id: str):
        self.conversations[session_id] = {
            'current_intent': None,
            'follow_up_count': 0,
            'context': {}
        }

    def get_intent_specific_responses(self, intent: str, stage: str = 'initial') -> str:
        response_category = self.map_dataset_category_to_response_category(intent)
        
        responses = {
            'transfer_money': {
                'initial': "I can help you with your transfer request. Would you like to:\n1. Make a new transfer\n2. Check transfer status\n3. View recent transfers",
                'follow_up_1': "To proceed with the transfer, please provide:\n1. Recipient's name\n2. Amount to transfer\n3. Purpose of transfer",
                'follow_up_2': "Would you like to:\n1. Confirm the transfer details\n2. Check transfer fees\n3. Cancel this transfer",
                'follow_up_3': "Is there anything else you'd like to know about transfers?"
            },
            'card_issues': {
                'initial': "I can help with card-related issues. What would you like to do?\n1. Report a problem\n2. Check card status\n3. Get card information",
                'follow_up_1': "Could you please specify the issue you're experiencing with your card?",
                'follow_up_2': "Would you like me to:\n1. Guide you through troubleshooting\n2. Help you report the issue\n3. Explain card features",
            },
            'exchange_info': {
                'initial': "I can help you with exchange rate information. What would you like to know?\n1. Current exchange rates\n2. Exchange fees\n3. Exchange limits",
                'follow_up_1': "Would you like to:\n1. Get a quote for a specific amount\n2. Learn about our exchange services\n3. Check exchange history",
            },
            'security_issues': {
                'initial': "I'll help you with security concerns. What would you like to do?\n1. Report suspicious activity\n2. Secure your account\n3. Update security settings",
                'follow_up_1': "Would you like me to:\n1. Guide you through security steps\n2. Help you report an incident\n3. Explain security features",
            },
            'general_inquiry': {
                'initial': "How can I assist you today?\n1. Account information\n2. Services overview\n3. General support",
                'follow_up_1': "Would you like more specific information about any of our services?",
            }
        }
        
        return responses.get(response_category, {}).get(stage, "I'm here to help. Could you please provide more details about your request?")

    def map_dataset_category_to_response_category(self, intent_category: str) -> str:
        transfer_related = [
            'transfer_timing', 'transfer_not_received_by_recipient',
            'transfer_fee_charged', 'transfer_into_account', 'failed_transfer',
            'pending_transfer', 'cancel_transfer', 'declined_transfer'
        ]
        
        card_related = [
            'card_arrival', 'card_not_working', 'lost_or_stolen_card',
            'card_about_to_expire', 'card_swallowed', 'card_payment_not_recognised'
        ]
        
        exchange_related = [
            'exchange_rate', 'exchange_charge', 'exchange_via_app',
            'card_payment_wrong_exchange_rate'
        ]
        
        security_related = [
            'lost_or_stolen_phone', 'lost_or_stolen_card',
            'compromised_card', 'verify_identity'
        ]
        
        if intent_category in transfer_related:
            return 'transfer_money'
        elif intent_category in card_related:
            return 'card_issues'
        elif intent_category in exchange_related:
            return 'exchange_info'
        elif intent_category in security_related:
            return 'security_issues'
        else:
            return 'general_inquiry'

    def generate_response(self, user_input: str, session_id: str) -> str:
        if session_id not in self.conversations:
            self.create_session(session_id)
            
        processed_input = preprocess_text(user_input)
        
        try:
            feature_vector = self.vectorizer.transform([processed_input])
            intent_number = self.model.predict(feature_vector)[0]
            intent_category = self.category_mapping.get(intent_number)
            
            if intent_category is None:
                return "I'm sorry, I didn't understand that. Could you please rephrase your request?"

            conversation = self.conversations[session_id]
            conversation['current_intent'] = intent_category

            # Check for specific intents in follow-ups
            if conversation['follow_up_count'] == 0:
                if "report a problem" in processed_input.lower():
                    conversation['follow_up_count'] = 1  # Move to follow-up response
                    return self.get_intent_specific_responses(intent_category, 'follow_up_1')

                if "check card status" in processed_input.lower():
                    return "Please provide the card number to check its status."

                if "get card information" in processed_input.lower():
                    return "Please specify what information you would like about your card."

            # General follow-up responses
            if conversation['follow_up_count'] < 3:
                response_stage = 'initial' if conversation['follow_up_count'] == 0 else f'follow_up_{conversation["follow_up_count"]}'
                conversation['follow_up_count'] += 1
                
                response = self.get_intent_specific_responses(intent_category, response_stage)
                return response
            
            else:
                conversation['follow_up_count'] = 0
                return "Let's start over. How can I assist you today?"

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I'm having trouble processing your request. Could you please try again?"

