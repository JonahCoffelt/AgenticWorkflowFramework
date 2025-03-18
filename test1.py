import subprocess

result = subprocess.run(["python3", "test2.py"], capture_output=True, text=True)

print(result.stdout)