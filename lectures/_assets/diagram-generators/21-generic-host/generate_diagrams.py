#!/usr/bin/env python3
"""
Генератор схем для Розділу 21: Generic Host та Dependency Injection.
Рендерить сучасні векторні діаграми (HTML5 + CSS3 + SVG) через headless Chromium (Microsoft Edge).

Підтримує:
- Тему сайту (темний фон, м'ятно-смарагдовий акцент, палітра tomka.space)
- Монохромний режим для друкованої книги (--bw або --monochrome)

Використання:
  python generate_diagrams.py         # Генерує кандидатів у кольорах сайту
  python generate_diagrams.py --bw    # Генерує чорно-білі варіанти для друку
"""

import os
import sys
import subprocess
import argparse

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

def get_theme_css(is_bw=False):
    if is_bw:
        return """
  :root {
    --bg-page: #ffffff;
    --bg-grad: #ffffff;
    --card-bg: #f7f7f7;
    --card-border: #333333;
    --text-main: #111111;
    --text-muted: #555555;
    --accent: #222222;
    --accent-blue: #333333;
    --accent-yellow: #444444;
    --accent-purple: #333333;
    --accent-red: #000000;
    --code-bg: #eeeeee;
    --code-border: #cccccc;
    --shadow: none;
    --badge-bg: #e0e0e0;
    --badge-text: #111111;
  }
"""
    return """
  :root {
    --bg-page: #0d1210;
    --bg-grad: radial-gradient(ellipse at 50% 0%, #172620 0%, #0a0e0c 80%);
    --card-bg: #141e19;
    --card-border: #283c32;
    --text-main: #f2f5f4;
    --text-muted: #a3b5ad;
    --accent: #76c7ad;
    --accent-blue: #82b9ee;
    --accent-yellow: #f0c977;
    --accent-purple: #dc95d1;
    --accent-red: #e26d6d;
    --code-bg: #0a100d;
    --code-border: #22352c;
    --shadow: 0 8px 24px rgba(0,0,0,0.4);
    --badge-bg: rgba(118, 199, 173, 0.25);
    --badge-text: #76c7ad;
  }
"""

def get_base_css(theme_css):
    return f"""
{theme_css}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg-page);
    background-image: var(--bg-grad);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
    color: var(--text-main);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
  }}
  .code-font {{
    font-family: "Cascadia Code", "JetBrains Mono", Consolas, monospace;
  }}
  .header {{
    text-align: center;
  }}
  .title {{
    font-size: 30px;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -0.5px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
  }}
  .title-tag {{
    font-size: 14px;
    font-weight: 700;
    color: #0a0e0c;
    background: var(--accent);
    padding: 3px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
  }}
  .subtitle {{
    font-size: 16.5px;
    color: var(--text-muted);
    margin-top: 4px;
    font-weight: 400;
  }}
"""

def render_page(html, out_name, w, h):
    tmp_path = os.path.join(SCRIPT_DIR, f"_temp_{out_name}.html")
    png_path = os.path.join(OUTPUT_DIR, out_name)
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(html)
    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={w},{h}",
        f"--screenshot={png_path}",
        f"file:///{tmp_path.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    print(f"  [OK] {out_name} ({w}x{h})")

# ==============================================================================
# 1. HOST ARCHITECTURE
# ==============================================================================
def get_html_1(theme_css):
    base_css = get_base_css(theme_css)
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<style>
{base_css}
  body {{
    width: 1200px;
    height: 1100px;
    padding: 24px 34px;
  }}
  .host-wrap {{
    display: flex;
    justify-content: center;
    position: relative;
    z-index: 2;
  }}
  .host-card {{
    background: #15221d;
    border: 2.5px solid var(--accent);
    border-radius: 16px;
    width: 660px;
    padding: 14px 24px;
    text-align: center;
    box-shadow: 0 0 35px rgba(118, 199, 173, 0.28), 0 8px 25px rgba(0,0,0,0.6);
  }}
  .host-card h2 {{
    font-size: 27px;
    color: var(--accent);
    font-weight: 800;
    letter-spacing: 0.5px;
  }}
  .host-sub {{
    font-size: 15px;
    color: #9cb0a8;
    margin-top: 2px;
    margin-bottom: 6px;
  }}
  .host-methods {{
    font-size: 15.5px;
    font-weight: 600;
    color: #ffffff;
    display: flex;
    justify-content: center;
    gap: 12px;
  }}
  .host-methods span {{
    background: rgba(255,255,255,0.08);
    padding: 3px 10px;
    border-radius: 8px;
    border: 1px solid #30433a;
  }}

  .pillars-row {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
    position: relative;
    z-index: 2;
  }}
  .pillar-card {{
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
  }}
  .pillar-card.blue {{
    border: 2px solid rgba(106, 162, 216, 0.7);
    background: linear-gradient(180deg, rgba(106, 162, 216, 0.14) 0%, rgba(18, 26, 23, 0.98) 100%);
  }}
  .pillar-card.yellow {{
    border: 2px solid rgba(220, 182, 101, 0.7);
    background: linear-gradient(180deg, rgba(220, 182, 101, 0.14) 0%, rgba(18, 26, 23, 0.98) 100%);
  }}
  .pillar-card.purple {{
    border: 2px solid rgba(196, 122, 184, 0.7);
    background: linear-gradient(180deg, rgba(196, 122, 184, 0.14) 0%, rgba(18, 26, 23, 0.98) 100%);
  }}

  .pillar-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    border-bottom: 1px solid #283730;
    margin-bottom: 12px;
  }}
  .pillar-title {{
    font-size: 20px;
    font-weight: 800;
  }}
  .pillar-card.blue .pillar-title {{ color: var(--accent-blue); }}
  .pillar-card.yellow .pillar-title {{ color: var(--accent-yellow); }}
  .pillar-card.purple .pillar-title {{ color: var(--accent-purple); }}

  .pillar-badge {{
    font-size: 12.5px;
    padding: 3px 9px;
    border-radius: 12px;
    font-weight: 700;
  }}
  .pillar-card.blue .pillar-badge {{ background: rgba(106, 162, 216, 0.3); color: #b4d8fa; }}
  .pillar-card.yellow .pillar-badge {{ background: rgba(220, 182, 101, 0.3); color: #fae2aa; }}
  .pillar-card.purple .pillar-badge {{ background: rgba(196, 122, 184, 0.3); color: #f4cbf0; }}

  .pillar-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 11px;
    font-size: 16.5px;
    color: #e2ece8;
    line-height: 1.35;
  }}
  .pillar-list li {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
  }}
  .pillar-list li::before {{
    content: "■";
    font-size: 12px;
    margin-top: 5px;
  }}
  .pillar-card.blue .pillar-list li::before {{ color: var(--accent-blue); }}
  .pillar-card.yellow .pillar-list li::before {{ color: var(--accent-yellow); }}
  .pillar-card.purple .pillar-list li::before {{ color: var(--accent-purple); }}

  .svg-connectors {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1200px;
    height: 1100px;
    pointer-events: none;
    z-index: 1;
  }}

  .services-section {{
    background: rgba(18, 27, 23, 0.88);
    border: 1.5px solid #283931;
    border-radius: 16px;
    padding: 14px 18px;
    position: relative;
    z-index: 2;
  }}
  .services-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
  }}
  .services-title {{
    font-size: 16.5px;
    font-weight: 800;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .services-note {{
    font-size: 14.5px;
    color: #9cb0a8;
  }}
  .services-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }}
  .service-card {{
    background: #141f1a;
    border-radius: 12px;
    padding: 12px 14px;
    border: 2px solid #2d3e36;
  }}
  .service-card .svc-name {{
    font-size: 15.5px;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .service-card .svc-desc {{
    font-size: 14px;
    color: #abbcb5;
    line-height: 1.3;
  }}
  .service-card.c1 {{ border-color: rgba(118, 199, 173, 0.6); }}
  .service-card.c1 .svc-name {{ color: var(--accent); }}
  .service-card.c2 {{ border-color: rgba(106, 162, 216, 0.6); }}
  .service-card.c2 .svc-name {{ color: var(--accent-blue); }}
  .service-card.c3 {{ border-color: rgba(220, 182, 101, 0.6); }}
  .service-card.c3 .svc-name {{ color: var(--accent-yellow); }}
  .service-card.c4 {{ border-color: rgba(196, 122, 184, 0.6); }}
  .service-card.c4 .svc-name {{ color: var(--accent-purple); }}

  .sequence-container {{
    background: #111815;
    border: 1.5px solid #26362f;
    border-radius: 16px;
    padding: 14px 18px;
    position: relative;
    z-index: 2;
  }}
  .seq-head {{
    font-size: 14.5px;
    font-weight: 800;
    color: #94a9a0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
  }}
  .sequence-bar {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
  }}
  .seq-node {{
    background: #15221d;
    border: 1px solid #2e4138;
    border-radius: 12px;
    padding: 10px 12px;
    position: relative;
    display: flex;
    flex-direction: column;
  }}
  .seq-node .seq-step {{
    font-size: 12.5px;
    font-weight: 800;
    color: #8da39a;
    margin-bottom: 3px;
  }}
  .seq-node .seq-name {{
    font-size: 14.5px;
    font-weight: 700;
    margin-bottom: 3px;
    line-height: 1.25;
  }}
  .seq-node .seq-desc {{
    font-size: 13px;
    color: #b2c2bb;
    line-height: 1.3;
  }}
  .seq-node.s1 {{ border-left: 4px solid var(--accent); }}
  .seq-node.s1 .seq-name {{ color: var(--accent); }}
  .seq-node.s2 {{ border-left: 4px solid var(--accent-blue); }}
  .seq-node.s2 .seq-name {{ color: var(--accent-blue); }}
  .seq-node.s3 {{ border-left: 4px solid var(--accent-yellow); }}
  .seq-node.s3 .seq-name {{ color: var(--accent-yellow); }}
  .seq-node.s4 {{ border-left: 4px solid var(--accent); }}
  .seq-node.s4 .seq-name {{ color: #ffffff; }}
  .seq-node.s5 {{ border-left: 4px solid var(--accent-purple); }}
  .seq-node.s5 .seq-name {{ color: var(--accent-purple); }}

  .seq-node:not(:last-child)::after {{
    content: "➔";
    position: absolute;
    right: -11px;
    top: 50%;
    transform: translateY(-50%);
    color: #4b6459;
    font-size: 16px;
    font-weight: 900;
    z-index: 5;
  }}
</style>
</head>
<body>
  <svg class="svg-connectors">
    <path d="M 450 200 C 450 240, 220 220, 220 250" fill="none" stroke="rgba(106, 162, 216, 0.45)" stroke-width="2.5" stroke-dasharray="5,5"/>
    <path d="M 600 200 L 600 250" fill="none" stroke="rgba(220, 182, 101, 0.45)" stroke-width="2.5" stroke-dasharray="5,5"/>
    <path d="M 750 200 C 750 240, 980 220, 980 250" fill="none" stroke="rgba(196, 122, 184, 0.45)" stroke-width="2.5" stroke-dasharray="5,5"/>
  </svg>

  <div class="header">
    <div class="title">
      <span>Generic Host — Архітектура та Життєвий Цикл</span>
      <span class="title-tag">.NET Runtime</span>
    </div>
    <div class="subtitle">Оркестратор залежностей, конфігурації та фонових служб застосунку</div>
  </div>

  <div class="host-wrap">
    <div class="host-card">
      <h2>IHost</h2>
      <div class="host-sub">Головний інтерфейс хоста • Services (IServiceProvider)</div>
      <div class="host-methods code-font">
        <span>StartAsync()</span>
        <span>RunAsync()</span>
        <span>StopAsync()</span>
        <span>Dispose()</span>
      </div>
    </div>
  </div>

  <div class="pillars-row">
    <div class="pillar-card blue">
      <div class="pillar-header">
        <span class="pillar-title">IServiceProvider</span>
        <span class="pillar-badge">DI-контейнер</span>
      </div>
      <ul class="pillar-list">
        <li>Реєстрація та резолв залежностей</li>
        <li>Керування часом життя (Lifetimes)</li>
        <li>Впровадження через конструктор</li>
        <li>Scope-ізоляція та валідація при старті</li>
      </ul>
    </div>

    <div class="pillar-card yellow">
      <div class="pillar-header">
        <span class="pillar-title">IConfiguration</span>
        <span class="pillar-badge">Конфігурація</span>
      </div>
      <ul class="pillar-list">
        <li>Ієрархічні файли appsettings.json</li>
        <li>Змінні середовища та CLI аргументи</li>
        <li>Локальні User Secrets розробника</li>
        <li>Типізоване зв'язування Options Pattern</li>
      </ul>
    </div>

    <div class="pillar-card purple">
      <div class="pillar-header">
        <span class="pillar-title">IHostApplicationLifetime</span>
        <span class="pillar-badge">Життєвий цикл</span>
      </div>
      <ul class="pillar-list">
        <li>Запуск і зупинка IHostedService</li>
        <li>Передача CancellationToken у цикли</li>
        <li>Сигнали: Started, Stopping, Stopped</li>
        <li>Зворотний порядок зупинки служб</li>
      </ul>
    </div>
  </div>

  <div class="services-section">
    <div class="services-header">
      <div class="services-title">
        <span style="color:var(--accent-purple); font-size:19px">⚙</span>
        <span>IHostedService & BackgroundService (Фонові воркери)</span>
      </div>
      <span class="services-note">Керуються хостом • автоматичний запуск при старті</span>
    </div>
    <div class="services-grid">
      <div class="service-card c1">
        <div class="svc-name code-font">AppointmentReminder</div>
        <div class="svc-desc">Періодична розсилка • кожні 24 год</div>
      </div>
      <div class="service-card c2">
        <div class="svc-name code-font">DatabaseMigrator</div>
        <div class="svc-desc">Міграція бази • одноразово при старті</div>
      </div>
      <div class="service-card c3">
        <div class="svc-name code-font">ReportScheduler</div>
        <div class="svc-desc">Нічні звіти • щодня о 23:00</div>
      </div>
      <div class="service-card c4">
        <div class="svc-name code-font">HealthCheckService</div>
        <div class="svc-desc">Моніторинг сервісів • кожні 30 с</div>
      </div>
    </div>
  </div>

  <div class="sequence-container">
    <div class="seq-head">
      Послідовність життєвого циклу (Startup & Shutdown Flow)
    </div>
    <div class="sequence-bar">
      <div class="seq-node s1">
        <div class="seq-step">1. Builder</div>
        <div class="seq-name code-font">CreateDefaultBuilder()</div>
        <div class="seq-desc">Завантаження конфігурацій та логера</div>
      </div>
      <div class="seq-node s2">
        <div class="seq-step">2. DI Setup</div>
        <div class="seq-name code-font">ConfigureServices()</div>
        <div class="seq-desc">Реєстрація типів у IServiceCollection</div>
      </div>
      <div class="seq-node s3">
        <div class="seq-step">3. Start</div>
        <div class="seq-name code-font">host.StartAsync()</div>
        <div class="seq-desc">Послідовний запуск служб (1 ➔ 4)</div>
      </div>
      <div class="seq-node s4">
        <div class="seq-step">4. Running</div>
        <div class="seq-name code-font">host.WaitForShutdown()</div>
        <div class="seq-desc">Робота до сигналу SIGTERM / Ctrl+C</div>
      </div>
      <div class="seq-node s5">
        <div class="seq-step">5. Stop</div>
        <div class="seq-name code-font">host.StopAsync()</div>
        <div class="seq-desc">Зворотна зупинка (4 ➔ 1) + Dispose</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# ==============================================================================
# 2. SERVICE REGISTRATION & RESOLUTION
# ==============================================================================
def get_html_2(theme_css):
    base_css = get_base_css(theme_css)
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<style>
{base_css}
  body {{
    width: 1200px;
    height: 1040px;
    padding: 24px 34px;
  }}
  .content-grid {{
    display: grid;
    grid-template-columns: 1fr 90px 1fr;
    gap: 16px;
    align-items: stretch;
    position: relative;
    z-index: 2;
  }}

  .phase-panel {{
    background: #141d19;
    border: 2px solid #263830;
    border-radius: 16px;
    padding: 16px 20px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .phase-panel.p1 {{ border-color: rgba(118, 199, 173, 0.6); }}
  .phase-panel.p2 {{ border-color: rgba(106, 162, 216, 0.6); }}

  .panel-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    border-bottom: 1px solid #283a32;
  }}
  .panel-title {{
    font-size: 20px;
    font-weight: 800;
  }}
  .panel-badge {{
    font-size: 13px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 12px;
    text-transform: uppercase;
  }}

  .card-item {{
    background: #17241f;
    border-radius: 12px;
    padding: 12px 14px;
    border: 1.5px solid #2f4339;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}
  .card-item.sing {{
    border-color: rgba(118, 199, 173, 0.55);
    background: linear-gradient(135deg, rgba(118, 199, 173, 0.1) 0%, #16221d 100%);
  }}
  .card-item.scpd {{
    border-color: rgba(106, 162, 216, 0.55);
    background: linear-gradient(135deg, rgba(106, 162, 216, 0.1) 0%, #16221d 100%);
  }}
  .card-item.tran {{
    border-color: rgba(220, 182, 101, 0.55);
    background: linear-gradient(135deg, rgba(220, 182, 101, 0.1) 0%, #16221d 100%);
  }}

  .card-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 17px;
    font-weight: 800;
  }}
  .lt-tag {{
    font-size: 12.5px;
    font-weight: 800;
    padding: 3px 9px;
    border-radius: 6px;
  }}
  .lt-sing {{ background: rgba(118, 199, 173, 0.25); color: var(--accent); }}
  .lt-scpd {{ background: rgba(106, 162, 216, 0.25); color: #9bcdfc; }}
  .lt-tran {{ background: rgba(220, 182, 101, 0.25); color: #f5d68d; }}

  .card-body {{
    font-size: 14.5px;
    color: #cad8d3;
    line-height: 1.35;
  }}
  .card-code {{
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    margin-top: 3px;
  }}

  .bridge-col {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }}
  .build-circle {{
    width: 68px;
    height: 68px;
    border-radius: 50%;
    background: #172721;
    border: 2.5px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    font-size: 30px;
    box-shadow: 0 0 25px rgba(118, 199, 173, 0.35);
    margin-bottom: 8px;
  }}
  .build-title {{
    font-size: 16px;
    font-weight: 800;
    color: var(--accent);
  }}
  .build-desc {{
    font-size: 13px;
    color: #a1b2ab;
    margin-top: 4px;
    line-height: 1.3;
  }}

  .anatomy-section {{
    background: #141d19;
    border: 2px solid #283a32;
    border-radius: 16px;
    padding: 16px 20px;
    box-shadow: var(--shadow);
    position: relative;
    z-index: 2;
  }}
  .anatomy-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
  }}
  .anatomy-title {{
    font-size: 17.5px;
    font-weight: 800;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .anatomy-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 15px;
  }}
  .anatomy-table tr {{
    border-bottom: 1px solid #23342d;
  }}
  .anatomy-table tr:last-child {{
    border-bottom: none;
  }}
  .anatomy-table td {{
    padding: 7px 6px;
  }}
  .anatomy-table td.field {{
    color: #92a49d;
    font-weight: 700;
    width: 25%;
  }}
  .anatomy-table td.val {{
    color: #ffffff;
    font-weight: 600;
    width: 35%;
  }}
  .anatomy-table td.comment {{
    color: #9fb0aa;
    font-size: 14px;
    width: 40%;
  }}

  .footer-row {{
    background: #111714;
    border: 1.5px solid #25362e;
    border-radius: 14px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14.5px;
    position: relative;
    z-index: 2;
  }}
  .rule-item {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <span>Реєстрація та Розпізнавання у IServiceCollection</span>
      <span class="title-tag">Dependency Injection</span>
    </div>
    <div class="subtitle">Перехід від списку інструкцій (дескрипторів) до заблокованого Runtime-контейнера</div>
  </div>

  <div class="content-grid">
    <div class="phase-panel p1">
      <div class="panel-header">
        <span class="panel-title" style="color:var(--accent)">Фаза 1: Реєстрація</span>
        <span class="panel-badge" style="background:rgba(118,199,173,0.25); color:var(--accent)">IServiceCollection</span>
      </div>

      <div class="card-item sing">
        <div class="card-top">
          <span style="color:var(--accent)">IPatientRepository</span>
          <span class="lt-tag lt-sing">Singleton</span>
        </div>
        <div class="card-body">
          Реалізація: <b>SqlPatientRepository</b>
          <div class="card-code code-font" style="color:var(--accent)">services.AddSingleton&lt;T, U&gt;()</div>
        </div>
      </div>

      <div class="card-item scpd">
        <div class="card-top">
          <span style="color:var(--accent-blue)">AppointmentService</span>
          <span class="lt-tag lt-scpd">Scoped</span>
        </div>
        <div class="card-body">
          Реалізація: <b>AppointmentService</b>
          <div class="card-code code-font" style="color:var(--accent-blue)">services.AddScoped&lt;T&gt;()</div>
        </div>
      </div>

      <div class="card-item tran">
        <div class="card-top">
          <span style="color:var(--accent-yellow)">INotificationService</span>
          <span class="lt-tag lt-tran">Transient</span>
        </div>
        <div class="card-body">
          Реалізація: <b>Фабрика (Lambda Func)</b>
          <div class="card-code code-font" style="color:var(--accent-yellow)">services.AddTransient(sp =&gt; ...)</div>
        </div>
      </div>
    </div>

    <div class="bridge-col">
      <div class="build-circle">➔</div>
      <div class="build-title code-font">.Build()</div>
      <div class="build-desc">Контейнер стає <b>Immutable</b> (незмінним)</div>
    </div>

    <div class="phase-panel p2">
      <div class="panel-header">
        <span class="panel-title" style="color:var(--accent-blue)">Фаза 2: Розпізнавання</span>
        <span class="panel-badge" style="background:rgba(106,162,216,0.25); color:var(--accent-blue)">IServiceProvider</span>
      </div>

      <div class="card-item sing">
        <div class="card-top">
          <span style="color:var(--accent)">IPatientRepository</span>
          <span class="lt-tag lt-sing">1 екземпляр</span>
        </div>
        <div class="card-body">
          Створюється лише раз при першому виклику. Всі наступні запити повертають <b>той самий об'єкт</b>.
          <div class="card-code code-font" style="color:var(--accent)">provider.GetRequiredService&lt;T&gt;()</div>
        </div>
      </div>

      <div class="card-item scpd">
        <div class="card-top">
          <span style="color:var(--accent-blue)">AppointmentService</span>
          <span class="lt-tag lt-scpd">1 на Scope</span>
        </div>
        <div class="card-body">
          Один екземпляр у межах Scope. Знищується (Dispose) автоматично після завершення HTTP-запиту.
          <div class="card-code code-font" style="color:var(--accent-blue)">scope.ServiceProvider.GetService&lt;T&gt;()</div>
        </div>
      </div>

      <div class="card-item tran">
        <div class="card-top">
          <span style="color:var(--accent-yellow)">INotificationService</span>
          <span class="lt-tag lt-tran">Новий щоразу</span>
        </div>
        <div class="card-body">
          Новий об'єкт створюється щоразу при зверненні. Ідеально для легких сервісів без збереження стану.
          <div class="card-code code-font" style="color:var(--accent-yellow)">provider.GetRequiredService&lt;T&gt;()</div>
        </div>
      </div>
    </div>
  </div>

  <div class="anatomy-section">
    <div class="anatomy-header">
      <div class="anatomy-title">
        <span>📋</span>
        <span>Анатомія структури ServiceDescriptor</span>
      </div>
      <span style="font-size:14px; color:#9cb0a8">Внутрішній дескриптор сервісу в колекції</span>
    </div>
    <table class="anatomy-table">
      <tr>
        <td class="field code-font">ServiceType</td>
        <td class="val code-font" style="color:var(--accent)">typeof(IPatientRepository)</td>
        <td class="comment">Тип інтерфейсу або базового класу контракту</td>
      </tr>
      <tr>
        <td class="field code-font">ImplementationType</td>
        <td class="val code-font" style="color:var(--accent-blue)">typeof(SqlPatientRepository)</td>
        <td class="comment">Конкретний клас реалізації для створення екземпляра</td>
      </tr>
      <tr>
        <td class="field code-font">ImplementationFactory</td>
        <td class="val code-font" style="color:#c5d3cd">Func&lt;IServiceProvider, object&gt;</td>
        <td class="comment">Делегат фабрики (опціонально, замість прямого типу)</td>
      </tr>
      <tr>
        <td class="field code-font">Lifetime</td>
        <td class="val code-font" style="color:var(--accent-yellow)">ServiceLifetime.Singleton</td>
        <td class="comment">Стратегія володіння та життєвого циклу екземпляра</td>
      </tr>
    </table>
  </div>

  <div class="footer-row">
    <div class="rule-item">
      <span style="color:var(--accent); font-size:18px">✔</span>
      <span><b>GetService&lt;T&gt;()</b> — повертає <code class="code-font">null</code>, якщо сервіс не зареєстровано</span>
    </div>
    <div class="rule-item">
      <span style="color:var(--accent-yellow); font-size:18px">⚡</span>
      <span><b>GetRequiredService&lt;T&gt;()</b> — кидає виняток, гарантуючи надійний <b>Fail-Fast</b></span>
    </div>
  </div>
</body>
</html>
"""

# ==============================================================================
# 3. SERVICE LIFETIMES & CAPTIVE DEPENDENCY
# ==============================================================================
def get_html_3(theme_css):
    base_css = get_base_css(theme_css)
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<style>
{base_css}
  body {{
    background: var(--bg-page);
    background-image: var(--bg-grad);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
    color: var(--text-main);
    width: 1200px;
    height: 980px;
    padding: 20px 28px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    overflow: hidden;
    position: relative;
  }}
  .code-font {{
    font-family: "Cascadia Code", "JetBrains Mono", Consolas, monospace;
  }}
  .header {{
    text-align: center;
  }}
  .title {{
    font-size: 27px;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -0.5px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
  }}
  .title-tag {{
    font-size: 13.5px;
    font-weight: 700;
    color: #0a0e0c;
    background: var(--accent);
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
  }}
  .subtitle {{
    font-size: 15px;
    color: var(--text-muted);
    margin-top: 2px;
  }}

  /* 1. TIMELINE WRAPPER */
  .timeline-wrapper {{
    background: #131d18;
    border: 2px solid #273b32;
    border-radius: 14px;
    padding: 12px 18px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  
  .timeline-axis-row {{
    display: grid;
    grid-template-columns: 210px repeat(4, 1fr);
    gap: 12px;
    align-items: center;
    padding-bottom: 6px;
    border-bottom: 1.5px dashed #283d34;
  }}
  .axis-label {{
    font-size: 14px;
    font-weight: 800;
    color: #7d938a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .scope-badge {{
    background: #182620;
    border: 1.5px solid #31463c;
    border-radius: 8px;
    padding: 4px 10px;
    text-align: center;
    font-size: 13.5px;
    font-weight: 700;
    color: #b5c7c0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .scope-badge span.id {{
    color: var(--accent);
    font-size: 12px;
  }}

  .lifetime-row {{
    display: grid;
    grid-template-columns: 210px 1fr;
    gap: 12px;
    align-items: center;
  }}
  .lt-info {{
    display: flex;
    flex-direction: column;
    gap: 1px;
  }}
  .lt-name {{
    font-size: 18px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .lt-desc {{
    font-size: 12.5px;
    color: #9cb0a8;
  }}

  .bar-container {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    width: 100%;
  }}

  .singleton-full-bar {{
    background: linear-gradient(90deg, rgba(118, 199, 173, 0.25) 0%, rgba(118, 199, 173, 0.12) 100%);
    border: 2px solid var(--accent);
    border-radius: 10px;
    padding: 9px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 0 20px rgba(118, 199, 173, 0.15);
  }}
  .singleton-full-bar .instance-title {{
    font-size: 15.5px;
    font-weight: 800;
    color: var(--accent);
  }}
  .singleton-full-bar .instance-note {{
    font-size: 13px;
    color: #c0d3cb;
  }}

  .scoped-bar {{
    background: linear-gradient(180deg, rgba(220, 182, 101, 0.22) 0%, rgba(220, 182, 101, 0.1) 100%);
    border: 2px solid var(--accent-yellow);
    border-radius: 10px;
    padding: 8px 6px;
    text-align: center;
  }}
  .scoped-bar .inst-code {{
    font-size: 14px;
    font-weight: 800;
    color: var(--accent-yellow);
  }}
  .scoped-bar .inst-sub {{
    font-size: 11.5px;
    color: #d1c8b0;
    margin-top: 1px;
  }}

  .transient-cell {{
    display: flex;
    gap: 6px;
  }}
  .transient-pill {{
    flex: 1;
    background: linear-gradient(180deg, rgba(106, 162, 216, 0.22) 0%, rgba(106, 162, 216, 0.1) 100%);
    border: 1.5px solid var(--accent-blue);
    border-radius: 8px;
    padding: 6px 3px;
    text-align: center;
  }}
  .transient-pill .pill-code {{
    font-size: 13px;
    font-weight: 800;
    color: var(--accent-blue);
  }}
  .transient-pill .pill-sub {{
    font-size: 11px;
    color: #a3bad0;
  }}

  /* 2. MATRIX COMPARISON TABLE */
  .matrix-wrapper {{
    background: #121b16;
    border: 1.5px solid #24362d;
    border-radius: 12px;
    padding: 10px 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  }}
  .matrix-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
  }}
  .matrix-table th {{
    text-align: left;
    padding: 6px 10px;
    color: #8da198;
    font-size: 12.5px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1.5px solid #22342b;
  }}
  .matrix-table td {{
    padding: 7px 10px;
    border-bottom: 1px solid #1a2721;
    color: #d4e0db;
    vertical-align: middle;
  }}
  .matrix-table tr:last-child td {{
    border-bottom: none;
  }}
  .lt-badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 13px;
  }}
  .lt-badge.sing {{ background: rgba(118, 199, 173, 0.2); color: var(--accent); border: 1px solid rgba(118, 199, 173, 0.4); }}
  .lt-badge.scpd {{ background: rgba(220, 182, 101, 0.2); color: var(--accent-yellow); border: 1px solid rgba(220, 182, 101, 0.4); }}
  .lt-badge.tran {{ background: rgba(106, 162, 216, 0.2); color: var(--accent-blue); border: 1px solid rgba(106, 162, 216, 0.4); }}

  /* 3. CAPTIVE DEPENDENCY + SOLUTION DUAL GRID */
  .dual-grid {{
    display: grid;
    grid-template-columns: 570px 550px;
    gap: 14px;
  }}
  
  .captive-panel {{
    background: #1b1417;
    border: 2px solid rgba(226, 109, 109, 0.65);
    border-radius: 12px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    box-shadow: 0 0 25px rgba(226, 109, 109, 0.12);
  }}
  .panel-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(226, 109, 109, 0.3);
  }}
  .panel-title-danger {{
    font-size: 15.5px;
    font-weight: 800;
    color: var(--accent-red);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .rule-pill-danger {{
    background: rgba(226, 109, 109, 0.2);
    color: #f7a2a2;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid rgba(226, 109, 109, 0.4);
  }}

  .danger-cards {{
    display: flex;
    flex-direction: column;
    gap: 7px;
  }}
  .danger-card {{
    background: #24181c;
    border: 1px solid rgba(226, 109, 109, 0.35);
    border-radius: 8px;
    padding: 8px 12px;
  }}
  .danger-card-top {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13.5px;
    font-weight: 800;
    margin-bottom: 3px;
  }}
  .danger-card-desc {{
    font-size: 12.5px;
    color: #e0d0d3;
    line-height: 1.35;
  }}

  .solution-panel {{
    background: #121c17;
    border: 2px solid rgba(118, 199, 173, 0.65);
    border-radius: 12px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    box-shadow: 0 0 25px rgba(118, 199, 173, 0.12);
  }}
  .panel-title-success {{
    font-size: 15.5px;
    font-weight: 800;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .solution-code {{
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    line-height: 1.45;
    color: #e0ece6;
  }}
  .solution-meta {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    color: #a4b8af;
    background: #16241e;
    padding: 5px 10px;
    border-radius: 6px;
    border: 1px solid #23372c;
  }}

  /* 4. FOOTER */
  .golden-footer {{
    background: #111714;
    border: 1.5px solid #283a32;
    border-radius: 10px;
    padding: 8px 16px;
    text-align: center;
    font-size: 14px;
    color: var(--accent);
    font-weight: 600;
  }}
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <span>Часи Життя Сервісів та Captive Dependency</span>
      <span class="title-tag">Service Lifetimes</span>
    </div>
    <div class="subtitle">Порівняння Singleton, Scoped, Transient, матриця вибору та захист від пасток інжекції</div>
  </div>

  <div class="timeline-wrapper">
    <div class="timeline-axis-row">
      <div class="axis-label">Час роботи ➔</div>
      <div class="scope-badge">
        <span>Запит 1</span>
        <span class="id code-font">Scope #1</span>
      </div>
      <div class="scope-badge">
        <span>Запит 2</span>
        <span class="id code-font">Scope #2</span>
      </div>
      <div class="scope-badge">
        <span>Запит 3</span>
        <span class="id code-font">Scope #3</span>
      </div>
      <div class="scope-badge">
        <span>Запит 4</span>
        <span class="id code-font">Scope #4</span>
      </div>
    </div>

    <div class="lifetime-row">
      <div class="lt-info">
        <div class="lt-name" style="color:var(--accent)">
          <span>●</span> Singleton
        </div>
        <div class="lt-desc">1 екземпляр на весь застосунок</div>
      </div>
      <div class="singleton-full-bar">
        <span class="instance-title code-font">AppConfiguration [Instance #1]</span>
        <span class="instance-note">Створюється при старті або 1-му виклику • живе до повної зупинки процесу</span>
      </div>
    </div>

    <div class="lifetime-row">
      <div class="lt-info">
        <div class="lt-name" style="color:var(--accent-yellow)">
          <span>●</span> Scoped
        </div>
        <div class="lt-desc">1 екземпляр на Scope / запит</div>
      </div>
      <div class="bar-container">
        <div class="scoped-bar">
          <div class="inst-code code-font">ClinicDbContext [#1]</div>
          <div class="inst-sub">Живе в межах Запиту 1</div>
        </div>
        <div class="scoped-bar">
          <div class="inst-code code-font">ClinicDbContext [#2]</div>
          <div class="inst-sub">Живе в межах Запиту 2</div>
        </div>
        <div class="scoped-bar">
          <div class="inst-code code-font">ClinicDbContext [#3]</div>
          <div class="inst-sub">Живе в межах Запиту 3</div>
        </div>
        <div class="scoped-bar">
          <div class="inst-code code-font">ClinicDbContext [#4]</div>
          <div class="inst-sub">Живе в межах Запиту 4</div>
        </div>
      </div>
    </div>

    <div class="lifetime-row">
      <div class="lt-info">
        <div class="lt-name" style="color:var(--accent-blue)">
          <span>●</span> Transient
        </div>
        <div class="lt-desc">Новий об'єкт щоразу</div>
      </div>
      <div class="bar-container">
        <div class="transient-cell">
          <div class="transient-pill">
            <div class="pill-code code-font">#1</div>
            <div class="pill-sub">виклик A</div>
          </div>
          <div class="transient-pill">
            <div class="pill-code code-font">#2</div>
            <div class="pill-sub">виклик B</div>
          </div>
        </div>
        <div class="transient-cell">
          <div class="transient-pill">
            <div class="pill-code code-font">#3</div>
            <div class="pill-sub">виклик A</div>
          </div>
          <div class="transient-pill">
            <div class="pill-code code-font">#4</div>
            <div class="pill-sub">виклик B</div>
          </div>
        </div>
        <div class="transient-cell">
          <div class="transient-pill">
            <div class="pill-code code-font">#5</div>
            <div class="pill-sub">виклик A</div>
          </div>
          <div class="transient-pill">
            <div class="pill-code code-font">#6</div>
            <div class="pill-sub">виклик B</div>
          </div>
        </div>
        <div class="transient-cell">
          <div class="transient-pill">
            <div class="pill-code code-font">#7</div>
            <div class="pill-sub">виклик A</div>
          </div>
          <div class="transient-pill">
            <div class="pill-code code-font">#8</div>
            <div class="pill-sub">виклик B</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="matrix-wrapper">
    <table class="matrix-table">
      <thead>
        <tr>
          <th>Lifetime</th>
          <th>Кількість об'єктів</th>
          <th>Створення</th>
          <th>Звільнення (Dispose)</th>
          <th>Потокобезпека</th>
          <th>Типові сервіси</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="lt-badge sing">Singleton</span></td>
          <td><b>1 на весь процес</b></td>
          <td>1-й запит або старт хоста</td>
          <td>Зупинка додатку</td>
          <td><span style="color:var(--accent-yellow)">Обов'язкова (Thread-safe)</span></td>
          <td class="code-font" style="color:var(--accent); font-size:12px">IConfiguration, Cache, HttpClient</td>
        </tr>
        <tr>
          <td><span class="lt-badge scpd">Scoped</span></td>
          <td><b>1 на Scope / запит</b></td>
          <td>1-й запит у межах Scope</td>
          <td>Кінець Scope (<code class="code-font">scope.Dispose</code>)</td>
          <td>Ізольовано в межах запиту</td>
          <td class="code-font" style="color:var(--accent-yellow); font-size:12px">DbContext, UnitOfWork, Repositories</td>
        </tr>
        <tr>
          <td><span class="lt-badge tran">Transient</span></td>
          <td><b>Новий щоразу</b></td>
          <td>Кожен виклик <code class="code-font">GetService()</code></td>
          <td>Кінець Scope або GC</td>
          <td>Не потрібна (ізольований)</td>
          <td class="code-font" style="color:var(--accent-blue); font-size:12px">Validators, Mappers, ILogger&lt;T&gt;</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="dual-grid">
    <div class="captive-panel">
      <div class="panel-header">
        <div class="panel-title-danger">
          <span style="font-size:18px">⚠</span>
          <span>Пастки Captive Dependency</span>
        </div>
        <div class="rule-pill-danger code-font">Lifetime(Dep) ≥ Lifetime(Consumer)</div>
      </div>
      <div class="danger-cards">
        <div class="danger-card">
          <div class="danger-card-top">
            <span style="color:var(--accent)">Singleton</span>
            <span style="color:var(--accent-red)">➔ конструктор ➔</span>
            <span style="color:var(--accent-yellow)">Scoped</span>
            <span style="background:rgba(226,109,109,0.3); color:#fca5a5; padding:1px 6px; border-radius:4px; font-size:11px">КРИТИЧНО [X]</span>
          </div>
          <div class="danger-card-desc">
            <b>«Полонений сервіс»:</b> Scoped-екземпляр назавжди застрягає в Singleton. DbContext ніколи не звільняється, викликаючи витоки пам'яті, змішування даних пацієнтів та race condition.
          </div>
        </div>
        <div class="danger-card">
          <div class="danger-card-top">
            <span style="color:var(--accent)">Singleton</span>
            <span style="color:var(--accent-yellow)">➔ конструктор ➔</span>
            <span style="color:var(--accent-blue)">Transient</span>
            <span style="background:rgba(220,182,101,0.25); color:var(--accent-yellow); padding:1px 6px; border-radius:4px; font-size:11px">ПАСТКА [!]</span>
          </div>
          <div class="danger-card-desc">
            <b>«Прихований Singleton»:</b> Transient створюється один раз під час запуску Singleton і більше не оновлюється, втрачаючи очікувану свіжість стану.
          </div>
        </div>
      </div>
    </div>

    <div class="solution-panel">
      <div class="panel-header">
        <div class="panel-title-success">
          <span style="font-size:18px">✔</span>
          <span>Правильне рішення: IServiceScopeFactory</span>
        </div>
        <span class="code-font" style="font-size:12px; color:var(--accent)">Worker / BackgroundService</span>
      </div>
      <pre class="solution-code code-font"><span style="color:var(--accent)">class</span> BackgroundQueueWorker : <span style="color:var(--accent-blue)">BackgroundService</span> {{
  <span style="color:var(--accent)">private readonly</span> <span style="color:var(--accent-yellow)">IServiceScopeFactory</span> _scopeFactory;
  <span style="color:var(--accent)">protected override async</span> Task <span style="color:var(--accent-blue)">ExecuteAsync</span>(CancellationToken ct) {{
    <span style="color:#7d988d">// Створюємо свіжий scope на кожну ітерацію / повідомлення</span>
    <span style="color:var(--accent)">using var</span> scope = _scopeFactory.<span style="color:var(--accent-yellow)">CreateScope</span>();
    <span style="color:var(--accent)">var</span> db = scope.ServiceProvider.<span style="color:var(--accent)">GetRequiredService</span>&lt;<span style="color:var(--accent-blue)">ClinicDbContext</span>&gt;();
    <span style="color:var(--accent)">await</span> db.ProcessBatchAsync(ct);
  }}
}}</pre>
      <div class="solution-meta code-font">
        <span>🛡 Fail-Fast захист:</span>
        <span style="color:var(--accent-yellow)">builder.Host.UseDefaultServiceProvider(o =&gt; o.ValidateScopes = true)</span>
      </div>
    </div>
  </div>

  <div class="golden-footer">
    Золоте правило DI: довгоживучі сервіси (Singleton) ніколи не повинні захоплювати короткоживучі сервіси (Scoped / Transient) через свій конструктор.
  </div>
</body>
</html>
"""


# ==============================================================================
# 4. OPTIONS PATTERN
# ==============================================================================
def get_html_4(theme_css):
    base_css = get_base_css(theme_css)
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<style>
{base_css}
  body {{
    width: 1240px;
    height: 980px;
    padding: 24px 30px;
  }}
  .top-pipeline {{
    display: grid;
    grid-template-columns: 430px 30px 320px 30px 370px;
    gap: 0;
    align-items: center;
    background: #141d19;
    border: 2px solid #263830;
    border-radius: 14px;
    padding: 12px 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
  }}
  .sources-group {{
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}
  .sources-label {{
    font-size: 13px;
    font-weight: 800;
    color: #8da299;
    text-transform: uppercase;
    letter-spacing: 0.6px;
  }}
  .sources-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .chip {{
    background: #182620;
    border: 1px solid #2d4237;
    border-radius: 8px;
    padding: 4px 9px;
    font-size: 12.5px;
    font-weight: 600;
  }}
  .chip.c1 {{ border-left: 3px solid var(--accent); }}
  .chip.c2 {{ border-left: 3px solid var(--accent-blue); }}
  .chip.c3 {{ border-left: 3px solid var(--accent-yellow); }}
  .chip.c4 {{ border-left: 3px solid var(--accent-purple); }}
  .chip.c5 {{ border-left: 3px solid var(--accent-red); }}

  .flow-arrow {{
    text-align: center;
    color: var(--accent);
    font-size: 20px;
    font-weight: 800;
  }}

  .pipe-box {{
    background: #182620;
    border: 1.5px solid #2f453a;
    border-radius: 10px;
    padding: 9px 12px;
  }}
  .pipe-title {{
    font-size: 14.5px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .pipe-code {{
    background: #0d1411;
    border: 1px solid #24352d;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
    font-weight: 600;
  }}

  .variants-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
  }}
  .var-card {{
    background: #141e19;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .var-card.v-mint {{
    border: 2px solid rgba(118, 199, 173, 0.7);
    background: linear-gradient(135deg, rgba(118, 199, 173, 0.12) 0%, #141e19 100%);
  }}
  .var-card.v-amber {{
    border: 2px solid rgba(220, 182, 101, 0.7);
    background: linear-gradient(135deg, rgba(220, 182, 101, 0.12) 0%, #141e19 100%);
  }}
  .var-card.v-purple {{
    border: 2px solid rgba(196, 122, 184, 0.7);
    background: linear-gradient(135deg, rgba(196, 122, 184, 0.12) 0%, #141e19 100%);
  }}

  .var-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    border-bottom: 1px solid #273931;
    margin-bottom: 12px;
  }}
  .var-name {{
    font-size: 19px;
    font-weight: 800;
  }}
  .var-badge {{
    font-size: 12.5px;
    font-weight: 800;
    padding: 3px 9px;
    border-radius: 6px;
    text-transform: uppercase;
  }}

  .var-points {{
    display: flex;
    flex-direction: column;
    gap: 9px;
    font-size: 14.5px;
    color: #dbe7e2;
    line-height: 1.35;
  }}
  .var-point {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
  }}
  .var-point span.icon {{
    font-weight: 800;
  }}
  .var-footer-tag {{
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px dashed #283a31;
    font-size: 13px;
    color: #9cb0a8;
  }}

  .bottom-grid {{
    display: grid;
    grid-template-columns: 680px 1fr;
    gap: 16px;
    align-items: stretch;
  }}
  .code-card {{
    background: #141e19;
    border: 2px solid #283c32;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
  }}
  .code-card-title {{
    font-size: 15px;
    font-weight: 800;
    color: var(--accent-blue);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  pre.code-box {{
    background: #0a100d;
    border: 1px solid #22352c;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13.5px;
    line-height: 1.45;
    color: #d2ded9;
    white-space: pre;
    margin: 0;
  }}
  .kw {{ color: var(--accent-red); font-weight: 700; }}
  .type {{ color: var(--accent-blue); font-weight: 700; }}
  .var {{ color: var(--accent); }}
  .cm {{ color: #6e867b; font-style: italic; }}

  .rule-card {{
    background: #141e19;
    border: 2px solid #283c32;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .rule-title {{
    font-size: 15px;
    font-weight: 800;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }}
  .rule-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 14px;
    color: #d1dfda;
    line-height: 1.35;
  }}
  .rule-list li b {{
    color: #ffffff;
  }}
  .rule-footer-tag {{
    font-size: 12.5px;
    color: #8da098;
    margin-top: 6px;
  }}
</style>
</head>
<body>
  <div class="header">
    <div class="title">
      <span>Options Pattern у .NET — IOptions, IOptionsSnapshot, IOptionsMonitor</span>
      <span class="title-tag">Configuration</span>
    </div>
    <div class="subtitle">Типізована конфігурація, інкапсуляція налаштувань та підтримка Hot Reload</div>
  </div>

  <div class="top-pipeline">
    <div class="sources-group">
      <div class="sources-label">Джерела конфігурації (Configuration Sources)</div>
      <div class="sources-chips">
        <div class="chip c1 code-font">appsettings.json</div>
        <div class="chip c2 code-font">appsettings.Prod</div>
        <div class="chip c3 code-font">Env Variables</div>
        <div class="chip c4 code-font">CLI Args</div>
        <div class="chip c5 code-font">User Secrets</div>
      </div>
    </div>

    <div class="flow-arrow">➔</div>

    <div class="pipe-box">
      <div class="pipe-title">
        <span class="code-font" style="color:var(--accent)">IConfiguration</span>
        <span style="font-size:11px; color:#8da098">Дерево ключів</span>
      </div>
      <div class="pipe-code code-font" style="color:var(--accent)">
        builder.Configuration.GetSection("Clinic")
      </div>
    </div>

    <div class="flow-arrow">➔</div>

    <div class="pipe-box">
      <div class="pipe-title">
        <span class="code-font" style="color:var(--accent-yellow)">services.Configure&lt;T&gt;()</span>
        <span style="font-size:11px; color:#8da098">Зв'язування з POCO</span>
      </div>
      <div class="pipe-code code-font" style="color:var(--accent-yellow)">
        services.Configure&lt;ClinicOptions&gt;(sec);
      </div>
    </div>
  </div>

  <div class="variants-grid">
    <div class="var-card v-mint">
      <div>
        <div class="var-head">
          <span class="var-name code-font" style="color:var(--accent)">IOptions&lt;T&gt;</span>
          <span class="var-badge" style="background:rgba(118,199,173,0.25); color:var(--accent)">Singleton</span>
        </div>
        <div class="var-points">
          <div class="var-point">
            <span class="icon" style="color:var(--accent)">✔</span>
            <span>Зчитується <b>один раз</b> при запуску застосунку</span>
          </div>
          <div class="var-point">
            <span class="icon" style="color:var(--accent)">✔</span>
            <span><b>Максимальна швидкодія</b>, мінімальний оверхед</span>
          </div>
          <div class="var-point">
            <span class="icon" style="color:var(--accent-red)">✖</span>
            <span><b>Не підтримує Hot Reload</b> (конфігурація статична)</span>
          </div>
        </div>
      </div>
      <div class="var-footer-tag">
        <b>Використання:</b> Незмінні системні налаштування
      </div>
    </div>

    <div class="var-card v-amber">
      <div>
        <div class="var-head">
          <span class="var-name code-font" style="color:var(--accent-yellow)">IOptionsSnapshot&lt;T&gt;</span>
          <span class="var-badge" style="background:rgba(220,182,101,0.25); color:var(--accent-yellow)">Scoped</span>
        </div>
        <div class="var-points">
          <div class="var-point">
            <span class="icon" style="color:var(--accent)">✔</span>
            <span>Перераховується для кожного <b>нового HTTP-запиту</b></span>
          </div>
          <div class="var-point">
            <span class="icon" style="color:var(--accent)">✔</span>
            <span>Підтримує <b>Hot Reload</b> на кожен новий запит</span>
          </div>
          <div class="var-point">
            <span class="icon" style="color:var(--accent-red)">✖</span>
            <span><b>Заборонено в Singleton!</b> (Captive Dependency)</span>
          </div>
        </div>
      </div>
      <div class="var-footer-tag">
        <b>Використання:</b> Веб-контролери та Scoped-сервіси
      </div>
    </div>

    <div class="var-card v-purple">
      <div>
        <div class="var-head">
          <span class="var-name code-font" style="color:var(--accent-purple)">IOptionsMonitor&lt;T&gt;</span>
          <span class="var-badge" style="background:rgba(196,122,184,0.25); color:var(--accent-purple)">Singleton</span>
        </div>
        <div class="var-points">
          <div class="var-point">
            <span class="icon" style="color:var(--accent)">✔</span>
            <span>Реактивне оновлення: <code class="code-font" style="color:var(--accent-purple)">.OnChange(cb)</code></span>
          </div>
          <div class="var-point">
            <span class="icon" style="color:var(--accent)">✔</span>
            <span>Безпечно для <b>Singleton</b> та <b>BackgroundService</b></span>
          </div>
          <div class="var-point">
            <span class="icon" style="color:var(--accent)">✔</span>
            <span>Властивість <code class="code-font" style="color:var(--accent-purple)">.CurrentValue</code> завжди актуальна</span>
          </div>
        </div>
      </div>
      <div class="var-footer-tag">
        <b>Використання:</b> Фонові сервіси та воркери
      </div>
    </div>
  </div>

  <div class="bottom-grid">
    <div class="code-card">
      <div class="code-card-title">
        <span>💉 Впровадження через конструктор (Constructor DI)</span>
      </div>
      <pre class="code-box code-font"><span class="kw">public class</span> <span class="type">AppointmentService</span>
{{
    <span class="kw">private readonly</span> <span class="type">ClinicOptions</span> <span class="var">_opts</span>;

    <span class="kw">public</span> <span class="type">AppointmentService</span>(<span class="type">IOptions</span>&lt;<span class="type">ClinicOptions</span>&gt; opts)
    {{
        <span class="var">_opts</span> = opts.Value; <span class="cm">// Типізовано, без magic strings!</span>
    }}
}}</pre>
    </div>

    <div class="rule-card">
      <div>
        <div class="rule-title">
          <span>💡 Швидка шпаргалка вибору</span>
        </div>
        <ul class="rule-list">
          <li><b>Web API / Контролери</b> ➔ <code class="code-font" style="color:var(--accent-yellow)">IOptionsSnapshot&lt;T&gt;</code></li>
          <li><b>BackgroundService / Воркери</b> ➔ <code class="code-font" style="color:var(--accent-purple)">IOptionsMonitor&lt;T&gt;</code></li>
          <li><b>Статичні Singleton</b> ➔ <code class="code-font" style="color:var(--accent)">IOptions&lt;T&gt;</code></li>
        </ul>
      </div>
      <div class="rule-footer-tag">
        Пакет: <code class="code-font" style="color:var(--accent)">Microsoft.Extensions.Options</code>
      </div>
    </div>
  </div>
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser(description="Генератор схем для Розділу 21")
    parser.add_argument("--bw", "--monochrome", action="store_true", help="Генерувати монохромні (ч/б) варіанти для друку")
    args = parser.parse_args()

    theme_css = get_theme_css(is_bw=args.bw)
    prefix = "bw-" if args.bw else "candidate-"

    print(f"Генерація діаграм (Режим: {'Чорно-білий для друку' if args.bw else 'Кольоровий для сайту'})...")
    render_page(get_html_1(theme_css), f"{prefix}01.png", 1200, 1100)
    render_page(get_html_2(theme_css), f"{prefix}02.png", 1200, 1040)
    render_page(get_html_3(theme_css), f"{prefix}03.png", 1200, 980)
    render_page(get_html_4(theme_css), f"{prefix}04.png", 1240, 980)
    print("Усі 4 діаграми успішно згенеровано!")

if __name__ == "__main__":
    main()
