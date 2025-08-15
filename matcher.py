from database import (
    get_all_volunteers,
    get_help_request_by_email,
    admin_all_users,
    add_match
)

# Match requester to volunteer
def match_request_to_volunteer(requester_email):
    requester = get_help_request_by_email(requester_email)
    if not requester:
        return []

    matches = []
    for volunteer in get_all_volunteers():
        if (volunteer["skills"] == requester["skills"] or
            volunteer["skills"] == "Other" or
            requester["skills"] == "Other") and volunteer["availability"] == requester["availability"]:
            
            # Add to match list
            match_info = {
                "request_name": requester["name"],
                "request_email": requester["email"],
                "volunteer_name": volunteer["name"],
                "volunteer_email": volunteer["email"],
                "skill": requester["skills"],
                "location": volunteer["location"],
                "availability": volunteer["availability"]
            }
            matches.append(match_info)

            # Store in DB
            add_match(
                requester["name"],
                requester["email"],
                volunteer["name"],
                volunteer["email"],
                requester["skills"],
                None
            )
    return matches

# Match volunteer to requester
def match_volunteer_to_request(volunteer_email):
    # Get volunteer info from main users table
    users = admin_all_users()
    volunteer = next((u for u in users if u["email"] == volunteer_email), None)
    if not volunteer:
        return []

    matches = []
    for user in users:
        if user["role"] == "Requester":
            if (user["skills"] == volunteer["skills"] or
                user["skills"] == "Other" or
                volunteer["skills"] == "Other") and user["availability"] == volunteer["availability"]:
                
                match_info = {
                    "request_name": user["name"],
                    "request_email": user["email"],
                    "volunteer_name": volunteer["name"],
                    "volunteer_email": volunteer["email"],
                    "skill": volunteer["skills"],
                    "location": user["location"],
                    "availability": user["availability"]
                }
                matches.append(match_info)

                # Store in DB
                add_match(
                    user["name"],
                    user["email"],
                    volunteer["name"],
                    volunteer["email"],
                    volunteer["skills"],
                    None
                )
    return matches
