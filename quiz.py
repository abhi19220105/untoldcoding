import json
import time
import random
from datetime import datetime

class QuizGame:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.current_question = 0
        self.quiz_start_time = 0
        self.quiz_duration = 0
        self.user_answers = []
        self.categories = set()
        self.selected_category = None
        self.difficulty_levels = ['Easy', 'Medium', 'Hard']
        self.selected_difficulty = None
    
    def load_questions(self, filename='questions.json'):
        """Load questions from JSON file and organize them"""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.questions = data['questions']
                self.categories = set(q['category'] for q in self.questions if 'category' in q)
                print(f"Loaded {len(self.questions)} questions in {len(self.categories)} categories.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading questions: {str(e)}")
    
    def display_welcome(self):
        """Show welcome message and instructions"""
        print("\n" + "="*50)
        print("PYTHON QUIZ GAME".center(50))
        print("="*50)
        print("\nTest your knowledge with this interactive quiz!")
        print("\nFeatures:")
        print("- Multiple categories and difficulty levels")
        print("- Timer for each question")
        print("- Detailed score report at the end")
        print("- Review your answers after the quiz")
        print("\n" + "="*50)
    
    def select_category(self):
        """Let user select a quiz category"""
        if not self.categories:
            return
        
        print("\nAvailable Categories:")
        for i, category in enumerate(sorted(self.categories), 1):
            print(f"{i}. {category}")
        print(f"{len(self.categories)+1}. All Categories")
        
        while True:
            try:
                choice = int(input("\nSelect category (number): "))
                if 1 <= choice <= len(self.categories)+1:
                    break
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        if choice == len(self.categories)+1:
            self.selected_category = None
        else:
            self.selected_category = sorted(self.categories)[choice-1]
    
    def select_difficulty(self):
        """Let user select difficulty level"""
        print("\nSelect Difficulty Level:")
        for i, level in enumerate(self.difficulty_levels, 1):
            print(f"{i}. {level}")
        
        while True:
            try:
                choice = int(input("\nSelect difficulty (number): "))
                if 1 <= choice <= len(self.difficulty_levels):
                    self.selected_difficulty = self.difficulty_levels[choice-1]
                    break
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
    
    def filter_questions(self):
        """Filter questions based on selected category and difficulty"""
        filtered = []
        for q in self.questions:
            if self.selected_category and q.get('category') != self.selected_category:
                continue
            if self.selected_difficulty and q.get('difficulty') != self.selected_difficulty:
                continue
            filtered.append(q)
        
        if not filtered:
            print("\nNo questions match your selected criteria.")
            print("Showing all questions instead.")
            return self.questions
        
        # Shuffle questions for variety
        random.shuffle(filtered)
        return filtered[:10]  # Limit to 10 questions
    
    def ask_question(self, question):
        """Display a question and get user's answer with timer"""
        print(f"\nQuestion {self.current_question + 1}:")
        print(question['question'])
        
        # Display options
        options = question['options']
        for opt in options:
            print(f"  {opt['letter']}. {opt['text']}")
        
        # Add timer
        start_time = time.time()
        while True:
            answer = input("\nYour answer (letter) or 'S' to skip: ").upper()
            
            # Check if time exceeded (10 seconds per question)
            if time.time() - start_time > 10:
                print("\nTime's up! Moving to next question.")
                return None, False
            
            if answer == 'S':
                return None, False
            elif answer in [opt['letter'] for opt in options]:
                time_taken = time.time() - start_time
                return answer, time_taken < 5  # Bonus for quick answers
            else:
                print("Invalid input. Please enter the letter of your choice.")
    
    def check_answer(self, user_answer, question):
        """Check if answer is correct and update score"""
        correct = user_answer == question['correct_answer']
        if correct:
            self.score += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Incorrect. The correct answer was {question['correct_answer']}."
        
        # Store user's answer for review
        self.user_answers.append({
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'is_correct': correct
        })
        
        print(f"\n{feedback}")
        time.sleep(1)
    
    def show_progress(self):
        """Display current progress in the quiz"""
        print(f"\nProgress: {self.current_question + 1}/{len(self.filtered_questions)}")
        print(f"Current Score: {self.score}")
    
    def show_results(self):
        """Display final results and statistics"""
        total = len(self.filtered_questions)
        percentage = (self.score / total) * 100 if total > 0 else 0
        
        print("\n" + "="*50)
        print("QUIZ RESULTS".center(50))
        print("="*50)
        print(f"\nFinal Score: {self.score}/{total}")
        print(f"Percentage: {percentage:.1f}%")
        print(f"Time Taken: {self.quiz_duration:.1f} seconds")
        
        # Performance feedback
        if percentage >= 90:
            print("\n🏆 Excellent! You're a quiz master!")
        elif percentage >= 70:
            print("\n👍 Great job! You know your stuff!")
        elif percentage >= 50:
            print("\n😊 Good effort! Keep learning!")
        else:
            print("\n📚 Keep studying! You'll improve!")
        
        # Offer to review answers
        review = input("\nWould you like to review your answers? (Y/N): ").upper()
        if review == 'Y':
            self.review_answers()
    
    def review_answers(self):
        """Show all questions with user's answers and correct answers"""
        print("\n" + "="*50)
        print("ANSWER REVIEW".center(50))
        print("="*50)
        
        for i, answer in enumerate(self.user_answers, 1):
            print(f"\nQuestion {i}: {answer['question']}")
            print(f"Your answer: {answer['user_answer']}")
            print(f"Correct answer: {answer['correct_answer']}")
            print("✅ Correct" if answer['is_correct'] else "❌ Incorrect")
            print("-"*50)
    
    def run(self):
        """Main method to run the quiz game"""
        self.load_questions()
        self.display_welcome()
        
        # Setup quiz parameters
        self.select_category()
        self.select_difficulty()
        self.filtered_questions = self.filter_questions()
        
        if not self.filtered_questions:
            print("No questions available. Exiting...")
            return
        
        input("\nPress Enter to start the quiz...")
        print("\n" + "="*50)
        
        # Start quiz timer
        self.quiz_start_time = time.time()
        
        # Ask each question
        for question in self.filtered_questions:
            self.current_question += 1
            self.show_progress()
            
            answer, is_quick = self.ask_question(question)
            if answer is not None:
                self.check_answer(answer, question)
                if is_quick:
                    print("+ Quick answer bonus!")
                    self.score += 0.5  # Bonus points
            
            # Brief pause between questions
            time.sleep(0.5)
        
        # Calculate total time
        self.quiz_duration = time.time() - self.quiz_start_time
        
        # Show results
        self.show_results()

# Sample questions data structure
sample_data = {
    "questions": [
        {
            "question": "What is the output of 'print(3 * '7')' in Python?",
            "options": [
                {"letter": "A", "text": "21"},
                {"letter": "B", "text": "777"},
                {"letter": "C", "text": "TypeError"},
                {"letter": "D", "text": "37"}
            ],
            "correct_answer": "B",
            "category": "Python Basics",
            "difficulty": "Easy"
        },
        {
            "question": "Which of these is NOT a Python built-in data structure?",
            "options": [
                {"letter": "A", "text": "list"},
                {"letter": "B", "text": "tuple"},
                {"letter": "C", "text": "array"},
                {"letter": "D", "text": "dictionary"}
            ],
            "correct_answer": "C",
            "category": "Python Basics",
            "difficulty": "Easy"
        },
        {
            "question": "What does the 'zip()' function do in Python?",
            "options": [
                {"letter": "A", "text": "Compresses files"},
                {"letter": "B", "text": "Combines iterables element-wise"},
                {"letter": "C", "text": "Creates a backup of data"},
                {"letter": "D", "text": "Encrypts strings"}
            ],
            "correct_answer": "B",
            "category": "Python Functions",
            "difficulty": "Medium"
        }
    ]
}

# Create sample questions file if it doesn't exist
try:
    with open('questions.json', 'x') as f:
        json.dump(sample_data, f, indent=2)
except FileExistsError:
    pass

# Run the quiz game
if __name__ == "__main__":
    game = QuizGame()
    game.run()