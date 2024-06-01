# pokemon-battle-AI
## Project Summary</b>
<b> This repository is part of our Erdos Institute May-Summer 2024 Data Science Boot Camp project. We aim to create a model that can predict the likely winners of competitive Pokémon Video Game Championships (VGC) battles, utilizing replay records from [Pokémon Showdown!](https://pokemonshowdown.com/), a popular online battle simulator. This format is a highly competitive, ‘doubles battle’ where each player selects four out of six Pokémon to battle against their opponent, with two Pokémon active for each player at a time. By reconstructing these replay records into text files, we can extract turn-by-turn information from over 10,000+ battles and curate a database to train our classifiction models.

</b>
<br>

![Screenshot of a online battle on Pokémon Showdown](https://github.com/maryanncollins/pokemon-battle-AI/assets/133918905/43c03791-0e0e-4e27-a5e6-db8a49e4ed4a)
<br>


## Data Gathering <br>
### Description of the Dataset:
The dataset is compiled from replay logs on Pokémon Showdown. In competitive Pokémon, there are many different battle formats, each with their own rules, regulations, and restrictions. For the purposes of this project, we have chosen to use battle logs that follow the current Gen 9 VGC 2024 Reg G ruleset. Additionally, we have chosen to sort replays by (highest) rating so we can pull data logs from matches played between high ranking players. Replays records can be scrapped directly from the Pokémon Showdown website and reconstructed into text files. Each battle log begins with the following information: player information (name/rank), the battle format/tier, and the names of each pokémon on each team. The rest of the log is sorted by turn, listing the series of decisions each player made and the resulting outcome. At the end, the log states the winner and loser of the match. The battle log ends with the result of the match, stating which player is the winner and which player lost, with +/- adjustments made to their rankings.
<br>
<br>

## Stakeholders & KPIs <br>
### Stakeholders:
- Competitive Pokémon battling community, ranked and casuals players
- Pokémon Showdown- to track changes in the metagame
- Official Pokémon Tournaments Organizers (such as The Pokémon Company International, TPCi; The Pokémon Company, TPC; Pokémon Korea, TPCK)

### Key Performance Indicators:
- Ability to predict the likely winner of a battle given team composition, movesets, abilities, items used, battle conditions, ect.
- Comparable or improved performance relative to other available PS battle prediction tools

### Initial Questions:
- Which factors have the most significant impact on the outcome of a battle? How many rounds of a battle are needed to train a model on to predict a winner? 
- What is the ideal output for this model? Should we try to predict a winner after every round or just at the start of the battle?
- By utilizing data gathered from previous battles, what level of accuracy can be achieved in predicting the winner of a future battle between two new teams?

