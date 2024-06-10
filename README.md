# pokemon-battle-AI
## Project Objective</b>
<b> We aim to create an AI model that can predict the likely winners of competitive Pokémon Video Game Championships (VGC) battles, utilizing replay records from Pokémon Showdown![^1], a popular online battle simulator. This format is a highly competitive, ‘doubles battle’ where each player selects four out of six Pokémon to battle against their opponent, with two Pokémon active for each player at a time. By reconstructing these replay records into text files, we can extract turn-by-turn information from over 10,000+ battles and curate a database to train our classifiction models.</b>
<br>

![Screenshot of a online battle on Pokémon Showdown](https://github.com/maryanncollins/pokemon-battle-AI/assets/133918905/1b858f43-cdbe-48bc-a0f5-3f8fffec6c6a)
<br>

## Stakeholders & KPIs <br>
### Stakeholders:
- Competitive Pokémon battling community, ranked and casuals players
- Pokémon Showdown- to track changes in the metagame
- Official Pokémon Tournaments Organizers (such as The Pokémon Company International, TPCi; The Pokémon Company, TPC; Pokémon Korea, TPCK)

### Key Performance Indicators:
- Ability to predict the likely winner of a battle given team composition, movesets, abilities, items used, battle conditions, ect.
- Comparable or improved performance relative to other available PS battle prediction tools

### Initial Questions: <i>
- Which factors have the most significant impact on the outcome of a battle? How many rounds of a battle are needed to train a model on to predict a winner? 
- What is the ideal output for this model? Should we try to predict a winner after every round or just at the start of the battle?
- By utilizing data gathered from previous battles, what level of accuracy can be achieved in predicting the winner of a future battle between two new teams?</i>


## Workflow <br>
![Workflow for Modeling](https://github.com/maryanncollins/pokemon-battle-AI/assets/133918905/75e4b3b0-fa99-48d4-9b0e-6a527fefc8f4)
<br>

### Data Gathering:
In competitive Pokémon, there are many different battle formats, each with their own rules, regulations, and restrictions. For the purposes of this project, we have chosen to use battle logs that follow the current [Gen 9] VGC 2024 Reg G ruleset. Additionally, we have chosen to sort replays by (highest) rating so we can pull data logs from matches played between high ranking players. Replays records are scraped directly from the Pokémon Showdown! website and reconstructed into text-based `.log` files containing the information for each battle, with a total of 14,474 unique battles  collected. Each battle log begins with the following information: player information (name/rank), the battle format/tier, and the names of each pokémon on each team. The rest of the log is sorted by turn, listing the series of decisions each player made and the resulting outcome. The battle log ends with the result of the match, stating which player is the winner and which player lost, with +/- adjustments made to their rankings. Data not available from battle logs, such as the base stats and typing for each Pokémon, was sourced from Smogon[^2] (the creator of Pokémon Showdown!) as `.json` files. Data from battle `.log` and `.json` files were parsed into dataframes and then combined into one database.

### Feature Engineering & EDA:
Based on exploratory data analysis, the database was filtered to remove battles that lasted less than five turns or ended in a tie. Battles were sorted by rating so only battles between players above a certain decent ranking are considered for training. All battle parameters were transformed into a 492-dimensional vector that was used for training the models described below. This vectorized dataset contained the conditions for each battle (weather, field, terrain) as well as the attributes of both player’s pokémon played during the match.

> [!TIP]
> - Please refer to `data/data_explanation.txt` for an explnataion of the full dataset
> - See `Exploratory_Data_Analysis/trainingdata02` for the most recent recent EDA plots

<br>

## Modeling Approach
<b>Several different classification models were generated. For each model, the main Key Performance Indicator is the accuracy of the predicted winner compared to the actual winner of a battle. Below is a description for the most interesting models:</b>

1. <b>Baseline Model:</b>
The baseline model used is a coin-flip with 50% chance of predicting the correct winner.

2. <b>RandomForest Model:</b>
The features used for this model only considered the attributes of the four Pokémon (two Pokémon per player) that started at turn one, from the vectorized dataset. The initial accuracy in predicting the correct winner was 61%. When we revised this model to consider the attributes of all Pokémon from every turn of the battle as well as the battle conditions from the whole vectorized data, the accuracy increased to 76%.

3. <b>ExtraTree Model:</b>
We also generated an ExtraTree Classifier, using the initial features from the RandomForest Model (only considering the attributes of the starting Pokémon). The initial accuracy in predicting the correct winner was the same as the first RandomForest Model (61%). When we used the revised feature set that considers the attributes of all Pokémon and the battle conditions throughout the match, the accuracy increased to 78% and performed slightly better than the RandomForest Model.

4. <b>Neural Net (NN) Models:</b>
The first iteration of the NN achieved a 61% success rate in predictions. However, it became apparent that this model was heavily influenced by the total amount of HP of all remaining Pokémon on each side. To reduce the influence of the remaining total HP, the model was adjusted. However the accuracy rate for this Weighted NN Model modestly dropped to 55%.

> [!IMPORTANT]
> See `modeling` for all our classifiction models
 
<br>

## Results & Conclusions
<b>Compared to our baseline model (50% accuracy), our other classification models performed better, with an accuracy of 55% - 78% to predict the correct winner. The best overall model was the ExtraTree Classifier, which incorporated the whole vectorized dataset, including the battle conditions as well as attributes for each Pokémon as features, and was trained on every turn for each battle. While neither of our Neural Networks performed as well as the ExtraTree Classifier, we were able to use the NN for more in-depth team analysis and explore the impact the most popular Pokémon have on the metagame.</b>

![Performace of Neural Network Models](https://github.com/maryanncollins/pokemon-battle-AI/assets/133918905/1c5c5448-02b7-42c3-a0f5-5dc0635196cc)

### Modeling Insights:
In addition to predicting the winner of each battle, we also explored how individual Pokémon impact the battle outcomes by modifying the input vectors—essentially swapping one Pokémon for another and observing changes in the model's output. This analysis revealed that Chi-Yu and Gholdengo, two Pokémon known for their medium speed, moderate durability, and powerful special attacks, play similar roles when on a team. This analysis also revealed the unique advantages of certain Pokémon. For example, although Incinaroar and Calyrex-Ice are two of the most-played Pokémon, they serve completely different roles; Calyrex-Ice is a strong Physical Attacker while Incinaroar is the strongest supportive Pokémon.

### Modeling Challenges:
We encountered a number of challenges; mainly concerning dataset variability and the computational costs of training various models. In addition, competitive Pokémon battling involves a significant level of uncertainty due to random chance events, information unavailable to both players, and a highly variable set of Pokémon. Such factors were difficult to fully account for in our models, as reflected in each of their accuracy rates, yet highlights the complexity of the game and dataset.
<br>
<br>

## Future Directions & Applications:
We believe this method of analyzing Pokémon battles holds promising potential for future applications in broader competitive strategy development and training. By understanding the roles and impact of specific Pokémon more deeply, players can refine team building and battle tactics more strategically. This model could also be used by Pokémon Showdown! and official Pokémon tournaments organizers (such as Nintendo and The Pokémon Company) to track changes in the metagame as new rulesets are released. Lastly, this approach could be adapted to other complex systems where numerous variables influence outcomes, such as other strategic turn-based game theory simulations.
<br>
<br>
<br>

> [!NOTE]
> ## Project Information
> This repository is associated with our Erdős Institute[^3] May-Summer 2024 Data Science Boot Camp project.
> ### Team Members
> - Mary Ann Collins
> - Izabella Freitas
> - Hongyi Shen
> - Guoqing Zhang
> - Tianyu Zhu
> 
> <i>project mentor: Zach Hafen-Saavedra </i>
> <br>
> <br>
> We would like to thank Steven Gubkin, Alec Clott, and Roman Holowinsky of The Erdős Institute as well as The Pokémon Community!


[^1]: “Pokémon Showdown! Battle Simulator” https://replay.pokemonshowdown.com/
[^2]: “Smogon University pokemon-showdown” https://github.com/smogon/pokemon-showdown/tree/master/data
[^3]: “The Erdős Institute” https://www.erdosinstitute.org/
