# 自製 map / filter / reduce，並在「禁止迴圈」下完成泡沫排序
#
# 規則：
#   1. map / filter / reduce 全部自己寫（用遞迴，不用任何 for/while）。
#   2. 泡沫排序也完全不使用迴圈，只用上面自製的函數 + 遞迴完成。


def my_reduce(f, xs, init):
    """把 xs 從左到右用 f 合併成一個值，起始值為 init（遞迴實作）。"""
    if not xs:
        return init
    return my_reduce(f, xs[1:], f(init, xs[0]))


def my_map(f, xs):
    """對 xs 每個元素套用 f，回傳新 list（用 my_reduce 實作）。"""
    return my_reduce(lambda acc, x: acc + [f(x)], xs, [])


def my_filter(pred, xs):
    """保留 pred 為真的元素（用 my_reduce 實作）。"""
    return my_reduce(lambda acc, x: acc + [x] if pred(x) else acc, xs, [])


def bubble_pass(xs):
    """一趟泡沫排序：用 my_reduce 掃過相鄰元素，把最大的推到最後。

    狀態 (done, carried)：done 是目前放好的前面部分，carried 是正在往後冒的盤子。
    """
    def step(acc, cur):
        done, carried = acc
        if carried is None:            # 第一個元素先拿著
            return (done, cur)
        if carried > cur:              # 左大右小 -> 交換，carried 繼續往後冒
            return (done + [cur], carried)
        return (done + [carried], cur)  # 順序正確 -> carried 落地，換 cur 往後冒

    done, carried = my_reduce(step, xs, ([], None))
    return done if carried is None else done + [carried]


def bubble_sort(xs):
    """泡沫排序：每趟把最大值推到最後，再遞迴處理前面的部分。"""
    if len(xs) <= 1:
        return xs
    passed = bubble_pass(xs)                     # 最後一個已就定位
    return bubble_sort(passed[:-1]) + [passed[-1]]


def is_sorted(xs):
    """檢查是否由小到大排好（用 my_reduce 實作，不用迴圈）。"""
    pairs = list(zip(xs, xs[1:]))
    return my_reduce(lambda acc, p: acc and p[0] <= p[1], pairs, True)


if __name__ == "__main__":
    print("===== 自製 map / filter / reduce 示範 =====")
    nums = [1, 2, 3, 4, 5, 6]
    print("原始          :", nums)
    print("my_map(平方)  :", my_map(lambda x: x * x, nums))
    print("my_filter(偶) :", my_filter(lambda x: x % 2 == 0, nums))
    print("my_reduce(加) :", my_reduce(lambda a, b: a + b, nums, 0))

    print("\n===== 泡沫排序（禁止迴圈，只用自製函數 + 遞迴）=====")
    tests = [
        [5, 2, 9, 1, 5, 6],
        [3, 3, 1, 2, 8, 0, 7],
        [10, -1, 3, 0, -5],
        [1],
        [],
    ]
    for data in tests:
        result = bubble_sort(data)
        ok = (result == sorted(data)) and is_sorted(result)
        print(f"原始: {data}  ->  排序後: {result}  正確: {ok}")
