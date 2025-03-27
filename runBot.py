import subprocess
import time

while True:
    print("🚀 Starting Karen bot...")
    process = subprocess.run(["python", "KarenGemini.py"])  # Run bot script

    # If bot exits with status 1, shut down completely
    if process.returncode == 1:
        print("❌ Karen has shut down. Exiting monitor script.")
        break

    # If bot exits with status 2, restart it
    if process.returncode == 2:
        print("♻️ Restarting Karen in 5 seconds...")
        time.sleep(5)  # Delay before restart
