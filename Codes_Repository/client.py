import requests

def main():
    url = "http://localhost:8080/calculate"
    angle = float(input("Enter angle: "))
    unit = input("Degree or Radian? ").strip().lower()
    func = input("Function (sin/cos/tan): ").strip().lower()
    
    data = {
        "angle": angle,
        "unit": unit,
        "function": func
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Result: {response.json()['result']}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    main()
