# 符號微分（Symbolic Differentiation）
# 用「遞迴」對數學運算式求導函數，並化簡結果。
# 運算式用 tuple 表示，例如 x^2 + 3x + 2：
#   add(pow(var('x'), const(2)), add(mul(const(3), var('x')), const(2)))
# 支援：常數、變數、+ - * /、次方（指數為常數）、sin cos exp ln。

import math


# ---------- 運算式建構子 ----------
def const(c):
    return ('const', c)


def var(name):
    return ('var', name)


def add(a, b):
    return ('add', a, b)


def sub(a, b):
    return ('sub', a, b)


def mul(a, b):
    return ('mul', a, b)


def div(a, b):
    return ('div', a, b)


def pw(a, b):
    return ('pow', a, b)


def sin(a):
    return ('sin', a)


def cos(a):
    return ('cos', a)


def exp(a):
    return ('exp', a)


def ln(a):
    return ('ln', a)


def neg(e):
    return ('mul', const(-1), e)


# ---------- 印成可讀的字串 ----------
def to_str(e, parent=0):
    tag = e[0]
    if tag == 'const':
        return str(e[1])
    if tag == 'var':
        return e[1]
    if tag == 'add':
        s, p = f"{to_str(e[1], 1)} + {to_str(e[2], 1)}", 1
    elif tag == 'sub':
        s, p = f"{to_str(e[1], 1)} - {to_str(e[2], 2)}", 1
    elif tag == 'mul':
        if e[1] == ('const', -1):
            s, p = f"-{to_str(e[2], 2)}", 2
        else:
            s, p = f"{to_str(e[1], 2)} * {to_str(e[2], 2)}", 2
    elif tag == 'div':
        s, p = f"{to_str(e[1], 2)} / {to_str(e[2], 3)}", 2
    elif tag == 'pow':
        s, p = f"{to_str(e[1], 4)} ^ {to_str(e[2], 4)}", 3
    elif tag in ('sin', 'cos', 'exp', 'ln'):
        s, p = f"{tag}({to_str(e[1])})", 4
    else:
        raise ValueError(f"未知的運算子: {tag}")
    return f"({s})" if p < parent else s


# ---------- 化簡 ----------
def is_const(e, val=None):
    return e[0] == 'const' and (val is None or e[1] == val)


def simplify(e):
    tag = e[0]
    if tag in ('const', 'var'):
        return e
    if tag in ('sin', 'cos', 'exp', 'ln'):
        return (tag, simplify(e[1]))
    if tag == 'pow':
        a, b = simplify(e[1]), simplify(e[2])
        if is_const(b, 0):
            return const(1)
        if is_const(b, 1):
            return a
        if a[0] == 'const' and b[0] == 'const':
            return const(a[1] ** b[1])
        return pw(a, b)

    a, b = simplify(e[1]), simplify(e[2])
    if tag == 'add':
        if is_const(a, 0):
            return b
        if is_const(b, 0):
            return a
        if a[0] == 'const' and b[0] == 'const':
            return const(a[1] + b[1])
        if a == b:
            return mul(const(2), a)
        return add(a, b)
    if tag == 'sub':
        if is_const(b, 0):
            return a
        if a[0] == 'const' and b[0] == 'const':
            return const(a[1] - b[1])
        if a == b:
            return const(0)
        if is_const(a, 0):
            return neg(b)
        return sub(a, b)
    if tag == 'mul':
        if is_const(a, 0) or is_const(b, 0):
            return const(0)
        if is_const(a, 1):
            return b
        if is_const(b, 1):
            return a
        if a[0] == 'const' and b[0] == 'const':
            return const(a[1] * b[1])
        if is_const(a, -1):
            return neg(b)
        if is_const(b, -1):
            return neg(a)
        if b[0] == 'const' and a[0] != 'const':   # 常數擺前面
            a, b = b, a
        return mul(a, b)
    if tag == 'div':
        if is_const(a, 0):
            return const(0)
        if is_const(b, 1):
            return a
        if a == b:
            return const(1)
        if a[0] == 'const' and b[0] == 'const' and b[1] != 0 and a[1] % b[1] == 0:
            return const(a[1] // b[1])
        return div(a, b)
    raise ValueError(f"未知的運算子: {tag}")


# ---------- 核心：遞迴求導 ----------
def sym_diff(e, v='x'):
    tag = e[0]
    if tag == 'const':
        return const(0)
    if tag == 'var':
        return const(1) if e[1] == v else const(0)
    if tag == 'add':
        return add(sym_diff(e[1], v), sym_diff(e[2], v))
    if tag == 'sub':
        return sub(sym_diff(e[1], v), sym_diff(e[2], v))
    if tag == 'mul':                                   # (uv)' = u'v + uv'
        return add(mul(sym_diff(e[1], v), e[2]), mul(e[1], sym_diff(e[2], v)))
    if tag == 'div':                                   # (u/v)' = (u'v - uv')/v^2
        return div(sub(mul(sym_diff(e[1], v), e[2]),
                       mul(e[1], sym_diff(e[2], v))),
                   pw(e[2], const(2)))
    if tag == 'pow':                                   # d(u^c) = c*u^(c-1)*u'
        u, c = e[1], e[2]
        if c[0] != 'const':
            raise ValueError("pow 的指數目前只支援常數")
        return mul(mul(const(c[1]), pw(u, const(c[1] - 1))), sym_diff(u, v))
    if tag == 'sin':                                   # (sin u)' = cos u * u'
        return mul(cos(e[1]), sym_diff(e[1], v))
    if tag == 'cos':                                   # (cos u)' = -sin u * u'
        return mul(neg(sin(e[1])), sym_diff(e[1], v))
    if tag == 'exp':                                   # (e^u)' = e^u * u'
        return mul(exp(e[1]), sym_diff(e[1], v))
    if tag == 'ln':                                    # (ln u)' = u'/u
        return div(sym_diff(e[1], v), e[1])
    raise ValueError(f"未知的運算子: {tag}")


# ---------- 數值代入（用來驗證微分正確）----------
def eval_expr(e, x):
    tag = e[0]
    if tag == 'const':
        return e[1]
    if tag == 'var':
        return x
    if tag == 'add':
        return eval_expr(e[1], x) + eval_expr(e[2], x)
    if tag == 'sub':
        return eval_expr(e[1], x) - eval_expr(e[2], x)
    if tag == 'mul':
        return eval_expr(e[1], x) * eval_expr(e[2], x)
    if tag == 'div':
        return eval_expr(e[1], x) / eval_expr(e[2], x)
    if tag == 'pow':
        return eval_expr(e[1], x) ** eval_expr(e[2], x)
    if tag == 'sin':
        return math.sin(eval_expr(e[1], x))
    if tag == 'cos':
        return math.cos(eval_expr(e[1], x))
    if tag == 'exp':
        return math.exp(eval_expr(e[1], x))
    if tag == 'ln':
        return math.log(eval_expr(e[1], x))
    raise ValueError(f"未知的運算子: {tag}")


if __name__ == "__main__":
    X = var('x')
    tests = [
        ("x^2 + 3*x + 2", add(pw(X, const(2)), add(mul(const(3), X), const(2)))),
        ("x^3", pw(X, const(3))),
        ("sin(x) * x", mul(sin(X), X)),
        ("exp(x) * x", mul(exp(X), X)),
        ("ln(x)", ln(X)),
        ("(x + 1) / (x - 1)", div(add(X, const(1)), sub(X, const(1)))),
    ]

    h = 1e-6
    for name, expr in tests:
        d = simplify(sym_diff(expr))
        print(f"f(x)  = {to_str(expr)}")
        print(f"f'(x) = {to_str(d)}")

        # 用中央差分 (f(x+h)-f(x-h))/2h 驗證符號微分是否正確
        ok = True
        for x in (0.5, 1.5, 2.0):
            numeric = (eval_expr(expr, x + h) - eval_expr(expr, x - h)) / (2 * h)
            symbolic = eval_expr(d, x)
            same = abs(numeric - symbolic) < 1e-4
            ok = ok and same
            print(f"    x={x:<4} 符號微分={symbolic: .6f}  數值微分={numeric: .6f}  相符={same}")
        print(f"    => 微分結果正確：{ok}\n")
