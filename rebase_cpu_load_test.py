import subprocess
import time
import re
from datetime import datetime

# 配置
DURATION = 600  # 10分钟（秒）
CPU_THRESHOLD = 8.0
CHECK_INTERVAL = 5  # 每5秒采样一次

# 可忽略的进程（你可以自己补充）
IGNORE_PROCESSES = [
    "top",
    "logcat",
    "adbd"
]


def get_top_output():
    """执行 adb shell top 并获取输出"""
    try:
        result = subprocess.check_output(
            ['adb', 'shell', 'top', '-n', '1', '-b'],
            encoding='utf-8'
        )
        return result
    except Exception as e:
        print("Error running adb:", e)
        return ""


def parse_top(output):
    """解析 top 输出，提取 CPU 使用率"""
    high_cpu_processes = []

    for line in output.splitlines():
        # 匹配 CPU % 和进程名（不同设备格式略有差异，这里做通用处理）
        match = re.search(r'(\d+\.?\d*)%\s+\S+\s+\S+\s+\S+\s+(.+)', line)
        if match:
            cpu = float(match.group(1))
            process = match.group(2).strip()

            # 排除调试进程
            if process in IGNORE_PROCESSES:
                continue

            if cpu > CPU_THRESHOLD:
                high_cpu_processes.append((process, cpu))

    return high_cpu_processes


def main():
    print("=== CPU Idle Test Start ===")
    print(f"Duration: {DURATION}s, Threshold: {CPU_THRESHOLD}%")

    start_time = time.time()
    issue_found = False

    while time.time() - start_time < DURATION:
        output = get_top_output()
        processes = parse_top(output)

        if processes:
            issue_found = True
            print("\n[ALERT] High CPU detected!")
            for p, cpu in processes:
                print(f"Process: {p}, CPU: {cpu}%")

        time.sleep(CHECK_INTERVAL)

    print("\n=== Test Finished ===")

    if issue_found:
        print("❌ RESULT: FAIL (High CPU process detected)")
    else:
        print("✅ RESULT: PASS (No abnormal CPU usage)")


if __name__ == "__main__":
    main()