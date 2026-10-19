from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

quiz_data = {
    "Matematika": [
        {"q": "Berapa hasil dari 12 x 5?", "options": ["50", "60", "70", "55"], "ans": 1},
        {"q": "Akar kuadrat dari 144 adalah...", "options": ["10", "11", "12", "14"], "ans": 2}
    ],
    "Informasi": [
        {"q": "Siapa penemu lampu pijar?", "options": ["Nikola Tesla", "Thomas Edison", "Albert Einstein", "Galileo"], "ans": 1},
        {"q": "Apa ibu kota negara Jepang?", "options": ["Seoul", "Beijing", "Tokyo", "Kyoto"], "ans": 2}
    ],
    "B. Indo": [
        {"q": "Sinonim dari kata 'haus' adalah...", "options": ["Dahaga", "Lapar", "Lelah", "Senang"], "ans": 0},
        {"q": "Penulisan huruf kapital yang benar terdapat pada...", "options": ["di jakarta", "Di Jakarta", "di Jakarta", "Di jakarta"], "ans": 1}
    ]
}

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text="PILIH KATEGORI KUIS", font_size=22, bold=True))
        
        for cat in quiz_data.keys():
            btn = Button(text=cat, font_size=18, background_color=(0.2, 0.6, 0.8, 1))
            btn.bind(on_press=lambda x, c=cat: self.start_quiz(c))
            layout.add_widget(btn)
            
        self.add_widget(layout)
        
    def start_quiz(self, category):
        quiz_screen = self.manager.get_screen('quiz')
        quiz_screen.load_category(category)
        self.manager.current = 'quiz'

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.timer_label = Label(text="Waktu: 10 detik", font_size=16, color=(1, 0, 0, 1))
        self.layout.add_widget(self.timer_label)
        
        self.q_label = Label(text="", font_size=18, halign='center', text_size=(300, None))
        self.layout.add_widget(self.q_label)
        
        self.options_layout = BoxLayout(orientation='vertical', spacing=10)
        self.layout.add_widget(self.options_layout)
        
        self.add_widget(self.layout)
        
        self.category = None
        self.q_index = 0
        self.score = 0
        self.time_left = 10
        self.timer_event = None

    def load_category(self, cat):
        self.category = cat
        self.q_index = 0
        self.score = 0
        self.next_question()

    def next_question(self):
        if self.timer_event:
            self.timer_event.cancel()
            
        questions = quiz_data[self.category]
        if self.q_index < len(questions):
            q_data = questions[self.q_index]
            self.q_label.text = f"Soal {self.q_index+1}: {q_data['q']}"
            
            self.options_layout.clear_widgets()
            for i, opt in enumerate(q_data['options']):
                btn = Button(text=opt, font_size=16)
                btn.bind(on_press=lambda x, ans=i: self.check_answer(ans))
                self.options_layout.add_widget(btn)
                
            self.time_left = 10
            self.timer_label.text = f"Waktu: {self.time_left} detik"
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        else:
            score_screen = self.manager.get_screen('score')
            score_screen.set_score(self.score, len(questions) * 10)
            self.manager.current = 'score'

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Waktu: {self.time_left} detik"
        if self.time_left <= 0:
            self.check_answer(-1)

    def check_answer(self, selected_ans):
        if self.timer_event:
            self.timer_event.cancel()
            
        questions = quiz_data[self.category]
        correct_ans = questions[self.q_index]['ans']
        
        if selected_ans == correct_ans:
            self.score += 10
            
        self.q_index += 1
        self.next_question()

class ScoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.score_label = Label(text="", font_size=20, halign='center')
        self.layout.add_widget(self.score_label)
        
        btn_back = Button(text="Kembali ke Menu Utama", font_size=16)
        btn_back.bind(on_press=self.back_to_menu)
        self.layout.add_widget(btn_back)
        
        self.add_widget(self.layout)

    def set_score(self, score, max_score):
        self.score_label.text = f"Kuis Selesai! 🎉\nSkor Kamu: {score} dari {max_score}"

    def back_to_menu(self, instance):
        self.manager.current = 'menu'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(ScoreScreen(name='score'))
        return sm

if __name__ == '__main__':
    MyApp().run()

