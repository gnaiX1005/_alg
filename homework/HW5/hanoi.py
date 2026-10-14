# 河內塔問題（Tower of Hanoi）
# 目標：把 n 個盤子從來源柱 src 全部移到目標柱 dst，過程中大盤不能壓在小盤上。
# 本檔提供兩種解法：
#   1. hanoi_recursive  -> 遞迴解法
#   2. hanoi_iterative  -> 非遞迴解法（禁止遞迴，只用迭代）


def hanoi_recursive(n, src='A', dst='C', aux='B', moves=None):
    """遞迴解法。

    想法：先把上面 n-1 個盤子搬到輔助柱 aux（遞迴），
    再搬最大的第 n 個盤子到 dst，最後把 n-1 個盤子從 aux 搬回 dst（遞迴）。
    """
    if moves is None:
        moves = []
    if n == 0:
        return moves
    hanoi_recursive(n - 1, src, aux, dst, moves)   # n-1 個：src -> aux
    moves.append((n, src, dst))                    # 最大盤：src -> dst
    hanoi_recursive(n - 1, aux, dst, src, moves)   # n-1 個：aux -> dst
    return moves


def hanoi_iterative(n, src='A', dst='C', aux='B'):
    """非迴圈（迭代）解法，完全不使用遞迴。

    規則：奇數步移動最小盤、偶數步移動另外兩柱中可合法移動的盤子。
    最小盤的環繞方向由 n 的奇偶決定：
        n 為奇數：src -> dst -> aux -> src ...
        n 為偶數：src -> aux -> dst -> src ...
    """
    pegs = {src: [], dst: [], aux: []}
    for d in range(n, 0, -1):        # 大的盤子在下面
        pegs[src].append(d)

    order = [src, dst, aux] if n % 2 == 1 else [src, aux, dst]
    index = {p: i for i, p in enumerate(order)}
    pos = src                        # 最小盤目前所在的柱子
    moves = []
    total = 2 ** n - 1

    for step in range(1, total + 1):
        if step % 2 == 1:
            # 奇數步：移動最小盤（盤子 1）沿環繞方向走一格
            nxt = order[(index[pos] + 1) % 3]
            moves.append((1, pos, nxt))
            pegs[pos].pop()
            pegs[nxt].append(1)
            pos = nxt
        else:
            # 偶數步：在另外兩柱之間，把「小盤疊到大盤（或空柱）」上
            x, y = [p for p in order if p != pos]
            tx = pegs[x][-1] if pegs[x] else None
            ty = pegs[y][-1] if pegs[y] else None
            if tx is None:
                s, t, d = y, x, ty
            elif ty is None:
                s, t, d = x, y, tx
            elif tx < ty:
                s, t, d = x, y, tx
            else:
                s, t, d = y, x, ty
            moves.append((d, s, t))
            pegs[s].pop()
            pegs[t].append(d)

    return moves


def print_moves(moves):
    for i, (disk, s, t) in enumerate(moves, 1):
        print(f"  第 {i:2d} 步: 將盤子 {disk} 從 {s} 移到 {t}")


if __name__ == "__main__":
    for n in [1, 2, 3, 4]:
        print(f"===== n = {n} 個盤子（最少需要 2^{n}-1 = {2 ** n - 1} 步）=====")

        rec = hanoi_recursive(n)
        it = hanoi_iterative(n)

        print(f"[遞迴]   共 {len(rec)} 步：")
        print_moves(rec)
        print(f"[非遞迴] 共 {len(it)} 步：")
        print_moves(it)

        same = rec == it
        print(f"兩種解法步數相同，且每一步的盤子與柱子都一致：{same}\n")
