i4Games Record Collector

i4Games.eu has hosted Unreal Tournament 1999 BunnyTrack servers since the early 2000s, and whilst the game is no longer fully active - years and years were spent mastering thousands of maps.

As i4Games does not provide an easy way to parse through records, this tool can be used to scrape the data for all active users.

It searches every record page (certified and non-certified), and concatenates them for store a DB of the players' best times on each map. In the case that a user has a non-certified time faster than their certified time, both records will be saved.

This tool is also able to search the records of *all* banned players, even if the accounts can no longer be accessed through traditional ways. Most banned player IDs have been mapped with the exception of a few. A player is considered banned when their record times are not on leaderboards (usually due to cheating).

Install requirements via pip install -r requirements.txt

Run using python main.py

This tool will take about 4/5 hours to completely run, please do not abuse it, and use at your own risk as it sends a lot of requests over that time. The most recent record database will always be found in the compiled\ folder.
