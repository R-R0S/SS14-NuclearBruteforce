import pyautogui
import keyboard
import time
import random
import sys
from datetime import datetime


class NuclearBruteForceBot:
    def __init__(self):
        self.running = False
        self.start_x, self.start_y = 0, 0
        self.delay = 0.60
        self.button_hold_time = 0.05
        self.start_int = 0
        self.mode = 2
        self.used_codes = set()
        self.total_codes = 1000000
        self.button_positions = {
            '1': (0, 0), '2': (45, 0), '3': (90, 0),
            '4': (0, 32), '5': (45, 32), '6': (90, 32),
            '7': (0, 64), '8': (45, 64), '9': (90, 64),
            '0': (45, 96), 'E': (90, 96), 'ARM': (135, 64)
        }
        self.log_file = "nuclear_bruteforce.log"
        self.log("Бот инициализирован.")


    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        # print(log_msg)
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(log_msg + "\n")


    def click_button(self, button):
        x = self.start_x + self.button_positions[button][0]
        y = self.start_y + self.button_positions[button][1]
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.mouseDown()
        time.sleep(self.button_hold_time)
        pyautogui.mouseUp()
        time.sleep(self.delay)
        return True


    def generate_unique_random_code(self):
        if len(self.used_codes) >= self.total_codes:
            self.log("Все возможные коды перебраны!")
            return None
        while True:
            code = random.randint(0, 999999)
            if code not in self.used_codes:
                self.used_codes.add(code)
                return code


    def enter_random(self):
        self.record_start_position()
        while self.running and len(self.used_codes) < self.total_codes:
            code = self.generate_unique_random_code()
            if code is None:
                break
            code_str = f"{code:06d}"
            self.log(f"Пробуем код: {code_str} (осталось: {self.total_codes - len(self.used_codes)})")
            try:
                for digit in code_str:
                    self.click_button(digit)
                self.click_button('E')
                self.click_button('ARM')
            except Exception as e:
                self.log(f"Ошибка: {str(e)}")
                self.running = False
                break
            if keyboard.is_pressed('insert'):
                self.running = False
                self.log("Пауза по insert")
                time.sleep(5)
                break


    def enter_code(self, code):
        code_str = f"{code:06d}"
        self.log(f"Пробуем код: {code_str}")
        for digit in code_str:
            if not self.click_button(digit):
                return False
        if not self.click_button('E'):
            return False
        if not self.click_button('ARM'):
            return False
        return True


    def run_sequential(self):
        self.record_start_position()
        for code in range(self.start_int, 1000000):
            if not self.running:
                self.start_int = code
                break
            if not self.enter_code(code):
                self.running = False
                self.start_int = code
                break
            if keyboard.is_pressed('insert'):
                self.running = False
                self.start_int = code
                self.log("Пауза по insert")
                time.sleep(5)
                break


    def record_start_position(self):
        self.log("Подведите курсор к центру кнопки '1' и нажмите Insert")
        while not keyboard.is_pressed('insert'):
            time.sleep(0.1)
        time.sleep(0.5)
        self.start_x, self.start_y = pyautogui.position()
        self.log(f"Стартовая позиция: {self.start_x}, {self.start_y}")


    def toggle(self):
        print("=== Ядерный террорист i_love_Megumin ===")
        self.running = not self.running
        if self.running:
            self.log(f"Задержка: {self.delay}")
            print('Выберите режим работы:')
            print('1 - По порядку')
            print('2 - В случайном порядке')
            try:
                self.mode = int(input('[1/2] (по умолчанию 2): ') or 2)
                if self.mode not in [1, 2]:
                    self.mode = 2
            except:
                self.mode = 2
            self.log(f"Режим: {'последовательный' if self.mode == 1 else 'случайный'}")
            self.log("=== НАЧАЛО ПЕРЕБОРА ===")
            if self.mode == 2:
                self.enter_random()
            else:
                self.run_sequential()
        else:
            self.log("=== ОСТАНОВКА ===")


def main():
    pyautogui.FAILSAFE = True
    bot = NuclearBruteForceBot()
    bot.toggle()
    bot.log("=== РАБОТА ЗАВЕРШЕНА ===")
    sys.exit(0)


if __name__ == "__main__":
    main()