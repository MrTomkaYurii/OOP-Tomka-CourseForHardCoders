# Генератор діаграм для Розділу 21 (Generic Host & Dependency Injection)

Ця папка містить вихідний код і генератор діаграм для розділу 21 курсу.

Діаграми побудовані на основі чистого **HTML5 + CSS3 (Flexbox/Grid) + SVG** і рендеряться у високій якості через headless Microsoft Edge (Chromium).

## Файли та діаграми
1. `21-01/host-architecture.png` — Архітектура `IHost`, три кити інфраструктури, Hosted Services та життєвий цикл.
2. `21-02/service-registration.png` — Реєстрація (`IServiceCollection`), `.Build()`, резолв (`IServiceProvider`), дескриптори та `GetService` vs `GetRequiredService`.
3. `21-03/service-lifetimes.png` — Времена життя (`Singleton`, `Scoped`, `Transient`), матриця вибору, пастки Captive Dependency та рішення через `IServiceScopeFactory`.
4. `21-04/options-pattern.png` — Паттерн Options (`IOptions`, `IOptionsSnapshot`, `IOptionsMonitor`), зв'язування з `IConfiguration`, C# код і шпаргалка вибору.

---

## Використання

### 1. Звичайна генерація (в кольорах сайту tomka.space):
```bash
python generate_diagrams.py
```

### 2. Чорно-біла монохромна генерація (для друкованої книги):
```bash
python generate_diagrams.py --bw
```
Режим `--bw` автоматично перемикає тему на білий фон з глибокими чорними контрастними рамками, поліграфічними шрифтами та чіткими лініями, оптимізованими для друку на папері.

---

## Налаштування кольорової гами
У файлі `generate_diagrams.py` функція `get_theme_css(is_bw)` містить CSS-змінні:
- `--bg-page`: фоновий колір
- `--card-bg`: фон карток
- `--accent`: основний смарагдовий/акцентний колір
- `--accent-blue`, `--accent-yellow`, `--accent-purple`, `--accent-red`: акцентні кольори для бейджів та блоків
