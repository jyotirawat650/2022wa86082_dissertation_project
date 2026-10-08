<?php
require_once __DIR__ . '/Calculator.php';
$calc = new Calculator();
$version = "1.0.0";
?>
<!doctype html>
<html>
<head><meta charset="utf-8"><title>PHP CI/CD Demo</title>
<style>body{font-family:Arial,sans-serif;max-width:600px;margin:60px auto;padding:0 20px}
.box{background:#f4f6f8;border-radius:8px;padding:16px;margin:12px 0}</style></head>
<body>
  <h1>PHP CI/CD Demo</h1>
  <p>Deployed automatically by Jenkins. Version <b><?= $version ?></b></p>
  <div class="box">
    <p>2 + 3 = <b><?= $calc->add(2, 3) ?></b></p>
    <p>10 - 4 = <b><?= $calc->subtract(10, 4) ?></b></p>
    <p>6 &times; 7 = <b><?= $calc->multiply(6, 7) ?></b></p>
  </div>
</body>
</html>
