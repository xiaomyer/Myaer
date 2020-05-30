# Myaer Discord Bot
Myaer is a Discord bot written with discord.py in Python 3.8.2. It is focused around Minecraft and Hypixel, but other commands can and will be added.
## Information
- Invite the bot to your server with [this link](https://discord.com/api/oauth2/authorize?client_id=700133917264445480&permissions=8&scope=bot)
- Join my public [Discord Server](https://inv.wtf/myerfire) for support
## Command List
### General
- **/help** - What do you think it is?
- **/ping** - Shows bot latency
### Minecraft
#### General
**If you are verified, you can omit the \<name\> part and it will default to you**
- **/mc name \<name\>** - Shows name history
  - verified mode (omitting name) coming soon™
- **/mc uuid \<name\>** - Shows UUID
- **/mc verify \<name\>** - Verifies you with the Myaer Bot database for easier command access
  - this requires that your Discord social media option be set to your Discord name on Hypixel
- **/mc unverify \<name\>** - Unverifies you from the Myaer Bot database
#### Hypixel
##### Bedwars
###### Player Stats
**If you are verified, you can omit the \<player\> part and it will default to you**
- **/bw \<player\>** - Shows general Bedwars stats
  - **/bw \<solos/doubles/threes/fours/4v4\> \<player\>** - Shows per game mode stats
  - **/bw \<armed/castles/luckyblocks/rush/ultimate/voidless> \<player\>** - Shows per dream game mode stats
- **/bw bblr \<player\>** - Shows bed break/loss ratio and other calculations
  - **/bw bblr \<solos/doubles/threes/fours/4v4\> \<player\>** - Shows per game mode bed break/loss ratio and other calculations
- **/bw fkdr \<player\>** - Shows final kill/death ratio and other calculations
  - **/bw fkdr \<solos/doubles/threes/fours/4v4\> \<player\>** - Shows per game mode final kill/death ratio and other calculations
- **/bw wlr \<player\>** - Shows win/loss ratio and other calculations
  - **/bw wlr \<solos/doubles/threes/fours/4v4\> \<player\>** - Shows per game mode win/loss ratio and other calculations

###### Leaderboards
- **/lb bw \<levels/level/star\>** - Shows Bedwars level leaderboard
  - Default Bedwars leaderboard is level leaderboard, therefore **/lb bw** works
- **/lb bw finals** - Shows overall Bedwars final kills leaderboard
- **/lb bw finals weekly** - Shows weekly Bedwars final kills leaderboard
- **/lb bw wins** - Shows overall Bedwars wins leaderboard
- **/lb bw wins weekly** - Shows weekly Bedwars wins leaderboard

##### Skywars
###### Player Stats
**If you are verified, you can omit the \<player\> part and it will default to you**
- **/sw \<player\>** - Shows general Skywars stats
  - per stat calculations coming soon™
##### Wrist Spasm
*These features are specific to Wrist Spasm*
- **/spasm verify \<name\>** - Sets your nickname to your Minecraft IGN and gives you a role based on your Bedwars prestige
  - **/spasm override \<discord_id_or_mention\> \<name\>** - Overrides and reverifies someone (only works if you have staff roles in Wrist Spasm)
## Authors
- **MyerFire** *myer#0001* *https://www.youtube.com/myerfire*
  - Anyone may submit a pull request and it will possibly be implemented
