# Myaer - Hypixel Stats Bot
[![widget](https://inv.wtf/widget/myerfire)](https://myer.wtf/discord)

[Bot Invite Link](https//myer.wtf/bot)

Maintained by [Myer (also known as myerfire, MyerFire)](https://github.com/myerfire)
- [YouTube](https://myer.wtf/youtube)
- [Twitter](https://myer.wtf/twitter)
- `myer#0001` on Discord
## Commands
[x/y/z] means replacing [x/y/z] with x, y, or z would result in a valid command name
- /help - ur mom
- /avatar - Shows your Discord avatar
    - aka: /av
- /prefix - Shows current server prefix if there is a custom prefix set
  - `myaer `, `Myaer `, and @ing the bot will always work as prefixes. Default prefix is `/`
- /prefix set `prefix` - Sets server custom prefix
- /prefix reset - Resets server prefix if a custom prefix was set
- /starboard - Shows current server starboard if there is one
  - A starboard is like pinned messages but all in one place
- /starboard set `channel` - Sets server starboard
- /starboard reset - Resets server starboard if there was one
- /[staff/mod/admin]only - Shows settings for who can run commands in certain channels if they were set
  - Staff is defined as having manage messages
  - Mod is defined as having manage server
  - Admin is defined as having administrator
- /[staff/mod/admin]only set `channels` - Sets settings for who can run commands in certain channels
- /[staff/mod/admin]only reset - Resets settings for who can run commands in certain channels
### Minecraft
- /mc verify `ign` - Saves your Minecraft profile for use with future commands. If you are verified, any commands other than this one that require ign as an input will no longer require ign
- /mc unverify - Removes your Minecraft profile from the database
#### Hypixel
- /hypixel `ign` - Shows Hypixel stats
- /bw `ign` - Shows Bedwars stats with a menu for FKDR, BBLR, WLR, and all four main Bedwars modes
- /sw `ign` - Shows Skywars stats with a menu for WLR
- /duels `ign` - Shows Duels stats with a menu for KDR
- /lb - Shows leaderboards with a game menu to select game
  - This is a very expensive command and will probably take a minute or so to complete, and results are cached for an hour
  
### Last.FM
- /fm set `username` - Sets your Last.FM username, similar to `/mc set ign`
- /fm recent `username` - Shows recent tracks
- /fm np `username` - Shows currently playing track
- /fm servernp `username` - Shows server's currently playing track
- /fm wk `artist` - Shows who knows an artist and their plays of the artist in the server
- /fm chart `username` `per` - (if a number is passed in as the only argument you must be verified) - Shows a weekly chart of albums
- /fm chart artist `username` `per` - same as above but for artists