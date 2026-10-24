<?php
$pageTitle = "CalcSpace";
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#101322">
  <title><?= htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8') ?> — Smart Calculator</title>
  <link rel="stylesheet" href="style.css">
  <script src="app.js" defer></script>
</head>
<body>
  <div class="ambient ambient-one"></div>
  <div class="ambient ambient-two"></div>
  <main class="shell">
    <header class="topbar">
      <a class="brand" href="/" aria-label="CalcSpace home">
        <span class="brand-mark" aria-hidden="true">∑</span>
        <span><strong>CalcSpace</strong><small>SMART CALCULATOR</small></span>
      </a>
      <div class="status"><span class="status-dot"></span> Ready to calculate</div>
    </header>

    <section class="intro">
      <p class="eyebrow">A LITTLE MORE CLARITY</p>
      <h1>Numbers, <span>made simple.</span></h1>
      <p class="intro-copy">A clean space for quick calculations, everyday math, and everything in between.</p>
    </section>

    <section class="workspace" aria-label="Calculator workspace">
      <div class="calculator panel">
        <div class="calc-heading">
          <div>
            <p class="section-kicker">YOUR WORKSPACE</p>
            <h2>Calculator</h2>
          </div>
          <span class="mode-pill"><span class="live-dot"></span> Standard</span>
        </div>

        <div class="display" aria-live="polite" aria-atomic="true">
          <div class="display-meta"><span id="display-label">Ready when you are</span><span class="keyboard-hint">KEYBOARD ENABLED</span></div>
          <div id="expression" class="expression">&nbsp;</div>
          <div id="display-value" class="display-value">0</div>
          <div id="error-message" class="error-message" role="alert"></div>
        </div>

        <div class="keypad" role="group" aria-label="Calculator keys">
          <button class="key key-utility" data-action="clear" type="button">AC</button>
          <button class="key key-utility" data-action="sign" type="button">+/−</button>
          <button class="key key-utility" data-action="percent" type="button">%</button>
          <button class="key key-operator" data-operator="divide" type="button" aria-label="Divide">÷</button>

          <button class="key" data-digit="7" type="button">7</button>
          <button class="key" data-digit="8" type="button">8</button>
          <button class="key" data-digit="9" type="button">9</button>
          <button class="key key-operator" data-operator="multiply" type="button" aria-label="Multiply">×</button>

          <button class="key" data-digit="4" type="button">4</button>
          <button class="key" data-digit="5" type="button">5</button>
          <button class="key" data-digit="6" type="button">6</button>
          <button class="key key-operator" data-operator="subtract" type="button" aria-label="Subtract">−</button>

          <button class="key" data-digit="1" type="button">1</button>
          <button class="key" data-digit="2" type="button">2</button>
          <button class="key" data-digit="3" type="button">3</button>
          <button class="key key-operator" data-operator="add" type="button" aria-label="Add">+</button>

          <button class="key key-utility" data-action="backspace" type="button" aria-label="Delete last digit">⌫</button>
          <button class="key key-zero" data-digit="0" type="button">0</button>
          <button class="key" data-action="decimal" type="button">.</button>
          <button class="key key-equals" data-action="equals" type="button" aria-label="Equals">=</button>
        </div>
        <p class="calc-footnote"><span>↵</span> Enter to calculate <span class="footnote-divider">·</span> Esc to clear</p>
      </div>

      <aside class="side-column">
        <section class="panel history-panel">
          <div class="side-heading">
            <div><p class="section-kicker">YOUR RECENT WORK</p><h2>History</h2></div>
            <button id="clear-history" class="text-button" type="button">Clear</button>
          </div>
          <div id="history-list" class="history-list">
            <div id="history-empty" class="empty-state">
              <span class="empty-icon">↗</span>
              <strong>Your calculations will appear here</strong>
              <p>Run a calculation to start your history.</p>
            </div>
          </div>
        </section>

        <section class="tip-card">
          <div class="tip-icon">✦</div>
          <div><p class="section-kicker">QUICK TIP</p><p>Use your keyboard for faster calculations. Your recent results stay in this browser session.</p></div>
        </section>

        <section class="system-card">
          <div class="system-icon">⌘</div>
          <div><strong>Powered by PHP</strong><p>Calculations are processed by your PHP backend.</p></div>
          <span class="system-check" title="Backend integration">✓</span>
        </section>
      </aside>
    </section>

    <footer><span>© <?= date('Y') ?> CalcSpace</span><span>Built for clarity <span class="footer-star">✦</span></span></footer>
  </main>
</body>
</html>
<-rwxrwxrwx 1 harshit harshit 21 Oct 8 12:01 CI/CD test -->
