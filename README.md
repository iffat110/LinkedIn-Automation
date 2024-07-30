# LinkedIn-Automation

## Problem:
The objective of this script is to automate the process of sending connection requests on LinkedIn. Given a list of LinkedIn profile URLs, the script should log in to a LinkedIn account, visit each profile, and send a personalized connection request. Additionally, the script should handle scenarios where the connect button is not directly accessible and should also manage OTP verification if required.

## Approach:

### Login Functionality (ll_login):

Created a function to log in to LinkedIn using Selenium. It handles OTP input if prompted and checks for successful login.
Send Connection Request (send_connection_request and send_connection_request_from_more_menu):

Implemented functions to send connection requests. These functions try to locate the connect button either on the main profile page or within the "More" actions menu. If successful, they send a connection request with or without a personalized note.
Main Automation (search_and_connect):

This is the main function that coordinates the workflow. It starts by logging in, iterates through the list of profile URLs, attempts to send connection requests, and handles cases where connections could not be sent. It logs the start and end time of the process and stores URLs where connection requests were unsuccessful.

## Working?
Login (ll_login):

The function initializes a Selenium WebDriver instance, navigates to LinkedIn's login page, enters the provided email and password, and clicks the "Sign in" button. If an OTP is required, the user is prompted to enter it.
Sending Connection Requests:

Direct Connect (send_connection_request):
This function attempts to find the "Connect" button on the profile page, clicks it, and sends a connection request with an optional note.
Connect via 'More' Menu (send_connection_request_from_more_menu):
If the "Connect" button isn't available directly, this function tries to find it in the "More actions" menu and sends the request similarly.
Processing Profiles (search_and_connect):

This function logs the start time, logs in to LinkedIn, and processes each profile URL. It checks if the profile is already connected (by looking for the "Message" button), and if not, it tries to send a connection request. URLs where the connection request failed are saved to a CSV file for future review.
Conclusion
The script successfully automates sending LinkedIn connection requests by:

Logging in to LinkedIn.
Navigating through given profile URLs.
Sending connection requests, handling different UI scenarios.

## Future Implementation
Error Handling and Logging: Enhance error handling to cover more scenarios and add detailed logging for debugging and monitoring purposes.

Captcha Handling: Implement methods to handle captchas, possibly using captcha-solving services or manual intervention.

Customization: Allow customization of the connection message per profile to make the requests more personalized.

Session Management: Implement session management to handle re-logins and maintain session states to avoid frequent logins.

Headless Mode and Proxy Usage: Add support for headless mode and proxy rotation to minimize the risk of being flagged by LinkedIn's security systems.

Rate Limiting and Pausing: Implement rate limiting and pauses to mimic human behavior and prevent account suspension.
