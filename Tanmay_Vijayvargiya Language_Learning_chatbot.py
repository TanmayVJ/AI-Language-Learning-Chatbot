#                               [ AI Language Learning Chatbot ]
#                              Developed by "TANMAY VIJAYVARGIYA"
#    Email: tanmay.vijayvargiya2003@gmail.com | LinkedIn: www.linkedin.com/in/tanmay-vijayvargiya


# A.I Language Learning Chatbot Program

import sqlite3
import streamlit as st
from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# 🌍 AI-Powered Language Learning Chatbot (Using OpenAI + LangChain)

class LanguageLearningChatbot:

    def __init__(self, api_key: str):
        """
        Initialize chatbot with OpenAI's GPT model via LangChain.
        Also sets up SQLite database for tracking mistakes.
        """
        self.llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4.O")
        self.conn = sqlite3.connect("language_learning.db", check_same_thread=False)
        self.create_mistakes_table()

        # Conversation settings
        self.history = []
        self.learning_language = None
        self.native_language = None
        self.proficiency_level = None

    def create_mistakes_table(self):
        """Create SQLite table for tracking user mistakes."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY,
                language TEXT,
                mistake_type TEXT,
                original_text TEXT,
                corrected_text TEXT,
                explanation TEXT
            )
        """)
        self.conn.commit()

    def record_mistake(self, mistake_type: str, original: str, corrected: str, explanation: str):
        """Store mistakes in the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO mistakes (language, mistake_type, original_text, corrected_text, explanation) 
            VALUES (?, ?, ?, ?, ?)
        """, (self.learning_language, mistake_type, original, corrected, explanation))
        self.conn.commit()

    def get_conversation_scene(self) -> str:
        """Generate a fun learning scene based on proficiency level."""
        scenes = {
            "🌱 Beginner": ["A coffee shop ☕", "A taxi ride 🚕", "Ordering food 🍽️"],
            "⚡Intermediate": ["Discussing hobbies 🎨", "Travel experiences ✈️", "A job interview 💼"],
            "🚀 Advanced": ["A business meeting 📊", "Debating politics 🎤", "Explaining science 🔬"]
        }
        return scenes[self.proficiency_level][0]


    """The below comment, dynamically detects mistakes properly and 
        retrieves previous mistakes from the database.
        It continues the conversation smoothly without stopping."""   
    
    # def detect_mistakes(self, user_message: str, bot_reply: str) -> str:
    #     """Check for mistakes and retrieve past mistake corrections."""
        
    #     cursor = self.conn.cursor()
        
    #     # Fetch past mistakes for this language
    #     cursor.execute("SELECT original_text, corrected_text, explanation FROM mistakes WHERE language = ?", (self.learning_language,))
    #     mistakes = cursor.fetchall()

    #     # If there are no recorded mistakes, return an empty string
    #     if not mistakes:
    #         return ""

    #     correction_feedback = []

    #     # Check if the user's message contains past mistakes
    #     for original, corrected, explanation in mistakes:
    #         if original in user_message:
    #             feedback = f"❌ {original} → ✅ {corrected}\n💡 {explanation}"
    #             correction_feedback.append(feedback)

    #     # Return formatted mistake feedback
    #     return "\n\n".join(correction_feedback) if correction_feedback else ""
    

    # def generate_response(self, user_message: str) -> str:
    #     """Generate AI response and analyze mistakes for correction feedback."""
        
    #     system_prompt = f"""
    #     You are a friendly language tutor helping someone learn {self.learning_language}.
    #     - Speak in {self.learning_language}.
    #     - Adjust complexity to {self.proficiency_level} level.
    #     - If they make mistakes, gently correct them.
    #     - Encourage them to continue learning!
    #     - Keep it engaging and natural.
    #     """

    #     messages = [SystemMessage(content=system_prompt)] + self.history
    #     messages.append(HumanMessage(content=user_message))

    #     try:
    #         bot_reply = self.llm(messages).content  # LangChain API call
            
    #         # Save conversation history
    #         self.history.append(HumanMessage(content=user_message))
    #         self.history.append(AIMessage(content=bot_reply))

    #         # Analyze user mistakes
    #         mistake_feedback = self.detect_mistakes(user_message, bot_reply)

    #         # If mistakes are found, append feedback to bot response
    #         if mistake_feedback:
    #             bot_reply += f"\n\n🔍 **Correction:** {mistake_feedback}"

    #         return bot_reply
        
    #     except Exception as e:
    #         return f"🤖 Oops! API Error: {str(e)}"

    """Another variation of generate_response()"""
    def generate_response(self, user_message: str) -> str:
        """Send user input to OpenAI via LangChain and return AI response."""
        system_prompt = f"""
        You are a friendly language tutor helping someone learn {self.learning_language}.
        - Speak in {self.learning_language}.
        - Adjust complexity to {self.proficiency_level} level.
        - If they make mistakes, gently correct them.
        - Encourage them to continue learning!
        - Keep it engaging and natural.
        """
        messages = [SystemMessage(content=system_prompt)] + self.history
        messages.append(HumanMessage(content=user_message))


        # For any exception handling.
        try:

            bot_reply = self.llm(messages).content  # LangChain API call
            # Save chat history
            self.history.append(HumanMessage(content=user_message))
            self.history.append(AIMessage(content=bot_reply))
            return bot_reply

        except Exception as e:

            return f"🤖 Oops! API Error: {str(e)}"

    def analyze_mistakes(self) -> Dict:
        """Analyze mistakes and suggest improvements."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT mistake_type, COUNT(*) FROM mistakes WHERE language = ? GROUP BY mistake_type", 
                       (self.learning_language,))
        mistakes = dict(cursor.fetchall())

        # Personalized recommendations based on most frequent issues
# """        personalized_tips = {}
#         for mistake_type, specific_issue, count in mistakes:
#             if mistake_type == "grammar" and "verb" in specific_issue:
#                 tip = "Focus on verb conjugation rules 📖."
#             elif mistake_type == "spelling":
#                 tip = "Practice with spelling drills and word games 🎯."
#             elif mistake_type == "idiomatic errors":
#                 tip = "Learn common idioms and their meanings in context 💡."
#             elif mistake_type == "cultural mistakes":
#                 tip = "Study cultural nuances and context-based expressions 🌎."
#             else:
#                 tip = "Review your mistakes carefully and practice using them in sentences 📚."
            
#             personalized_tips[specific_issue] = tip

#         return {"mistake_details": mistakes, "personalized_tips": personalized_tips}"""

        recommendations = {
            "grammar": "Practice verb conjugations and sentence structure exercises.",
            "vocabulary": "Use flashcards to expand your vocabulary.",
            "pronunciation": "Listen to native speakers and repeat phrases.",
            "spelling": "Try dictation exercises.",
            "idiomatic": "Learn common idioms in this language.",
            "cultural": "Read about the culture to understand language nuances."
        }

        return {"mistake_counts": mistakes, "recommendations": recommendations}

    def close_connection(self):
        """Close database connection."""
        self.conn.close()


def main():
    # Streamlit App UI

    # Creating Header and Title
    st.set_page_config(page_title="AI Language Tutor", page_icon="🌍")
    st.sidebar.title("🔤 Language Learning Setup")

    # Initialize chatbot
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # API Key Input
    api_key = st.sidebar.text_input("Enter OpenAI API Key 🔑", type="password")

    # User Preferences

    # we can add as many learning_language as we want.
    learning_language = st.sidebar.selectbox("Language to Learn", ["🇪🇸 Spanish", "🇫🇷 French", "🇩🇪 German", "🇯🇵 Japanese"])
    # we can add as many native_language as we want.
    native_language = st.sidebar.selectbox("Your Native Language", ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 English", "🇪🇸 Spanish", "🇫🇷 French", "🇩🇪 German"])
    # we can add any difficulty as we want.
    proficiency_level = st.sidebar.selectbox("Proficiency Level", ["🌱 Beginner", "⚡Intermediate", "🚀 Advanced"])

    if st.sidebar.button("Start Learning! 🚀"):
        if api_key:
            chatbot = LanguageLearningChatbot(api_key)
            chatbot.learning_language = learning_language
            chatbot.native_language = native_language
            chatbot.proficiency_level = proficiency_level
            st.session_state.chatbot = chatbot
            st.session_state.messages = []

            scene = chatbot.get_conversation_scene()
            welcome_msg = f"🌟 Welcome! Let's practice {learning_language} at a {proficiency_level} level. Scene: {scene}."
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        else:
            st.sidebar.error("❌ Please enter an API key.")

    # Chat Interface
    st.title(f"🗣️ Language Chat: {learning_language}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.chatbot:
            with st.chat_message("assistant"):
                bot_reply = st.session_state.chatbot.generate_response(prompt)
                st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Mistake Analysis
    if st.session_state.chatbot:
        st.sidebar.header("📊 Learning Insights")
        mistakes = st.session_state.chatbot.analyze_mistakes()
        
        if mistakes["mistake_counts"]:
            st.sidebar.subheader("Your Mistakes:")
            for mistake, count in mistakes["mistake_counts"].items():
                st.sidebar.metric(mistake.capitalize(), count)
            
            st.sidebar.subheader("📌 Improvement Tips:")
            for area, tip in mistakes["recommendations"].items():
                st.sidebar.write(f"- {area.capitalize()}: {tip}")
        else:
            st.sidebar.info("Start chatting to track your progress! 📈")

    # Motivational Quote 
    # At Page Footer
    
    if "chatbot" in st.session_state and st.session_state.chatbot:
        motivational_quotes = [
            "Practice regularly for the best results! 🌟 Even 10 minutes a day can lead to significant improvement.",
            "The best way to learn a language is to make mistakes. Keep going! 💪",
            "Learning a new language opens up a whole new world of possibilities. 🌎",
            "Consistency beats perfection. A little practice each day adds up to big results! ✨",
            "Every conversation is a step forward in your language journey. 👣",
            "Language learning is a marathon, not a sprint. Enjoy the process! 🏃‍♀️",
            "The more you speak, the more confident you become. Keep practicing! 🗣️",
            "Don't worry about mistakes - they're your best teachers in language learning. 📚",
            "You're building neural pathways with every new word you learn! 🧠",
            "Bilingual people have stronger cognitive abilities. You're getting smarter! 🧠✨"
        ]
        import random
        random_quote = random.choice(motivational_quotes)
        st.markdown(f""" 
        <div style="text-align: center; margin-top: 12rem; color: #757575; font-size: 0.8rem;">
        {random_quote}
        </div>
        """, unsafe_allow_html=True)


# Running the main program
if __name__ == "__main__":
    main()

