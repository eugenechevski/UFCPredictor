# displayed/display.py
def display_event_predictions(event_data, predictions):
    """Formats and displays predictions for the entire UFC event card."""
    for fight, prediction in zip(event_data["fights"], predictions):
        print(f"Fight: {fight['fighter1']} vs {fight['fighter2']}")
        print(f"Prediction: {prediction['win_probability']*100:.2f}% chance of {prediction['method_of_victory']}")
        print("-" * 30)

def display_fighter_stats(fighter_data):
    """Displays the stats of a single fighter."""
    print(f"Fighter: {fighter_data['fighter_name']}")
    print("Stats:", fighter_data['stats'])
