<h1>ipl_score_predictor</h1>
<h2>Model for IITM contest: Cricket Hackathon</h2>

<ul list-style-type:disc>
<li>match_id</li>
<li>season,</li>
<li>start_date</li>
<strong><li>venue, Relevant</li></strong>
<strong><li>innings, Relevant</li></strong>
<strong><li>ball, Relevant</li></strong>
<strong><li>batting_team, Relevant</li></strong>
<strong><li>bowling_team, Relevant</li></strong>
<strong><li>striker, Relevant</li></strong>
<li>non_striker,</li>
<strong><li>bowler, Relevant</li></strong>
<strong><li>runs_off_bat, Relevant</li></strong>
<strong><li>extras, Relevant</li></strong>
<li>wides,</li>
<li>noballs,</li>
<li>byes,</li>
<li>legbyes,</li>
<li>penalty,</li>
<li>wicket_type,</li>
<li>player_dismissed,</li>
<li>other_wicket_type,</li>
<li>other_player_dismissed</li>
</ul>

<p>The data is formatted to fit the input_test_data format provided <br>
   by IITM, displayed in input_test_data.csv<br>
</p>
<h4>Format:</h4>
<p>venue, innings, ball, batting_team, bowling_team, batsmen, bowlers<br></p>

<h3>TODO:</h3>
<p>-Calculate runs after each ball - <strong>Done</strong></p>
<p>-CSV Database for all relevant data - <strong>Done</strong></p>
<p>-Filter data for first 6 overs. (i.e just before 6.1) - <strong>Done</strong></p>
<p>-Relations between relevant data and runs visualized</p>
