import asyncio


async def add_input() -> float:
    print('inputs: ')
    x, y = tuple(map(float, input("Enter two numbers: ").split(" ")))
    return x + y

async def multiply_input(x: int) -> float:
    y = float(input(f"Enter number to multiply with {x}: "))
    return x * y

async def display_output(output: ...) -> None:
    print(f"Final Output: {output}")

async def get_nums() -> list[float]:
    return list(map(float, input("Enter numbers: ").split(" ")))

async def get_sum(*args):
    value = float(input(f"What is the sum of these numbers {[arg for arg in args]}: ")) 
    return value

async def auto_sum(nums: list) -> float:
    await asyncio.sleep(1.0)
    value = float(sum(nums))
    return value

async def show_readings(human_value: float, AI_value: float) -> None:
    print(f"Human Reading: {human_value}\nAI Reading: {AI_value}")