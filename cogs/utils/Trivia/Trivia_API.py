import requests

def get_question(Number_of_Questions: int = 1, Category: int = None, Difficulty: str = None, Type: str = None):
    url = f"https://opentdb.com/api.php?amount={Number_of_Questions}"
    if Category is not None:
        url += f"&category={Category}"
    if Difficulty is not None:
        url += f"&difficulty={Difficulty}"
    if Type is not None:
        url += f"&type={Type}"
    try:
        response = requests.get(url).json()
        error = response["response_code"]
        return Handle_Error(error) if error > 0 else response["results"]
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the API request: {e}"



def catagory_lookup(id: int = None):
    url = "https://opentdb.com/api_category.php"
    categories = requests.get(url).json()["trivia_categories"]

    if id is None:
        return categories
    matching_categories = [category for category in categories if category["id"] == id]
    return matching_categories[0] if matching_categories else None
    

def Handle_Error(e):
    if e == 1:
        return "Code 1: No Results: Could not return results. The API doesn't have enough questions for your query. (Ex. Asking for 50 Questions in a Category that only has 20.)"
    if e == 2:
        return "Code 2: Invalid Parameter: Contains an invalid parameter. Arguements passed in aren't valid. (Ex. Amount = Five)"
    if e == 3:
        return "Code 3: Token Not Found: Session Token does not exist."
    if e == 4:
        return "Code 4: Token Empty: Session Token has returned all possible questions for the specified query. Resetting the Token is necessary."
