#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整 Lambda Calculus (λ-演算) 解譯器
支援：
1. 正規序 (Normal Order) 逐步歸約顯示 (δ-展開、α-轉換、β-歸約)
2. 「有名稱 (Named Macros)」與「沒名稱 (Pure Lambda)」雙模式輸入与自動轉譯
3. 內建完整 Church 編碼庫 (SKI、布林、自然數、算術、比较、Pair 結構、List、Y-Combinator 遞迴)
4. 結果自動逆向識別 (α-等價比對 + Church 數值解碼)
5. 互動式 REPL 命令列模式
"""

import re
from dataclasses import dataclass
from typing import Dict, Set, Optional, Tuple, List

# ==========================================
# 1. 抽象語法樹 (AST) 定義
# ==========================================
class Expr:
    def pretty(self) -> str:
        """簡潔格式輸出：合併連續 λ 並省去多餘括號，方便閱讀"""
        raise NotImplementedError

@dataclass(frozen=True)
class Var(Expr):
    name: str
    def __str__(self):
        return self.name
    def pretty(self) -> str:
        return self.name

@dataclass(frozen=True)
class Abs(Expr):
    param: str
    body: Expr
    def __str__(self):
        return f"(λ{self.param}.{self.body})"
    def pretty(self) -> str:
        params = [self.param]
        curr = self.body
        while isinstance(curr, Abs):
            params.append(curr.param)
            curr = curr.body
        return f"(λ{' '.join(params)}. {curr.pretty()})"

@dataclass(frozen=True)
class App(Expr):
    func: Expr
    arg: Expr
    def __str__(self):
        return f"({self.func} {self.arg})"
    def pretty(self) -> str:
        # 左結合展開：((A B) C) -> A B C
        func_str = self.func.pretty()
        if isinstance(self.func, Abs):
            func_str = f"({func_str})"
        arg_str = self.arg.pretty()
        if isinstance(self.arg, (App, Abs)):
            # Abs 已自帶外括號，App 作為右參數需加括號以維持優先級語義
            if isinstance(self.arg, App):
                arg_str = f"({arg_str})"
        return f"{func_str} {arg_str}"


# ==========================================
# 2. 語法分析器 (Parser)
# ==========================================
def tokenize(text: str) -> List[str]:
    """支援 \ 或 λ，以及英數、底線、算術符號名稱"""
    return re.findall(r'[\\λ]|[\(\)\.]|[A-Za-z0-9_\+\-\*\?\=]+', text)

def parse(text: str) -> Expr:
    tokens = tokenize(text)
    if not tokens:
        raise ValueError("輸入為空")
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected=None):
        nonlocal pos
        tok = peek()
        if expected and tok != expected:
            raise ValueError(f"語法錯誤：預期 '{expected}'，但讀到 '{tok}'")
        pos += 1
        return tok

    def parse_expr() -> Expr:
        expr = parse_atom()
        while peek() is not None and peek() not in (')', '.'):
            if peek() in ('\\', 'λ'):
                right = parse_abs()
                expr = App(expr, right)
            else:
                right = parse_atom()
                expr = App(expr, right)
        return expr

    def parse_abs() -> Expr:
        consume()  # 消耗 \ 或 λ
        params = []
        while peek() != '.':
            p = consume()
            if p is None:
                raise ValueError("語法錯誤：Lambda 定義缺少 '.'")
            params.append(p)
        consume('.')  # 消耗 .
        body = parse_expr()
        for p in reversed(params):
            body = Abs(p, body)
        return body

    def parse_atom() -> Expr:
        tok = peek()
        if tok in ('\\', 'λ'):
            return parse_abs()
        elif tok == '(':
            consume('(')
            expr = parse_expr()
            consume(')')
            return expr
        elif tok is not None and tok not in (')', '.'):
            return Var(consume())
        else:
            raise ValueError(f"語法錯誤：非預期的符號 '{tok}'")

    result = parse_expr()
    if pos < len(tokens):
        raise ValueError(f"語法錯誤：無法解析的多餘符號 '{tokens[pos:]}'")
    return result


# ==========================================
# 3. 計算核心：自由變數、α-轉換、β-歸約、巨集展開
# ==========================================
def free_vars(expr: Expr) -> Set[str]:
    if isinstance(expr, Var):
        return {expr.name}
    elif isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}
    elif isinstance(expr, App):
        return free_vars(expr.func) | free_vars(expr.arg)
    return set()

def fresh_var(base: str, avoid: Set[str]) -> str:
    prefix = re.sub(r'\d+$', '', base) or 'v'
    i = 1
    while f"{prefix}{i}" in avoid:
        i += 1
    return f"{prefix}{i}"

def substitute(expr: Expr, var: str, val: Expr, alpha_log: list) -> Expr:
    """執行 expr[var := val]，必要時自動進行 α-轉換避免變數捕捉"""
    if isinstance(expr, Var):
        return val if expr.name == var else expr
    elif isinstance(expr, App):
        return App(
            substitute(expr.func, var, val, alpha_log),
            substitute(expr.arg, var, val, alpha_log)
        )
    elif isinstance(expr, Abs):
        if expr.param == var:
            return expr
        elif expr.param in free_vars(val):
            avoid = free_vars(expr.body) | free_vars(val) | {var}
            new_param = fresh_var(expr.param, avoid)
            alpha_log.append(f"{expr.param}→{new_param}")
            renamed_body = substitute(expr.body, expr.param, Var(new_param), [])
            return Abs(new_param, substitute(renamed_body, var, val, alpha_log))
        else:
            return Abs(expr.param, substitute(expr.body, var, val, alpha_log))
    return expr

def expand_all_macros(expr: Expr, env: Dict[str, Expr], bound: Optional[Set[str]] = None) -> Expr:
    """將『有名稱』的表達式遞迴展開為 100% 『沒名稱』的純 Lambda 表達式"""
    if bound is None:
        bound = set()
    if isinstance(expr, Var):
        if expr.name not in bound and expr.name in env:
            return expand_all_macros(env[expr.name], env, bound)
        return expr
    elif isinstance(expr, Abs):
        return Abs(expr.param, expand_all_macros(expr.body, env, bound | {expr.param}))
    elif isinstance(expr, App):
        return App(
            expand_all_macros(expr.func, env, bound),
            expand_all_macros(expr.arg, env, bound)
        )
    return expr

def step_normal(expr: Expr, env: Dict[str, Expr]) -> Tuple[Optional[Expr], str]:
    """正規序 (Normal Order) 單步歸約：最左、最外層優先"""
    # 1. 展開具名常數/函數 (δ-展開)
    if isinstance(expr, Var) and expr.name in env:
        return env[expr.name], f"δ-展開 : {expr.name} ⇒ {env[expr.name].pretty()}"

    # 2. 函數應用 (Application)
    if isinstance(expr, App):
        if isinstance(expr.func, Abs):
            alpha_log = []
            res = substitute(expr.func.body, expr.func.param, expr.arg, alpha_log)
            alpha_note = f" [α-轉換: {', '.join(alpha_log)}]" if alpha_log else ""
            return res, f"β-歸約 : 代入 ({expr.func.param} := {expr.arg.pretty()}){alpha_note}"

        next_func, desc = step_normal(expr.func, env)
        if next_func is not None:
            return App(next_func, expr.arg), desc

        next_arg, desc = step_normal(expr.arg, env)
        if next_arg is not None:
            return App(expr.func, next_arg), desc

        return None, ""

    # 3. 抽象主體內部歸約 (Abstraction)
    if isinstance(expr, Abs):
        inner_env = {k: v for k, v in env.items() if k != expr.param}
        next_body, desc = step_normal(expr.body, inner_env)
        if next_body is not None:
            return Abs(expr.param, next_body), desc
        return None, ""

    return None, ""


# ==========================================
# 4. 結果逆向識別工具 (α-等價與 Church 數值解碼)
# ==========================================
def alpha_equiv(e1: Expr, e2: Expr, map1=None, map2=None, depth=0) -> bool:
    if map1 is None: map1 = {}
    if map2 is None: map2 = {}
    if type(e1) is not type(e2):
        return False
    if isinstance(e1, Var):
        return map1.get(e1.name, e1.name) == map2.get(e2.name, e2.name)
    if isinstance(e1, Abs):
        m1 = dict(map1); m1[e1.param] = depth
        m2 = dict(map2); m2[e2.param] = depth
        return alpha_equiv(e1.body, e2.body, m1, m2, depth + 1)
    if isinstance(e1, App):
        return alpha_equiv(e1.func, e2.func, map1, map2, depth) and \
               alpha_equiv(e1.arg, e2.arg, map1, map2, depth)
    return False

def decode_church_numeral(expr: Expr) -> Optional[int]:
    """自動檢查表達式是否為標準 Church 自然數 λf.λx. f (f ... x)，並算出整數值"""
    if not (isinstance(expr, Abs) and isinstance(expr.body, Abs)):
        return None
    f_param = expr.param
    x_param = expr.body.param
    if f_param == x_param:
        return None  # 如 λx.λx.x 實為 FALSE/0，但參數同名時特殊處理
    curr = expr.body.body
    count = 0
    while isinstance(curr, App):
        if isinstance(curr.func, Var) and curr.func.name == f_param:
            count += 1
            curr = curr.arg
        else:
            return None
    if isinstance(curr, Var) and curr.name == x_param:
        return count
    return None

def identify_result(expr: Expr, env: Dict[str, Expr]) -> str:
    tags = []
    # 檢查是否為任意 Church 整數
    num = decode_church_numeral(expr)
    if num is not None:
        tags.append(f"Church 整數 {num}")
    # 檢查與環境中已定義常數的 α-等價性 (展開後比對)
    for name, val in env.items():
        pure_val = expand_all_macros(val, env)
        if alpha_equiv(expr, pure_val):
            tags.append(name)
    return f"  <== 識別結果: [{', '.join(tags)}]" if tags else ""


# ==========================================
# 5. 評估與過程印出函數
# ==========================================
def evaluate(
    code: str,
    env: Optional[Dict[str, Expr]] = None,
    title: str = "",
    max_steps: int = 200,
    verbose_limit: int = 30
) -> Expr:
    """
    verbose_limit: 若步驟超過此數量，中間步驟會自動折疊，僅印出前段與後段，避免洗版
    """
    if env is None:
        env = {}
    print("=" * 80)
    if title:
        print(f"【{title}】")
    print(f"輸入程式 : {code}")

    expr = parse(code)
    print(f"標準語法 : {expr}")
    print("-" * 80)

    history = []
    curr = expr
    step = 0
    while step < max_steps:
        next_expr, desc = step_normal(curr, env)
        if next_expr is None:
            break
        step += 1
        history.append((step, desc, next_expr))
        curr = next_expr

    total = len(history)
    if total <= verbose_limit:
        for s, desc, e in history:
            print(f"步驟 {s:02d} | {desc}")
            print(f"       ⇒ {e.pretty()}")
    else:
        head_count = verbose_limit // 2
        tail_count = verbose_limit - head_count
        for s, desc, e in history[:head_count]:
            print(f"步驟 {s:02d} | {desc}")
            print(f"       ⇒ {e.pretty()}")
        print(f"   ... (中間省略 {total - verbose_limit} 步計算過程，可調大 verbose_limit 查看全部) ...")
        for s, desc, e in history[-tail_count:]:
            print(f"步驟 {s:02d} | {desc}")
            print(f"       ⇒ {e.pretty()}")

    print("-" * 80)
    status = "已達正規形式 (Normal Form)" if step < max_steps else f"達到最大步數上限 ({max_steps} 步)，提前終止"
    id_str = identify_result(curr, env)
    print(f"計算狀態 : {status}（共 {step} 步）")
    print(f"最終結果 : {curr.pretty()}{id_str}")
    print(f"嚴格括號 : {curr}\n")
    return curr


# ==========================================
# 6. 內建標準庫與完整測試展示
# ==========================================
def build_standard_env() -> Dict[str, Expr]:
    raw_defs = {
        # 1. SKI 組合子與不動點
        "I":     r"\x. x",
        "K":     r"\x y. x",
        "S":     r"\x y z. x z (y z)",
        "Y":     r"\g. (\x. g (x x)) (\x. g (x x))",

        # 2. 布林代數與條件分支
        "TRUE":  r"\x y. x",
        "FALSE": r"\x y. y",
        "IF":    r"\p a b. p a b",
        "AND":   r"\p q. p q p",
        "OR":    r"\p q. p p q",
        "NOT":   r"\p. p FALSE TRUE",
        "XOR":   r"\p q. p (NOT q) q",

        # 3. Church 自然數
        "0":     r"\f x. x",
        "1":     r"\f x. f x",
        "2":     r"\f x. f (f x)",
        "3":     r"\f x. f (f (f x))",
        "4":     r"\f x. f (f (f (f x)))",
        "5":     r"\f x. f (f (f (f (f x))))",
        "6":     r"\f x. f (f (f (f (f (f x)))))",

        # 4. 算術運算
        "SUCC":  r"\n f x. f (n f x)",
        "PLUS":  r"\m n f x. m f (n f x)",
        "MULT":  r"\m n f. m (n f)",
        "EXP":   r"\b e. e b",
        "PRED":  r"\n f x. n (\g h. h (g f)) (\u. x) (\u. u)",
        "SUB":   r"\m n. n PRED m",

        # 5. 比較與邏輯判斷
        "ISZERO": r"\n. n (\x. FALSE) TRUE",
        "LEQ":    r"\m n. ISZERO (SUB m n)",
        "EQ":     r"\m n. AND (LEQ m n) (LEQ n m)",

        # 6. 資料結構：Pair (序對) 與 List (串列節點)
        "PAIR":  r"\x y f. f x y",
        "FST":   r"\p. p TRUE",
        "SND":   r"\p. p FALSE",
        "NIL":   r"\x y. y",
        "CONS":  r"\h t. PAIR FALSE (PAIR h t)",
        "ISNIL": r"\l. FST l",
        "HEAD":  r"\l. FST (SND l)",
        "TAIL":  r"\l. SND (SND l)",

        # 7. 遞迴函數步驟定義 (配合 Y-Combinator 使用)
        # SUM_STEP: 計算 0 + 1 + ... + n
        "SUM_STEP":  r"\r n. ISZERO n 0 (PLUS n (r (PRED n)))",
        # FACT_STEP: 計算 n! (階乘)
        "FACT_STEP": r"\r n. ISZERO n 1 (MULT n (r (PRED n)))",
    }
    return {name: parse(defn) for name, defn in raw_defs.items()}


def run_all_demos(env: Dict[str, Expr]):
    # 準備 8 組經典程式（程式會自動用 expand_all_macros 產生對照的「沒名稱」純 Lambda 版本）
    demos = [
        ("1. SKI 組合子恆等定理", "S K K target"),
        ("2. 布林互斥或運算", "XOR TRUE FALSE"),
        ("3. 自動 α-轉換（防止自由變數 y 被捕捉）", r"(\x y. x y) y"),
        ("4. 自然數加法与乘法", "MULT 2 (PLUS 1 2)"),
        ("5. Kleene 前驅數與減法 (3 - 1)", "SUB 3 1"),
        ("6. 數值大小比較與條件分支 (若 2 <= 3 則回傳 4 否則 0)", "IF (LEQ 2 3) 4 0"),
        ("7. 資料結構：建立串列 [1, 2] 並取出第 2 個元素 (HEAD (TAIL list))", "HEAD (TAIL (CONS 1 (CONS 2 NIL)))"),
        ("8. Y-Combinator 匿名遞迴：計算 3! (3 的階乘 = 6)", "Y FACT_STEP 3"),
    ]

    for title, named_code in demos:
        parsed_named = parse(named_code)
        pure_expr = expand_all_macros(parsed_named, env)
        unnamed_code = pure_expr.pretty()

        # 執行「有名稱」版本
        evaluate(named_code, env=env, title=f"{title} — 【有名稱版本】", max_steps=250, verbose_limit=16)
        # 執行「沒名稱」純 Lambda 版本
        evaluate(unnamed_code, env=env, title=f"{title} — 【沒名稱 (Pure λ) 版本】", max_steps=250, verbose_limit=16)


# ==========================================
# 7. 互動式 REPL 命令列
# ==========================================
def repl(env: Dict[str, Expr]):
    print("=" * 80)
    print("進入 Lambda Calculus 互動式解譯器 (REPL)")
    print("指令說明：")
    print("  • 直接輸入表達式即可計算，例如: PLUS 2 3  或  (\\x y. x) a b")
    print("  • 輸入 pure <表達式>  : 將有名稱的表達式轉換為 100% 沒名稱的純 Lambda")
    print("  • 輸入 def <名稱> = <表達式> : 新增自訂函數，例如 def DOUBLE = MULT 2")
    print("  • 輸入 env           : 查看目前已定義的所有具名常數與函數")
    print("  • 輸入 quit 或 exit  : 離開程式")
    print("=" * 80)

    while True:
        try:
            line = input("λ> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再見！")
            break

        if not line:
            continue
        if line.lower() in ("quit", "exit"):
            print("再見！")
            break
        elif line.lower() == "env":
            print("\n【目前環境定義的名稱】")
            for k, v in env.items():
                print(f"  {k:<10} = {v.pretty()}")
            print()
        elif line.startswith("pure "):
            target = line[5:].strip()
            try:
                e = parse(target)
                pure_e = expand_all_macros(e, env)
                print(f"純 Lambda (好讀版) : {pure_e.pretty()}")
                print(f"純 Lambda (嚴格版) : {pure_e}\n")
            except Exception as ex:
                print(f"錯誤：{ex}\n")
        elif line.startswith("def "):
            parts = line[4:].split("=", 1)
            if len(parts) != 2:
                print("格式錯誤，請使用: def 名稱 = 表達式\n")
                continue
            name, body_str = parts[0].strip(), parts[1].strip()
            try:
                env[name] = parse(body_str)
                print(f"已定義：{name} = {env[name].pretty()}\n")
            except Exception as ex:
                print(f"錯誤：{ex}\n")
        else:
            try:
                evaluate(line, env=env, title="互動式計算", max_steps=300, verbose_limit=40)
            except Exception as ex:
                print(f"錯誤：{ex}\n")


if __name__ == "__main__":
    standard_env = build_standard_env()
    # 1. 先自動執行 8 大類（共 16 個有名稱/沒名稱對照）範例
    run_all_demos(standard_env)
    # 2. 接著進入互動模式讓你可以隨時自己輸入測試
    repl(standard_env)