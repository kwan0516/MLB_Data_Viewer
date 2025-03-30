# IA637 Kuan final project - MLB data viewer

## Introduction
This class is teaching how to combine database and front end, plus another big data class is teaching how to collect and arrange the data. Therefore, I decided to make a project that can use the data which I collected. The web page shows the MLB 2024 season game data and the player basic information(players stat not complete yet). 

## User role purpose
    Admin: To manage and update the data in this webpage. Not only the baseball data, but also the users information.
    customer: The basic role of the webpage with limited access. Only can see the information about the favorite team. Let the user love this webpage and make them to upgrade to VIP to get profit.
    VIP: Have the full access of viewing all the data in the webpage. 

## User account test 
There are three kinds of roles in this web page. They are `admin`, `customer`, and `VIP`. `admin` can add, edit the stat and information of the teams and players. `VIP` are able to view all the data in this web page. `customer` are only able to view the information of his/her favorite team. 
    
### Accounts  with different role
|user name |password|  role  |
|---------:|-------:|-------:|
|  kuan    |  5566  | admin  |
|  saber   |  1234  |   VIP  |
|  luna    | aabb   |customer|

## Admin 
In admin main page, admin can edit user and team information through `Manage Users` and `Manage Teams`. If you want to edit or add players in a specific team, click `Manage Teams` and select a team. You can see the player list of the team. 

## VIP
The VIP can view all the things on the website, including the leaderboard, game schedule, and the every game of the 2024 season. 

## Customer
The customer only can view leaderboard and the information relative to their favorite team, including games and players. You can upgrade your account through getVIP.

### Tables 
- ![user](/img/table_user.png) 

The user table includes `uid`, `name`, `password`, `role`, and `favoriteTeam`.

- ![team](/img/table_team.png) 

The team table includes the basic information of the teams.

- ![player](/img/table_player.png) 

The player table includes the basic information and the season stats of the player. 

- ![game](/img/table_game.png) 

The game table includes the game result and the home team and away team information.

- ![linescore](/img/table_linescore.png) 
![pitcherbox](/img/table_pitcherbox.png) 
![batterbox](/img/table_batterbox.png) 

These three tables shows the overview of the game in the scoreboard page.

- ![gamelog](/img/table_gamelog.png) 

The gamelog table includes every detail of a game. 

## SQL query
New function in baseObject `getByMultiField`. The function can set multi conditions to get the result.

Update `getByField` in baseObject. Add a new argument `sort_by` to get return in a order. 

In user, player, and team, all of the three tables have `verify_update` and `verify_new` functions to check if everything correct when a data is added or changed.

In player table, a join query `getPlayerTeams` to select a player with his team. 

In player table, function `getTopfield` can select the top 10 player of a specific field.

An analytical query is written in team table. `getMonthHomeStat` can list out the average score of each team they get each month. 
