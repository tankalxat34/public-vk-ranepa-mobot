"""
ФАЙЛ ДЛЯ ИНИЦИАЛИЗАЦИИ ХЕНДЛЕРОВ НА КОНКРЕТНЫЕ СООБЩЕНИЯ ОТ ПОЛЬЗОВАТЕЛЯ
"""

class Handler:
    def __init__(self, text: str, trigger_message: str, function) -> None:
        """Добавляет хендлер для всех сообщений text, имеющих текст trigger_message и выполняющих функцию function при получении такого текста"""
        self.text = text.lower()
        self.trigger_message = trigger_message.lower()
        self.function = function
    
    def add(self):
        """Добавляет реакцию на message функцией function"""
        if self.text == self.trigger_message:
            self.function()
        
