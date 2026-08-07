# Helper utilities if needed for future formatting
def validate_non_empty(prompt_text):
    while True:
        val = input(prompt_text).strip()
        if val:
            return val
        print("Input cannot be empty. Try again.")