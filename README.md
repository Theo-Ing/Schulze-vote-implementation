# Schulze vote counter

This small library is made to count votes where several nominees can be ranked in order of preference. The
implementation uses the Schulze method, the steps of which can be found [here](https://en.wikipedia.org/wiki/Schulze_method).

All necessary user interaction is done through vote_retriever.py and vote_counter.py


## Raw data format

Raw data should be saved in a txt file (in the same folder as the code files) where each row is a vote in the
following format:
<pre>
name_1,name_2 name_3 name_4
</pre>
(See test cases)

This means that name_1 and name_2 are prioritized equally but they are both preferred over name_3
who is preferred over name_4

## Vote retriever

To format the votes to above specification the program [*vote_retriever.py*](https://github.com/Theo-Ing/Schulze-vote-implementation/blob/main/vote_retriever.py) can be used.
Here a simple UI will allow you to define the number of candidates (excluding vacant), as well as whether 
you wish to append new votes to a file or create a new file (in either case you will select the location 
of the file). Input of a singular vote is done through the indexing given in the UI. With indexing<br />
<pre>0 - Candidate_A
1 - Candidate_B
2 - Candidate_C
3 - Candidate_D
4 - Vacant</pre>
and a vote with the following priority choices
<pre>Candidate_A (2)
Candidate_B (3)
Candidate_C (1)
Candidate_D (2)
Vakant ()</pre>
The input should be:<br />
<pre>2 03 1</pre> followed by enter.
This corresponds to the indices in choice order, with no space between choices meaning equal preference.
The resulting vote will then be saved as
<pre>Candidate_C Candidate_A,Candidate_D Candidate_B</pre>

## Vote counter

When running [*vote_counter.py*](https://github.com/Theo-Ing/Schulze-vote-implementation/blob/main/vote_counter.py) you will be prompted to select:
<pre>
- Name of the position
- Number of vacancies
- The raw data file
- The directory where the report should be saved
</pre>
Then a report txt file will be created called *\<positionName\>_report.txt* containing all relevant info.
In the unlikely event of a tie this will be stated in the report and it is up to user discretion how this is handled.

## Tutorial case

For practice a tutorial case is provided along with the expected result so that you may confirm your understanding
of the programs before implementing them on actual elections.
