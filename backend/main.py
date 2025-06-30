import requests

def test_get():
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}")

if __name__ == '__main__':
    test_get()
