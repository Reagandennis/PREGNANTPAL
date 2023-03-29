from os import name
from scrollable_frame import ScrollableFrame
import re
import random
import tkinter as tk


class ChatWindow(tk.Toplevel):
    greetings = (
        "hello",
        "hi",
        "good morning",
    )
    labour = (
        "is labour painful",
        "what are the signs of labour",
        "what to do when in labour"
    )
    show = (
        "what is show",
        "blood",
        "blood show",
        "reddish pinkish discharge"
    )
    vaginal_bleeding = (
       "i am bleeding from my vagina",
        "i am bleeding what can i do",
        "blood is coming from my vagina",
        "i have blood on my cloth"
    )
    itchy = (
        "i am experiencing itchiness over my sole and palm",
        "itchy hands and feet",
        "scratchy palm and legs",
        "itchy hands and sole"
    )
    fever = (
        "i have a fever"
        "i have a very high body temperature",
        "my temperature is higher than normal"
    )
    morning_sickness = (
        "what is morning sickness",
        "what are the signs of morning sickness"
    )
    sleeping_position = (
        "How do i sleep",
        "what is the best sleeping position when pregnant",
        "can i sleep on my belly",
        "can i sleep on my back"
    )
    left_side = (
        "why should i sleep on my left side",
        "what are the benefits of sleeping on my left side",
        "why left"
        "why left side"
    )
    stretchmarks = (
        "how do i get rid of stretchmarks",
        "how do i prevent stretchmarks",
        "can i use cream to clear stretchmarks"
    )
    swelling_feet = (
        "i have swelling feet",
        "i am experiencing swelling on my feet",
        "what can i do to prevent my feet from swelling",
        "what is edema"
    )
    contractions = (
        "how do contractions feel like",
        "what are contractions",
        "how long does contractions last"
    )
    false_labour = (
        "what is false labour",
        "how do you differentiate between true and false labour"
    )
    braxton_hicks = (
        "what is braxton hicks",
        "tell me about braxton hicks contractions",
        "braxton hicks",
        "are there painless contractions"
    )
    weight = (
        "advice to avoid gaining too much weight",
        "what whats the recommended weight in pregnancy",
        "what should i do to reduce weight",
        "what are the dangers associated with less weight gain",
        "what are the dangers associated with over weight gain in pregnancy"
    )
    exercise = (
        "what exercises can i do",
        "what exercises are good for pregnant women",
        "what exercises do you recommend for a pregnant lady",
        "what exercises can you do at home while pregnant"
    )
    caffeine = (
        "i cant function without my morning coffee please advice",
        "to what limit should my caffeine intake be",
        "should i take coffee",
        "is caffeine bad for a pregnant woman",
        "how many cups of coffee should i take as a pregnant woman"
    )
    calories = (
        "do you really need extra calories while pregnant",
        "how many calories should i eat while pregnant",
        "how much calorie deficit during pregnancy",
        "how much calories does one need during pregnancy"
    )
    fish = (
        "what type of fish should i eat?",
        "should i eat fish"
        "is fish harmful to a pregnant woman"
    )
    abdominal = (
        "I feel pain in my stomach",
        "I feel pain in my abdomen"
    )
    negative_responses = (
        "no",
        "nope",
        "nah",
        "naw",
        "not a chance",
        "sorry"
    )
    exit_commands = (
        "quit",
        "pause",
        "exit",
        "goodbye",
        "bye",
        "later"
    )
    random_questions = (
        "What trimester are you in?"
        "How are you feeling?"

    )

    def __init__(self, master):
        super().__init__(master)

        self.protocol('WM_DELETE_WINDOW', master.destroy)

        self.alienbabble = {'describe_pain_intent': r'.*\s*your planet.*',
                            'answer_why_intent': r'why\sare.*',
                            'cubed_intent': r'.*cube.*(\d+)'
                            }

        self.resizable(False, False)
        self.geometry('300x400')
        self.transient(master)

        self.rowconfigure(0, weight=1)

        self.convo = ScrollableFrame(self, width=400)
        self.convo.grid(row=0, column=0, sticky='nsew')

        self.bar = tk.Frame(self)

        self.btnpressed = tk.BooleanVar(self, name='btn')
        self.msg = tk.Entry(self.bar, width=24, font=(None, 12))

        self.btn = tk.Button(self.bar, text="SEND",
                             width=4, command=self.send_msg)

        self.msg.pack(side=tk.LEFT)
        self.btn.pack(side=tk.LEFT)
        self.bar.grid(row=1, column=0, sticky='ew')

        self.greeted = False
        self.greet()

    def send_msg(self):
        message = self.msg.get()
        tk.Message(self.convo.window, text=message, bg="#eee",
                   width=256).grid(sticky='e', pady=5)
        self.btnpressed.set(True)
        self.chat(message)

    def greet(self):
        tk.Message(self.convo.window, width=256,
                   text="Hello there, what's your name?", bg="#eee").grid(sticky='w')

        self.wait_variable('btn')

        will_help = "Hi {} I'm Pregnantpal, nice to meet you.".format(
            self.msg.get())

        tk.Message(self.convo.window, width=256,
                   text=will_help, bg="#eee").grid(sticky='w')

        self.wait_variable('btn')

        if self.msg.get() in ChatWindow.negative_responses:
            tk.Message(self.convo.window, width=256,
                       text="Okay, have a lovely day!", bg="#eee").grid(sticky='w')
            self.after(1000, self.master.destroy)
            return

        tk.Message(self.convo.window, width=256,
                   text=random.choice(self.random_questions), bg="#eee").grid(sticky='w')
        self.greeted = True

    def make_exit(self, reply):
        if reply in ChatWindow.exit_commands:
            tk.Message(self.convo.window, width=256,
                       text="Okay, have a nice day!", bg="#eee").grid(sticky='w')
            self.after(10, self.master.destroy)

        return False

    def chat(self, message):
        if not self.greeted:
            return
        reply = message

        if not self.make_exit(reply):
            tk.Message(self.convo.window, width=256,
                       text=self.match_reply(reply), bg="#eee").grid(sticky='w')

    def match_reply(self, reply):
        for key, value in self.alienbabble.items():
            intent = key
            regex_pattern = value
            found_match = re.match(regex_pattern, reply)
            if found_match and intent == "describe_yourself_intent":
                return self.describe_yourself_intent()
            elif found_match and intent == "answer_why_intent":
                return self.answer_why_intent()
            elif found_match and intent == "cubed_intent":
                return self.cubed_intent()
            elif found_match and intent == "greetings_intent":
                return self.greetings_intent()
            elif found_match and intent == "labour_intent":
                return self.labour_intent()
            elif found_match and intent == "show_intent":
                return self.show_intent()
            elif found_match and intent == "vaginal_bleeding_intent":
                return self.vaginal_bleeeding_intent()
            elif found_match and intent == "itchy_intent":
                return self.itchy_intent()
            elif found_match and intent == "fever_intent":
                return self.fever_intent()
            elif found_match and intent == "morning_sickness_intent":
                return self.mornimg_sickness_intent()
            elif found_match and intent == "sleeping_position_intent":
                return self.sleeping_position_intent()
            elif found_match and intent == "left_side_intent":
                return self.left_side_intent()

            elif found_match and intent == "abdominal_responses":
                return self.abdominal_responses(found_match.groups()[0])
            else:
                return self.no_match_intent()

    def describe_yourself_intent(self):
        responses = (
                     "I am PREGNANTPAL, a pregnancy bot here to help you through your pregnancy."
        )
        return random.choice(responses)

    def answer_why_intent(self):
        responses = ("I come to ease your pregnancy journey",
                     "I am here to collect data on you and help you best i can",
                     "I lend a helping hand to pregnant women",
                     "Just checking on you and the baby :)"
                     )
        return random.choice(responses)

    def cubed_intent(self, number):
        return "Cubed Number is {}, is there anything else I can help you with?".format(int(number)**3)

    def abdominal_responses(self):
        responses = (
            "There's no abdominal pain in pregnancy, when experienced seek fast medical assistant."
        )
        return random.choice(responses)

    def no_match_intent(self):
        responses = (

            "Please tell me more.",
        )
        return random.choice(responses)


if __name__ == "__main__":
    win = ChatWindow()
    win.mainloop()
