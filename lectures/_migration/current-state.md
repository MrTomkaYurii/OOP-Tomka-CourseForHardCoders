# Поточний стан переносу лекцій

Дата фіксації: 2026-05-13

## Принцип переносу

- Джерело: `docx/.NET - OOP.docx`.
- Markdown-лекції зберігаються в `lectures/*.md`.
- Матеріал переноситься 1 в 1 за змістом: без скорочення тексту, без власних додаткових блоків і без переписування стилю автора.
- Дозволені тільки очевидні правки: помилки DOCX-екстракції, зламаний код, очевидні друкарські/мовні помилки, Markdown-адаптація.
- Усі правки фіксуються в `lectures/_migration/transfer-log.md`.
- Рисунки витягнуті в `lectures/assets/docx`; при перенесенні на сайт вони мають бути доступні як публічні assets.

## Перенесено

- `01-vstup.md`
- `02-struktura-programy-zminni-ta-konstanty.md`
- `03-literaly-ta-typy-danykh.md`
- `04-konsolne-vvedennia-vyvedennia.md`
- `05-operatsii-ta-prysvoiennia.md`
- `06-peretvorennia-typiv.md`
- `07-umovni-vyrazy-ta-cykly.md`
- `08-masyvy.md`
- `09-metody-parametry-return.md`
- `10-parametry-ref-out-in-params.md`
- `11-rekursiia-ta-lokalni-funktsii.md`
- `12-switch-ta-enum.md`
- `13-klasy-ta-obiekty.md`
- `14-konstruktory-ta-this.md`
- `15-program-main-ta-top-level-statements.md`
- `16-struktury.md`
- `17-typy-znachen-ta-posylan.md`

## Важливо для наступних кроків

- Не інтегрувати в сайт неперенесені частини як готові лекції.
- Якщо рисунок у DOCX містить код, бажано залишати рисунок і поруч додавати текстову транскрипцію коду, щоб студент міг скопіювати приклад.
- Після інтеграції на сайт перевіряти GitHub Pages base path, бо сайт може публікуватися не з кореня домену.
- Сайт читає атомарні файли з `lectures/sections/`, де один файл відповідає одному підрозділу лекції (`2.1`, `2.2`, `3.1` тощо).
- Великі файли `lectures/01-*.md` ... `lectures/17-*.md` залишаються як перенесені блоки-джерела для звірки.
