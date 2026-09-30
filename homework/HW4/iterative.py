def sqrt_newton(s: float, tol: float = 1e-9, max_iter: int = 100) -> float:
    """使用牛頓迭代法求解正數 s 的平方根。

    :param s: 欲開方的正數
    :param tol: 誤差容許值 (tolerance)
    :param max_iter: 最大安全迭代次數，避免無限迴圈
    :return: 近似平方根
    """
    if s < 0:
        raise ValueError("負數在實數範圍內沒有平方根")
    if s == 0:
        return 0.0

    # 1. 設定初始猜測值 (Initial Guess)
    x = s / 2.0 if s >= 1.0 else 1.0

    # 2. 進入迭代循環
    for i in range(1, max_iter + 1):
        x_next = 0.5 * (x + s / x)

        # 列印每一步的收斂軌跡
        print(f"迭代第 {i:2d} 次: x = {x_next:.10f}, 差距 = {abs(x_next - x):.2e}")

        # 3. 檢查終止條件
        if abs(x_next - x) < tol:
            return x_next

        x = x_next

    return x


# 測試：計算 S = 612 的平方根 (真實值約 24.7386337537...)
target = 612
result = sqrt_newton(target)
print(f"\n最終解: {result:.10f}")
print(f"驗算 result^2: {result**2:.10f}")