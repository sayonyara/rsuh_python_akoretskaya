import speech_recognition as sr
from gtts import gTTS
import random
from googletrans import Translator
import pygame       #не забыть еще скачать pyaudio

class LanguageAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()       #создаем объект Recognizer из библиотеки sr. который умеет распознавать речь
        self.language_database = [              #база данных с предложениями на разных языках для практики
            {"text": "Привет как дела", "language": "ru"},
            {"text": "Hello how are you", "language": "en"}
        ]
        self.translator = Translator()

    def recognize_speech(self):     #распознавание речи с микрофона
        with sr.Microphone() as source:     #открывает микрофон как source
            print("Скажите что-нибудь:")
            audio = self.recognizer.listen(source)  #listen - метод из Recognizer, записывает звук с микрофона, пока пользователь не перестанет говорить

            try:            #блок try-except возвращающая либо распознанное аудио, либо тексты об ошибках
                text = self.recognizer.recognize_google(audio, language='ru-RU')        #собственно распознавание аудио через гугл и записывание в переменную текст
                return text
            except sr.UnknownValueError:
                return "Извините, не удалось распознать речь"
            except sr.RequestError:
                return "Ошибка сервиса распознавания речи"

    def translate_text(self, text):                      #метод для перевода
        def detect_language(text):          #определение языка введенного текста
            detected_language = self.translator.detect(text)        #detect возвращает объект с разной информацией о тексте
            return detected_language.lang       #из результата метода detect берем информацию о языке

        source_language = detect_language(text)     #распознанный язык записываем как язык-источник
        target_language = 'ru' if source_language == 'en' else 'en'     #если язык-источник англ, то переводим на русский, если язык-источник - любой другой язык, то переводим на английский
        translated_text = self.translator.translate(text, dest=target_language) #собственно переводим текст на определенный выше целевой язык
        return translated_text.text

    def read_text_aloud(self, text):        #зачитай вслух
        #определяем язык введенного текста с помощью googletrans
        return self.translator.detect(text).lang

        language = detect_language(text)    #записываем результат определения в переменную

        if language == 'en':    #устанавливаем язык для gTTS (написала так потому что английский распознает вроде без проблем, а вот русский распознает как угодно (украинский, белорусский), но только не как русский)
            language = 'en'
        else:
            language = 'ru'

        tts = gTTS(text=text, lang=language, slow=False)
        tts.save("output.mp3")

        pygame.init()
        pygame.mixer.init()         #инициализация pygame

        pygame.mixer.music.load("output.mp3")          #загрузка аудио
        pygame.mixer.music.play()           #проигрывание

        while pygame.mixer.music.get_busy():       #get busy возвращает true если файл проигрывается и false если нет.
            pygame.time.Clock().tick(10)        #паузит исполнение чтобы не перегружать процессор (я не особо шарю как и что он конкретно паузит и хз насколько вообще важно эту штуку вставлять было)

        pygame.mixer.quit()         #завершение работы с pygame
        pygame.quit()

        print("Текст был зачитан вслух")

    def practice(self):
        selected_text = random.choice(self.language_database)
        print("Произнесите следующий текст вслух:")
        print(selected_text['text'])
        user_input = self.recognize_speech()            #распознавание с помощью метода описанного выше
        print("Ввод:", user_input)
        if user_input.lower() == selected_text['text'].lower():     #возможно я это доделаю а возможно и нет, но сюда бы еще добавить очистку от знаков препинания в текстах из базы (из-за них не соотносятся строки)
            print("Отлично! Вы правильно воспроизвели текст.")
        else:
            print("Текст был воспроизведен неправильно.")

    def add_text_to_database(self, text, language):                 #пополнение списка текстов
        self.language_database.append({"text": text, "language": language})
        print("Текст успешно добавлен в базу данных.")



assistant = LanguageAssistant()
while True:
    command = input("Введите команду (переведи, зачитай вслух, практика, добавить текст, выход): ")

    if command == "переведи":
        input_text = input("Введите текст для перевода: ")
        translated_text = assistant.translate_text(input_text)
        print("Переведенный текст:", translated_text)
    elif command == "зачитай вслух":
        input_text = input("Введите текст для чтения: ")
        assistant.read_text_aloud(input_text)
    elif command == "практика":
        assistant.practice()
    elif command == "добавить текст":
        input_text = input("Введите текст для добавления в базу данных: ")
        language = input("Введите язык текста (ru/en): ")
        assistant.add_text_to_database(input_text, language)
    elif command == "выход":
        print("Программа завершена.")
        break
    else:
        print("Некорректная команда. Попробуйте снова.")
