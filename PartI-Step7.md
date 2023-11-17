Part I-Step 7

How is the logged in user being kept track of?

    They are being tracked by the set up for a global user in @app.before_request. This sets the global user as the current user and applies it to the variable g.user. This global user is set in the session so that the variable can be used across all pages throughout the app.

What is Flask's g object?

    It is a query to User model that pulls all the data from PostGreSql server to get a row of just the signed in user's data to be used globally until they are signed out.

What is the purpose of add_user_to_g?

    This is the pre-route taht sets up the global user variable to be used throughout the duration of the person being signed in no matter what route they are on.

What does @app.before_request mean?

    This meant the request is made before the first route is ran in a specific session.