<?php
// Minimal dependency-free test runner. Exits with code 1 if any test fails.
$base = is_dir(__DIR__ . '/../src') ? __DIR__ . '/../src' : __DIR__ . '/../html';
require_once $base . '/Calculator.php';

$calc = new Calculator();
$passed = 0;
$failed = 0;

function check($name, $actual, $expected)
{
    global $passed, $failed;
    if ($actual == $expected) {
        echo "[PASS] $name\n";
        $passed++;
    } else {
        echo "[FAIL] $name (expected $expected, got $actual)\n";
        $failed++;
    }
}

check('add 2+3',        $calc->add(2, 3),        5);
check('subtract 10-4',  $calc->subtract(10, 4),  6);
check('multiply 6*7',   $calc->multiply(6, 7),   42);
check('divide 8/2',     $calc->divide(8, 2),     4);

try {
    $calc->divide(1, 0);
    check('divide by zero throws', 'no exception', 'exception');
} catch (InvalidArgumentException $e) {
    check('divide by zero throws', 'exception', 'exception');
}

echo "\nResult: $passed passed, $failed failed\n";
exit($failed > 0 ? 1 : 0);
