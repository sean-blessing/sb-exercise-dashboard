from src.strava.activities import get_all_activities

activities = get_all_activities()

print()
print(f"Total activities retrieved: {len(activities)}")
print()

first_activity = activities[0]

print("First activity:")
print(f"  ID: {first_activity['id']}")
print(f"  Name: {first_activity['name']}")
print(f"  Type: {first_activity['type']}")
print(f"  Distance: {first_activity['distance']} meters")