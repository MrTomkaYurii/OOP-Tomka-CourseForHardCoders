# Git & GitHub: Практичний воркшоп

> **Перед Lab-01.** Цей воркшоп — єдине що потрібно знати про Git для виконання всіх 22 лабораторних.  
> Ніяких попередніх знань не потрібно.

## Мета

Після цього воркшопу ти вмієш:

- Клонувати репозиторій і орієнтуватись у його структурі
- Створювати гілку для кожної лаби та правильно її називати
- Робити коміти з правильним форматом повідомлення
- Зливати лабу в `main` і переходити до наступної
- Пушити роботу на GitHub

---

## Частина 1. Архітектура Git

Git розбиває твою роботу на **чотири зони**. Зрозуміти їх — значить зрозуміти Git.

![Чотири зони Git](_assets/git-zones.png)

| Зона | Що тут живе | Ключова команда |
|------|-------------|-----------------|
| Working Directory | Файли які ти редагуєш | `git status` |
| Staging Area | Зміни підготовлені до коміту | `git add` |
| Local Repository | Зафіксована історія (`.git/`) | `git commit` |
| Remote (GitHub) | Твоя копія на сервері | `git push / pull` |

Важливо: `git add` не зберігає зміни назавжди — він лише переміщує їх до Staging. Тільки `git commit` фіксує знімок назавжди в локальному репо.

### Крок 1. Встановлення Git

Завантаж з [git-scm.com](https://git-scm.com/downloads) та встанови (всі налаштування за замовчуванням).

Перевірка:

```bash
git --version
# git version 2.x.x
```

### Крок 2. Налаштування імені та email

Git підписує кожен коміт твоїм іменем. Виконай один раз:

```bash
git config --global user.name "Іван Петренко"
git config --global user.email "ivan.petrenko@gmail.com"
```

Перевірка:

```bash
git config --list
# user.name=Іван Петренко
# user.email=ivan.petrenko@gmail.com
```

### Крок 3. Клонування репозиторію курсу

```bash
git clone https://github.com/<викладач>/OOP-Tomka-CourseForHardCoders.git
cd OOP-Tomka-CourseForHardCoders
```

`git clone` — це **одноразова** операція. Вона завантажує весь репозиторій разом з повною історією комітів. Після цього у тебе є локальна копія з якою можна працювати без інтернету.

```bash
git status
# On branch main
# nothing to commit, working tree clean
```

---

## Частина 2. Що таке коміт і гілка

Перш ніж створювати гілки — треба розуміти що вони собою являють.

![Що таке коміт і гілка](_assets/commit-chain.png)

### Коміт — не різниця файлів, а знімок

Кожен коміт — це об'єкт із чотирма полями:

- **SHA** — унікальний 40-символьний хеш (ідентифікатор)
- **tree** — посилання на знімок усіх файлів проєкту в цей момент
- **parent** — SHA попереднього коміту (так формується ланцюжок)
- **message** — твоє повідомлення

Коміт **незмінний**. Якщо змінити повідомлення — Git створить новий коміт з новим SHA. Старий залишиться в базі.

### Гілка — просто pointer

Гілка — це файл із 41 байтом: SHA коміту на який вона вказує. Створити гілку дешево і безпечно — файли не копіюються.

```
main     → a3f82c1  (вказує на "Initial commit")
Lab-01   → 3a4b5c6  (вказує на "Lab01 Task03: Doctor")
HEAD     → Lab-01   (вказує на поточну гілку)
```

`HEAD` — це завжди поточне місце де ти знаходишся. Коли робиш `git checkout Lab-01`, HEAD переміщується на гілку Lab-01.

### Крок 4. Перша гілка

```bash
# Переконайся що ти на main
git checkout main

# Створи гілку для Lab-01 і одразу перейди на неї
git checkout -b Lab-01
```

Прапор `-b` означає "create + checkout". Після цього:

```bash
git branch
# * Lab-01
#   main
```

Зірочка показує поточну гілку.

### Крок 5. Перевірка стану

```bash
git status
# On branch Lab-01
# nothing to commit, working tree clean
```

Тепер усі зміни які ти будеш робити — потраплять в гілку `Lab-01`, а не в `main`.

---

## Частина 3. Workflow курсу

Кожна лаба — один цикл. Подивись на структуру всього курсу:

![Workflow курсу](_assets/branch-topology.png)

Як видно з графа: `main` — стабільна лінія. Кожна лаба — окрема гілка яка відходить від `main`, набирає коміти (по одному на завдання) і зливається назад. Після злиття одразу стартує наступна лаба.

### Формат коміту

Усі коміти в курсі дотримуються одного шаблону:

```
Lab01 Task01: коротко що зроблено
```

- `Lab01` — номер лаби (без дефіса, дві цифри)
- `Task01` — номер завдання (дві цифри)
- `: ` — двокрапка і пробіл
- Далі — дієслово + що: `add Patient class`, `implement GetCost`, `fix null check`

**Приклади:**

```
Lab01 Task01: add Hello World console output
Lab03 Task02: add Patient class with properties
Lab17 Task03: configure Fluent API for Doctor with WorkSchedule
```

### Крок 6. Коміт після кожного завдання

```bash
# Подивись що змінилось
git status
git diff

# Додай файли до staging
git add src/

# Зафіксуй
git commit -m "Lab01 Task01: add Hello World console output"
```

Переглянь результат:

```bash
git log --oneline
# 3a4b5c6 Lab01 Task01: add Hello World console output
# a1b2c3d Initial commit
```

Роби так після **кожного завдання** — один `git commit` на одне завдання.

### Крок 7. Завершення лаби — злиття в main

Виконав усі завдання? Зливай в `main`:

```bash
# Перейди на main
git checkout main

# Злий гілку Lab-01 (--no-ff зберігає топологію гілки в графі)
git merge --no-ff Lab-01 -m "Merge Lab-01: Intro to C#"
```

Прапор `--no-ff` (no fast-forward) важливий: він створює явний merge-коміт навіть якщо злиття можна зробити лінійно. Завдяки цьому в `git log --graph` видно де починалась і де закінчилась кожна лаба.

Перевір результат:

```bash
git log --oneline --graph --all
# *   c8d9e0f Merge Lab-01: Intro to C#
# |\
# | * 3a4b5c6 Lab01 Task03: add Doctor class
# | * 2b3c4d5 Lab01 Task02: add Patient class
# | * 1a2b3c4 Lab01 Task01: add Hello World
# |/
# * a1b2c3d Initial commit
```

### Крок 8. Перехід до наступної лаби

Відразу після злиття:

```bash
git checkout -b Lab-02
```

Готово — Lab-02 стартує з чистого `main`.

---

## Частина 4. Merge vs Rebase

Під час роботи над лабою може виникнути ситуація: `main` пішов вперед (наприклад, викладач запушив нові файли) поки ти виконував завдання. Потрібно синхронізуватись.

![Merge vs Rebase](_assets/merge-vs-rebase.png)

### git merge main — зберігає топологію

```bash
git checkout Lab-01
git merge main
```

Створює **merge-коміт** який об'єднує дві лінії розробки. Граф набуває форми "ромба" — видно точний момент злиття. Це підхід який ми використовуємо для фінального злиття лаби в `main`.

### git rebase main — переписує поверх

```bash
git checkout Lab-01
git rebase main
```

Git "від'єднує" твої коміти `E` і `F`, застосовує нові коміти `C` і `D` з main, а потім "перекладає" твої коміти зверху. Результат: `E'` і `F'` з **новими SHA**. Стара `E` і `F` видаляються.

Плюс: лінійна, чиста історія.  
**Правило:** ніколи не робити `rebase` на гілці яку вже запушив і яку бачать інші. Rebase переписує SHA — у колег виникнуть конфлікти.

**Коли rebase доречний:** локальне прибирання комітів перед PR, `git rebase -i` для squash/reorder.

### Для курсу

У більшості випадків rebase не знадобиться — ти єдиний хто працює у своєму форку. Якщо викладач оновив репо — просто:

```bash
git checkout main
git pull origin main
git checkout Lab-01
git merge main   # або git rebase main — на свій розсуд
```

---

## Частина 5. Push на GitHub

### Крок 9. Запуши main після кожного злиття

```bash
git push origin main
```

### Крок 10. Запуши поточну лабу (для бекапу і перевірки)

```bash
git push origin Lab-01
```

Перша пуш гілки — можна скоротити через флаг `-u`:

```bash
git push -u origin Lab-01
# Тепер достатньо просто: git push
```

Переглянути що запушено:

```bash
git branch -r
# origin/main
# origin/Lab-01
# origin/Lab-02
```

---

## Типові помилки

### 1. Коміт потрапив у `main` замість `Lab-01`

```bash
# Відмінити останній коміт з main (зміни залишаться в файлах)
git checkout main
git reset --soft HEAD~1

# Перейти на Lab-01 і закомітити там
git checkout Lab-01
git add .
git commit -m "Lab01 Task01: ..."
```

### 2. Забув `git add` — файл не потрапив у коміт

```bash
git status                    # видно що файл не staged
git add src/Models/Patient.cs # додай конкретний файл
git commit --amend --no-edit  # додай до попереднього коміту (якщо ще не пушив)
```

### 3. Неправильний формат коміту

```bash
# Змінити повідомлення останнього коміту (якщо ще не пушив)
git commit --amend -m "Lab01 Task01: add Patient class with properties"
```

### 4. Конфлікт при злитті

```
Auto-merging src/Models/Patient.cs
CONFLICT (content): Merge conflict in src/Models/Patient.cs
```

Відкрий файл — Git позначив конфліктні місця:

```csharp
<<<<<<< HEAD
public string FullName { get; set; }
=======
public string FirstName { get; set; }
public string LastName  { get; set; }
>>>>>>> Lab-01
```

Обери правильний варіант (або об'єднай), видали маркери, потім:

```bash
git add src/Models/Patient.cs
git commit -m "resolve merge conflict in Patient"
```

### 5. Push rejected — remote has changes

```
! [rejected] main -> main (non-fast-forward)
```

Хтось (або ти з іншого комп'ютера) запушив в `main`. Спочатку отримай:

```bash
git pull origin main --rebase
git push origin main
```

---

## Шпаргалка

| Команда | Що робить |
|---------|-----------|
| `git clone <url>` | Скачати репо (одноразово) |
| `git status` | Стан робочої директорії і staging |
| `git diff` | Що змінилось (не staged) |
| `git diff --cached` | Що в staging |
| `git add <path>` | Додати файл/директорію до staging |
| `git add -p` | Додавати по частинах (інтерактивно) |
| `git commit -m "..."` | Зафіксувати зміни |
| `git log --oneline` | Коротка історія комітів |
| `git log --oneline --graph --all` | Граф усіх гілок |
| `git checkout main` | Перейти на гілку main |
| `git checkout -b Lab-01` | Створити гілку і перейти на неї |
| `git branch` | Список гілок (зірочка = поточна) |
| `git merge --no-ff Lab-01 -m "..."` | Злити Lab-01 в поточну гілку |
| `git push origin main` | Запушити main на GitHub |
| `git push -u origin Lab-01` | Запушити гілку і встановити tracking |
| `git pull origin main` | Отримати зміни з GitHub |
| `git stash` | Тимчасово сховати незакомічені зміни |
| `git stash pop` | Відновити сховані зміни |
| `git restore <file>` | Відмінити зміни у файлі (Working Dir) |
| `git restore --staged <file>` | Прибрати файл зі staging |
| `git reset --soft HEAD~1` | Відмінити останній коміт (зміни лишаються) |

---

## Структура гілок у курсі

```
main
├── Lab-01   (Intro to C#)      → merge → main
├── Lab-02   (Arrays)           → merge → main
├── Lab-03   (Classes)          → merge → main
│   ...
├── Lab-17   (EF Core Basics)   → merge → main
├── Lab-18   (EF Relations)     → merge → main
│   ...
└── Lab-22   (SOLID + DI)       → merge → main
```

Кожна гілка: `Lab-XX` з великої літери, дві цифри, дефіс.  
Кожен коміт: `LabXX TaskXX: дієслово + що зроблено`.
