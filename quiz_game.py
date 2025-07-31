from tkinter import Tk, Label, Button, Frame
import pygame
import os

class Question:
    def __init__(self, category, question, answers, correctLetter):
        self.category = category
        self.question = question
        self.answers = answers  # Fixed: now properly stores the answers list
        self.correctLetter = correctLetter

    def check(self, letter, view):
        global right, correct_sound, incorrect_sound
        if letter == self.correctLetter:
            label = Label(view, text="Correct!", font=("Helvetica", 20), bg='green', fg='white')
            label.pack(pady=10)
            # Play correct sound if available
            if 'correct_sound' in globals():
                pygame.mixer.Sound.play(correct_sound)
            right += 1
        else:
            correct_answer = ""
            for i, ans_letter in enumerate(['A', 'B', 'C', 'D']):
                if ans_letter == self.correctLetter:
                    correct_answer = self.answers[i]
                    break
            label = Label(view, text=f"Wrong! Correct answer: {correct_answer}", 
                         font=("Helvetica", 16), bg='red', fg='white')
            label.pack(pady=10)
            # Play incorrect sound if available
            if 'incorrect_sound' in globals():
                pygame.mixer.Sound.play(incorrect_sound)
        
        # Wait 2 seconds then go to next question
        view.after(2000, lambda: self.nextQuestion(view))

    def nextQuestion(self, view):
        view.pack_forget()
        askQuestion()

    def getView(self, window):
        view = Frame(window, bg='black')
        
        # Question text
        question_label = Label(view, text=self.question, font=("Comic Sans MS", 20), 
                              bg='black', fg='sky blue', wraplength=600)
        question_label.pack(pady=20)
        
        # Answer buttons
        answer_letters = ['A', 'B', 'C', 'D']
        for i, answer in enumerate(self.answers):
            btn_text = f"{answer_letters[i]}) {answer}"
            Button(view, text=btn_text, 
                  command=lambda letter=answer_letters[i]: self.check(letter, view),
                  font=("Helvetica", 14), bg='gray', fg='white', 
                  wraplength=500, justify='left').pack(pady=5, padx=20, fill='x')
        
        view.pack(expand=True, padx=20, pady=50)
        return view

# Fixed: Moved functions outside of class
def selectCategory(category):
    global category_label, category_buttons, selected_category
    selected_category = category
    category_label.pack_forget()
    for button in category_buttons:
        button.pack_forget()
    askQuestion()

def startQuiz():
    global welcome_label, start_button
    welcome_label.pack_forget()
    start_button.pack_forget()
    askQuestion()

def askQuestion():
    global questions, window, index, right, number_of_questions, selected_category
    
    if selected_category is None:
        # Display category selection
        category_label.pack(pady=50)
        for button in category_buttons:
            button.pack(pady=10)
        return
    
    if index >= len(questions[selected_category]) - 1:
        # Quiz finished
        result_text = f"Quiz Complete!\nYou got {right} out of {number_of_questions} questions correct!"
        Label(window, text=result_text, font=("Helvetica", 24), 
              bg='black', fg='yellow').pack(pady=50)
        
        # Restart button
        Button(window, text="Play Again", command=restartQuiz, 
               font=("Helvetica", 20), bg='blue', fg='white').pack(pady=20)
        return
    
    index += 1
    current_question = questions[selected_category][index]
    current_question.getView(window)

def restartQuiz():
    global index, right, selected_category
    # Clear the window
    for widget in window.winfo_children():
        if widget != background_label:  # Keep background
            widget.pack_forget()
    
    # Reset variables
    index = -1
    right = 0
    selected_category = None
    
    # Show welcome screen again
    welcome_label.pack(pady=(window.winfo_height() - 200) // 2)
    start_button.pack(pady=20)

# Fixed question data with correct answer indices
questions = {
    "General Knowledge": [
        Question("General Knowledge", "What is the capital of France?", 
                ["Paris", "London", "Berlin", "Madrid"], "A"),
        Question("General Knowledge", "What is the largest mammal?", 
                ["Blue Whale", "Elephant", "Giraffe", "Great White Shark"], "A"),
        Question("General Knowledge", "Which planet is known as the Red Planet?", 
                ["Earth", "Mars", "Jupiter", "Saturn"], "B"),
        Question("General Knowledge", "What is the chemical symbol for water?", 
                ["H2O", "CO2", "O2", "NaCl"], "A"),
        Question("General Knowledge", "Who wrote 'Romeo and Juliet'?", 
                ["Mark Twain", "William Shakespeare", "Charles Dickens", "Jane Austen"], "B"),
        Question("General Knowledge", "What is the smallest bone in the human body?", 
                ["Stapes", "Femur", "Tibia", "Fibula"], "A"),
        Question("General Knowledge", "Which country is known as the Land of the Rising Sun?", 
                ["China", "Japan", "South Korea", "Thailand"], "B"),
        Question("General Knowledge", "What is the national flower of India?", 
                ["Rose", "Lotus", "Sunflower", "Lily"], "B"),
        Question("General Knowledge", "Who is known as the father of Computers?", 
                ["Charles Babbage", "Alan Turing", "Bill Gates", "Steve Jobs"], "A"),
        Question("General Knowledge", "Which gas is most abundant in Earth's atmosphere?", 
                ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "B"),
    ],
    "History": [
        Question("History", "Who was the first President of the United States?", 
                ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"], "A"),
        Question("History", "In which year did World War I begin?", 
                ["1912", "1914", "1918", "1920"], "B"),
        Question("History", "Which ancient civilization built the pyramids?", 
                ["Mesopotamians", "Egyptians", "Greeks", "Romans"], "B"),
        Question("History", "Who was the leader of the Soviet Union during the Cuban Missile Crisis?", 
                ["Nikita Khrushchev", "Leonid Brezhnev", "Joseph Stalin", "Vladimir Lenin"], "A"),
        Question("History", "What was the capital of the Byzantine Empire?", 
                ["Constantinople", "Athens", "Rome", "Cairo"], "A"),
        Question("History", "Who was the last emperor of Russia?", 
                ["Nicholas II", "Alexander III", "Peter the Great", "Catherine the Great"], "A"),
        Question("History", "In which year did Christopher Columbus discover America?", 
                ["1492", "1498", "1500", "1510"], "A"),
        Question("History", "Who was the last queen of France?", 
                ["Marie Antoinette", "Catherine de Medici", "Elizabeth I", "Anne Boleyn"], "A"),
        Question("History", "Which ancient civilization built Machu Picchu?", 
                ["Aztecs", "Mayans", "Incas", "Olmecs"], "C"),
        Question("History", "Who wrote the Communist Manifesto?", 
                ["Karl Marx", "Friedrich Engels", "Vladimir Lenin", "Leon Trotsky"], "A"),
    ],
    "Movies": [
        Question("Movies", "Who directed the movie 'Titanic'?", 
                ["James Cameron", "Steven Spielberg", "Martin Scorsese", "Christopher Nolan"], "A"),
        Question("Movies", "Which movie won the Academy Award for Best Picture in 2020?", 
                ["Parasite", "1917", "Once Upon a Time in Hollywood", "Joker"], "A"),
        Question("Movies", "Who played the lead role in 'The Godfather'?", 
                ["Al Pacino", "Marlon Brando", "Robert De Niro", "Jack Nicholson"], "B"),
        Question("Movies", "Which actor portrayed Iron Man in the Marvel Cinematic Universe?", 
                ["Chris Hemsworth", "Chris Evans", "Robert Downey Jr.", "Mark Ruffalo"], "C"),
        Question("Movies", "Which movie features the character Darth Vader?", 
                ["Star Wars", "Star Trek", "The Matrix", "Blade Runner"], "A"),
        Question("Movies", "Who directed the movie 'Pulp Fiction'?", 
                ["Quentin Tarantino", "Martin Scorsese", "Steven Spielberg", "Christopher Nolan"], "A"),
        Question("Movies", "Which actor portrayed Neo in 'The Matrix'?", 
                ["Keanu Reeves", "Hugo Weaving", "Laurence Fishburne", "Carrie-Anne Moss"], "A"),
        Question("Movies", "Who won the Academy Award for Best Actor for 'The Revenant'?", 
                ["Leonardo DiCaprio", "Matthew McConaughey", "Eddie Redmayne", "Joaquin Phoenix"], "A"),
        Question("Movies", "Who played the Joker in 'The Dark Knight'?", 
                ["Heath Ledger", "Jared Leto", "Jack Nicholson", "Joaquin Phoenix"], "A"),
        Question("Movies", "Who directed 'The Shawshank Redemption'?", 
                ["Frank Darabont", "Steven Spielberg", "Martin Scorsese", "Christopher Nolan"], "A"),
    ]
}

# Initialize global variables
index = -1
right = 0
number_of_questions = 10  # Number of questions per category
selected_category = None

# Create main window
window = Tk()
window.title("Quiz Game")
window.configure(bg='black')

# Initialize pygame mixer for sounds (optional)
try:
    pygame.mixer.init()
    # Try to load sound files if they exist
    if os.path.exists("correct.wav"):
        correct_sound = pygame.mixer.Sound("correct.wav")
    if os.path.exists("incorrect.wav"):
        incorrect_sound = pygame.mixer.Sound("incorrect.wav")
except:
    print("Sound files not found or pygame not available. Running without sound.")

# Set window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
window.geometry(f"{window_width}x{window_height}")

# Try to load background image (optional)
background_label = None
try:
    if os.path.exists("background.png"):
        from tkinter import PhotoImage
        background_image = PhotoImage(file="background.png")
        background_label = Label(window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    print("Background image not found. Using solid color background.")

# Create welcome screen
welcome_label = Label(window, text="Welcome to the Quiz!", 
                     font=("Comic Sans MS", 36), bg='black', fg='cyan')
welcome_label.pack(pady=(window_height - 200) // 2)

start_button = Button(window, text="Start Quiz", command=startQuiz, 
                     font=("Helvetica", 24), bg='green', fg='white')
start_button.pack(pady=20)

# Create category selection elements
category_label = Label(window, text="Select a Category", 
                      font=("Comic Sans MS", 36), bg='black', fg='cyan')

category_buttons = []
for category in questions.keys():
    btn = Button(window, text=category, 
                command=lambda c=category: selectCategory(c),
                font=("Helvetica", 24), bg='blue', fg='white')
    category_buttons.append(btn)

# Start the GUI
window.mainloop()