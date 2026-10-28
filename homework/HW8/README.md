# 第7週習題：優化算法 — 旅行推銷員問題（TSP）

使用下列五種方法解決旅行推銷員問題（Traveling Salesman Problem, TSP）：

1. 改良法（2-opt）
2. 爬山演算法（Hill Climbing）
3. 模擬退火法（Simulated Annealing）
4. 梯度下降法（Gradient Descent，連續鬆弛）
5. 貪婪演算法（最近鄰居）

測試資料使用 20 個隨機城市（固定亂數種子 42），所有方法使用同一組資料進行比較。

## 檔案

- `tsp.py`：五種演算法實作、比較與繪圖
- `README.md`：本說明文件

## 執行方式

```bash
pip install numpy matplotlib
python tsp.py
```

## 結果說明

程式會印出各方法的路徑長度、耗時與路徑順序，並輸出 `tsp_results.png` 顯示五種方法的路徑比較圖。

## 參考

- [原始參考解答（week7-tsp）](https://github.com/ccc115a/alg/tree/main/_more/homework/week7-tsp)
- [Claude 分享連結](https://claude.ai/share/36c286d7-0b9d-4e67-8684-76733347dffc)
