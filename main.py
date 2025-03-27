from src.utils import *

if __name__ == '__main__':
    data = load_data('data/sample_input.json')
    scheduler = load_scheduler(data)

    scheduler.solve()