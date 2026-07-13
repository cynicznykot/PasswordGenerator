# 🔐 Персональный Генератор Паролей

**Безопасное и удобное приложение для генерации паролей с графическим интерфейсом, индикатором сложности и сохранением в файл.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen.svg)](tests/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)]()

---

## 📖 Оглавление

- [О проекте](#о-проекте)
- [Возможности](#возможности)
- [Как использовать](#как-использовать)
- [Быстрый старт](#быстрый-старт)
- [Структура проекта](#структура-проекта)
- [Запуск тестов](#запуск-тестов)
- [Технологии](#технологии)
- [Планы по развитию](#планы-по-развитию)
- [Лицензия](#лицензия)
- [Автор](#автор)

---

## О проекте

**"Персональный Генератор Паролей"** — это десктопное приложение на Python с графическим интерфейсом для генерации криптографически безопасных паролей.

Приложение позволяет:
- Генерировать пароли с настраиваемой длиной и набором символов
- Оценивать их сложность в реальном времени
- Сохранять пароли с указанием сервиса и логина

Проект создан для практики:
- Разработки **GUI** на `tkinter`
- **Криптографической безопасности** с модулем `secrets`
- **Модульного тестирования** с `unittest` и `pytest`
- Организации структуры проекта и работы с **Git**

---

## ✨ Возможности

- 🖥️ **Графический интерфейс** — интуитивное окно на `tkinter`
- 🔐 **Безопасная генерация** — используется модуль `secrets` (криптостойкий)
- 📏 **Настройка длины** — от 16 до 64 символов
- 🔤 **Выбор символов** — буквы, цифры, специальные символы
- 📊 **Индикатор сложности** — `Небезопасный` / `Умеренный` / `Очень сильный`
- 📋 **Копирование в буфер** — одно нажатие с визуальным подтверждением
- 💾 **Сохранение в файл** — пароль + сервис + логин/почта
- 📁 **Выбор места сохранения** — пользователь выбирает папку и имя файла
- ✅ **Тесты** — 25 unit-тестов с `pytest`
- 🖥️ **Кроссплатформенность** — работает на Windows, Linux и macOS

---

## Как использовать

### Генерация пароля

1. **Установите длину** с помощью ползунка (16–64 символа)
2. **Выберите типы символов**:
   - ☑️ Буквы
   - ☑️ Цифры
   - ☑️ Символы
3. Нажмите **"Generate Password"**
4. Пароль появится в поле с **индикатором сложности** под ним

### Копирование пароля

- Нажмите **"📋 Copy to clipboard"** — пароль скопируется, появится подтверждение

### Сохранение пароля

1. **Введите название сервиса** (например, `Google`)
2. **Введите логин или почту** (например, `user@gmail.com`)
3. Нажмите **"💾 Save the password to file"**
4. **Выберите место и имя файла** (по умолчанию: `passwords.txt`)
5. Запись сохраняется в формате: Service: Google | Login/email: user@gmail.com | Password: P@ssw0rd!

### Пример работы

Ваш интерфейс будет выглядеть так:

Windows:

![Пример интерфейса](images/screenshot_main_win.png)

![Пример интерфейса](images/screenshot_save_password_win.png)

Linux:

![Пример интерфейса](images/screenshot_main_linux.png)

![Пример интерфейса](images/screenshot_save_password_linux.png)

---

## Быстрый старт

### Требования

- **Python 3.8** или выше
- `pip` (менеджер пакетов Python)

### Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/cynicznykot/PasswordGenerator.git

# Перейдите в папку проекта
cd PasswordGenerator

# Создайте виртуальное окружение (рекомендуется)
python -m venv .venv

# Активируйте виртуальное окружение
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```
### Запуск приложения

```bash
# Через модуль Python
python -m src.main

# Или напрямую через файл
python src/main.py
```

### Возможные проблемы на Linux
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Структура проекта
```bash
PasswordGenerator/
├── src/                   # Исходный код
│   ├── __init__.py        # Пакетный файл
│   ├── generator.py       # Логика генерации и проверки
│   ├── gui.py             # Графический интерфейс (tkinter)
│   └── main.py            # Точка входа
├── tests/                 # Тесты
│   ├── __init__.py
│   ├── test_generator.py  # 25 тестов для логики
│   └── test_gui.py        # 8 тестов для GUI (пропущены)
├── images/                # Скриншоты для README
├── .gitignore             # Игнорируемые файлы Git
├── LICENSE                # Лицензия MIT
├── README.md              # Документация (русский)
├── README.en.md           # Документация (английский)
└── requirements.txt       # Зависимости
```

## Запуск тестов

### Установка зависимостей для разработки 
```bash
pip install -r requirements-dev.txt
```

### Запуск тестов
```bash
# Запустить все тесты
pytest tests/ -v

# Запустить с покрытием кода
pytest tests/ --cov=src --cov-report=html

# Запустить конкретный тест
pytest tests/test_generator.py -v
```

### Результаты тестов
```bash
============================= test session starts ==============================
collected 25 items

tests/test_generator.py::TestBuildCharacterPool::test_all_types PASSED
tests/test_generator.py::TestBuildCharacterPool::test_digits_only PASSED
tests/test_generator.py::TestBuildCharacterPool::test_letters_and_digits PASSED
tests/test_generator.py::TestBuildCharacterPool::test_letters_only PASSED
tests/test_generator.py::TestBuildCharacterPool::test_no_types PASSED
tests/test_generator.py::TestBuildCharacterPool::test_symbols_only PASSED
tests/test_generator.py::TestGeneratePassword::test_empty_pool PASSED
tests/test_generator.py::TestGeneratePassword::test_length_16 PASSED
tests/test_generator.py::TestGeneratePassword::test_length_30 PASSED
tests/test_generator.py::TestGeneratePassword::test_length_64 PASSED
tests/test_generator.py::TestGeneratePassword::test_pool_with_digits_only PASSED
tests/test_generator.py::TestGeneratePassword::test_pool_with_letters_only PASSED
tests/test_generator.py::TestGeneratePassword::test_randomness PASSED
tests/test_generator.py::TestGeneratePassword::test_zero_length PASSED
tests/test_generator.py::TestCheckStrength::test_empty PASSED
tests/test_generator.py::TestCheckStrength::test_moderate_letters_and_digits_16 PASSED
tests/test_generator.py::TestCheckStrength::test_moderate_letters_and_symbols_16 PASSED
tests/test_generator.py::TestCheckStrength::test_score_2 PASSED
tests/test_generator.py::TestCheckStrength::test_score_3 PASSED
tests/test_generator.py::TestCheckStrength::test_score_5 PASSED
tests/test_generator.py::TestCheckStrength::test_strong_all_types_16 PASSED
tests/test_generator.py::TestCheckStrength::test_strong_long_all_types_30 PASSED
tests/test_generator.py::TestCheckStrength::test_weak_only_digits_16 PASSED
tests/test_generator.py::TestCheckStrength::test_weak_only_lowercase_16 PASSED
tests/test_generator.py::TestCheckStrength::test_weak_short PASSED

============================= 25 passed in 0.03s ==============================

============================= test session starts ==============================
collecting ... collected 8 items

test_gui.py::TestGuiVariables::test_length_var_default SKIPPED (GUI
tests are slow, skipping for now)                                        [ 12%]
Skipped: GUI tests are slow, skipping for now

test_gui.py::TestGuiVariables::test_use_digits_default SKIPPED (GUI
tests are slow, skipping for now)                                        [ 25%]
Skipped: GUI tests are slow, skipping for now

test_gui.py::TestGuiVariables::test_use_letters_default SKIPPED (GUI
tests are slow, skipping for now)                                        [ 37%]
Skipped: GUI tests are slow, skipping for now

test_gui.py::TestGuiVariables::test_use_symbols_default SKIPPED (GUI
tests are slow, skipping for now)                                        [ 50%]
Skipped: GUI tests are slow, skipping for now

test_gui.py::TestGuiVariables::test_variables_created SKIPPED (GUI tests
are slow, skipping for now)                                              [ 62%]
Skipped: GUI tests are slow, skipping for now

test_gui.py::TestGuiFunctions::test_copy_password_called SKIPPED (GUI
tests are slow, skipping for now)                                        [ 75%]
Skipped: GUI tests are slow, skipping for now

test_gui.py::TestGuiFunctions::test_on_generate_called SKIPPED (GUI
tests are slow, skipping for now)                                        [ 87%]
Skipped: GUI tests are slow, skipping for now

test_gui.py::TestGuiFunctions::test_save_password_called SKIPPED (GUI
tests are slow, skipping for now)                                        [100%]
Skipped: GUI tests are slow, skipping for now


============================== 8 skipped in 0.02s ==============================
```
### Технологии

- **Python 3.8+** — язык программирования
- **Tkinter** — графический интерфейс
- **Secrets** — криптографическая безопасность
- **Unittest / Pytest** — тестирование
- **Git** — контроль версий

### Планы по развитию

- [x] ✅ **Автоматическая проверка обновлений** — программа проверяет новую версию при запуске.
- [x] ✅ **Улучшенный интерфейс** — обновлённый дизайн на `ttk` и чистый layout.
- [x] ✅ **Сборка для Windows и Linux** — готовые исполняемые файлы для скачивания.
- [ ] 🔜 **Возможность переключения между светлой и тёмной темой интерфейса**.
- [ ] 🔜 **Кнопка «Не напоминать об обновлении»** - возможность отключить уведомления на 24 часа.
- [ ] ⏳ **Просмотр сохранённых паролей** — список всех записей с поиском, сортировкой и фильтрацией.
- [ ] ⏳ **Реализовать поиск по сервисам** — быстрый поиск пароля по названию.
- [ ] ⏳ **Импорт и экспорт паролей** — поддержка форматов `.docx` (Word), `.csv` (Excel/Google Таблицы), `.json` (для переноса данных).
- [ ] ⏳ **Шифрование файла с паролями** — защита данных пользователя.
- [ ] ⏳ **Функция Мастер-пароль** - вход в программу по одному главному паролю - дополнительный уровень безопасности.
- [ ] ⏳ **Собрать `.exe` для macOS** — поддержка всех основных платформ.


### Лицензия

Распространяется под лицензией **MIT**. См. файл [LICENSE](LICENSE) для подробностей.

## Автор

**CynicznyKot**

- GitHub: [@cynicznykot](https://github.com/cynicznykot)
- Проект: [PasswordGenerator](https://github.com/cynicznykot/PasswordGenerator)

---

## Поддержите проект

Если вам понравился мой небольшой проект, поставьте ⭐ на GitHub! Буду очень благодарен! 


