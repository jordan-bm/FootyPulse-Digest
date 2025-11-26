from footypulse.api.football_api import get_leagues

def main():
    print("Testing API-Football connection...")
    data = get_leagues()
    print("Success. Sample output:")
    print(data["response"][:2])  # print two leagues

if __name__ == "__main__":
    main()
