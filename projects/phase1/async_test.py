import asyncio
import time

async def fetch_data(name: str, delay: int):
    print(f"{name}: 開始")
    await asyncio.sleep(delay)  # I/O待ちの模擬
    print(f"{name}: 完了（{delay}秒後）")
    return f"{name}のデータ"

async def main():
    # 順番に実行（同期的）
    print("=== 順番に実行 ===")
    start = time.time()
    result1 = await fetch_data("タスクA", 2)
    result2 = await fetch_data("タスクB", 1)
    print(f"結果: {result1}, {result2}")
    print(f"合計経過時間: {time.time() - start:.1f}秒\n")

    # 同時に実行（非同期的）
    print("=== 同時に実行 ===")
    start = time.time()
    results = await asyncio.gather(
        fetch_data("タスクC", 2),
        fetch_data("タスクD", 1),
    )
    print(f"結果: {results}")
    print(f"合計経過時間: {time.time() - start:.1f}秒")

asyncio.run(main())
