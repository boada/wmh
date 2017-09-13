# WTC Tournament Analysis/Forecast

## Intro

This project has two parts.
 - 1. Try to use previous WTC tournament results to forecast the results from the upcoming WTC.
 - 2. Using the tournament information (e.g., lists) to see if we can get deeper understanding of the meta. A basic question could be "do lists with more free points win more?"

For the forecasting portion. We've assigned each player (603 unique as of 2016) an [Elo](https://en.wikipedia.org/wiki/Elo_rating_system) score initialized at 1500. We then update their individual rankings at the end of each round. If the Elo ranking was a good predictor of final placement, then we'd expect that the team with the highest combined Elo rank would win the tournament (spoiler: it's not).

In each matchup we also calculate the probability of each player winning the game (`pwin`). This is defined as:

    1 / (1 + 10 ** ((B - A) / 400))

This works really well for Chess where the game is balanced well. In Warmachine and Hordes their are many ways to win and many different match ups that could possibly occur. Currently, `pwin` does not take any of this additional information into account. In the future we will define corrections to the Elo ranking which attempt to take into consideration things like the margin of victory (MOV) and other information, such as the specific match up. Most of these corrections are entirely data driven. We build a model of each player's good and bad match ups and then constantly update things as the dataset grows.

## DIY

If you'd like to have a look a the data with the Elo scores check out any of the `*_results_elo.json` files. These files contain all of the original data along with the individual Elo scores for each of the players. The data in `wtc_data` is the original (after a bunch of cleaning and corrections -- `mkPlayers.py`) data and really shouldn't be modified. This is just so I don't have to fix things if I really break something.

The data in `model_data` contains all (really most) of information about the point costs for individual models. This isn't used for the forecasting, but will be used after the tournament ends when we try to answer questions like the one above.

The ranking model is given in `elo.py` and can be fiddled as much or as little as you like. In the coming days, I'll try to get a better model up and running to see if I can actually get some decent forecasts before the tournament starts.

## Contribute

Pull requests are welcome.

## License

All of the original code is licensed under the MIT license. See the attached `LICENSE.md` file. Anything that isn't original code is probably owned by Privateer Press.
