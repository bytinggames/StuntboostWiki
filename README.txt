# STUNTBOOST Wiki

$discord = [Discord](https://discord.gg/stuntboost)

Links
    Follow us
        - [Steam - STUNTBOOST](https://store.steampowered.com/app/2999500/STUNTBOOST/)
        - [Steam - Byting Games](https://store.steampowered.com/developer/bytinggames)
        - [YouTube](https://www.youtube.com/@bytinggames9902)
        - [Bluesky](https://bsky.app/profile/bytinggames.com)
    - $discord
	- [Leaderboard Website](https://sblb.thefanclub.cc/)
    - [Presskit](https://bytinggames.com/press/sheet.php?p=stuntboost)
    - [Custom Mapping Tools](https://github.com/bytinggames/StuntboostTools)
    - [speedrun.com](https://www.speedrun.com/stuntboost)
    - [Homepage](https://bytinggames.com)
    - [WRs on YouTube](https://www.youtube.com/@STUNTBOOSTWorldRecords)
    - [Tobi's Music](https://tobiaskozel.bandcamp.com/album/stuntboost-ost)

FAQ
    Where to report a bug?
        Either on $discord or on the [Steam Forum](https://steamcommunity.com/app/2999500/discussions/)
    Where can I follow you?
        See [[Links/Follow us]]
    Where can I chat with other players?
        - Our $discord
    When did it release?
        2026, September 22th
    Is there a level editor?
        No, but you can [design levels with our tools](https://github.com/bytinggames/StuntboostTools)
    Is there multiplayer or co-op? Or is it planned?
        No, there's only online leaderboards. A multiplayer mode is more likely to appear in future projects.
    Is there a demo?
        No
    Does it support controller / keyboard?
        It's strongly recommended to play with mouse and keyboard, but you can play with any controller too.
    How long is the campaign?
        Simply getting through the game will take you around 3 hours. But the game is made with high replayability in mind. Finding shortcuts, earning medals, getting collectibles, bonus levels, speedrun challenges and community maps.
    How much RNG is in the game?
        None
    Can I remap controls?
        Yes
    Does it support 4K / Ultrawide monitors?
        Yes
    Does it run on the Steam Deck or Steam Machine?
        Yes: https://steamcommunity.com/games/2999500/announcements/detail/677384059121303747
    Does it run at 60 FPS and beyond?
        Yes, no artificial frame cap
    Does it run on a potato?
        It runs on pretty low-end PCs and most laptops. See minimum specs on the Steam-Page.
    Does it run on Linux?
        Yes, natively.
    Any plans to support Mac?
        Not planned currently.
    Is there modding support?
        Not officially, but some players got some things going on our $discord
    Are there achievements?
        Yes, over 60
    What engine did you build it in?
        Self made engine on top of MonoGame.
    What were your inspirations?
        Zineth, N (flash game), Trackmania, Celeste and Jet Set Radio.
    Who are you?
        After having published my free game Find You I teamed up with Tobi - a friend I met during college - to work on our first commercial game. We graduated and later quit our jobs to work full time on STUNTBOOST. I like to work in small teams, so it's only us two. We had a lot of additional help though. F.ex. SBVille helped in designing a few levels. Check out the credits to see who else was part of it.
    Why are there so many shortcuts?
        A big part of improving your runs is not only by physically playing better but also by figuring out shortcuts. Discovering shortcuts is part of the experience.
    What's next?
        Not sure yet. But for now, the two of us will take a break soon. And we'll probably focus on new projects afterwards. That could mean working on something that builds upon STUNTBOOST or it could also mean something completely new.
    How to get the lights back on?
        Hit Escape > Options

Ingame - Physics
    Abilities
        Steer
            You can take very tight turns. If you drag your mouse faster than your board can turn, then your board will follow up pretty quickly. No matter how hard you steer, you won't loose speed
        Crouch
            - Increases gravity in air and on ground.
            - It also increases your grip. The grip is strongest when you begin to hold the crouch key or when you land on an edge (also works without crouching).
            - Crouching makes the player smaller too.
            - If you fly upwards, crouching cancels your ascension.
            - When you begin to crouch mid-air you'll get a tiny downward boost.
        Jump
            - It doesn't matter how long you hold the jump key. You can do a shorter jump by interrupting it with the crouch key (shift).
            - Jumping makes your collision shape smaller by pulling your "legs" up. When ground is in reach your "legs" / collision capsule will extend again
        Land
            - You conserve the most speed if the platform you land on matches the angle of your velocity. This is less relevant when landing on ramps. Landing on ramps always gives you more speed.
            - Landing somewhere higher then where you jumped off slightly slows you down. Sometimes it might be worth to ride up an uphill instead of jumping over it
            - Landing sideways or backwards initiates a drift which slows you down
        Kickflip
            - This gets taught in lvl B3.
            - Jump before a ramp and then jump again when touching it mid-air. This will initiate a Kickflip which gives you twice the jump height. It works on horizontal and vertical ramps (quarterpipes).
            - The jump key timing is pretty generous and it doesn't matter if you hit the jump key slightly before or after collision
        Grind
            - Grinding doesn't give you speed, unless you're grinding on an orange/yellow rail. Then you'll accelerate constantly.
            - Grinding downhill or uphill will affect your velocity the same as when riding on the ground normally.
            - You can crouch while grinding.
            - You can exit a grind either by letting go of the grind key or by hitting the space key. Both result in the same.
            - When you exit a grind you perform a short dash that disables gravity for a short time, or until you collide with something. So instead of giving you upward momentum like with a normal jump, you simply have a few ticks where gravity is ignored.
            - You dash into the direction your camera points
            - You can tilt your board left and right by looking around, but that won't affect your speed and also not the distance you travel. But it'll move your collision shape a bit, so you can evade obstacles.
        Spring Jump / Heelflip
            - This is a kickflip that gives you even more height
            - Perform it like this: Fall a good amount -> hit "jump" before touching a downwards tilted surface -> launch yourself against a ramp -> do a kickflip
            - Practice it in lvl A7 on the second ramp or A13 in the halfpipe
            - When spring jumping, all your initial falling velocity gets re-applied when you do the final kickflip. The higher your faling velocity was, the stronger your Spring Jump will be
    Vehicles
        Each level has a set vehicle.
        Skateboard
            The default. You can only grind in levels starting from level B3. Exception: You can't grind in level E10.
        Longboard
            Like the skateboard, but can't jump.
        Scooter
            - Has 10cm/s base speed instead of 5.
            - Can time travel with R/T.
            - Only occurs in freeroam levels.
        Car
            - Cars drift constantly.
            - Oversteering is recommended.
            - The speed you loose when drifting backwards gets charged and re-applied.
        Time Travel Car
            - Has 10cm/s base speed instead of 5.
            - Is a mix of the Scooter and the Car.
    Objects
        Ramps
            - Most things that point upward and end with a sharp edge are considered ramps.
            - Landing on ramps conserves most speed than landing on normal ground.
            - Ramps can be used to initiate a Kickflip.
            Vertical Ramps
                - Also called Verts or Quarterpipes
                - They end in a completely vertical surface, launching the player straight up
                - Steering behaves slightly different on them to get the player to jump where they actually want
                - The first jump for a "Spring Jump" also behaves differently. See "Spring Jump".
                - You cannot kickflip away from a vertical ramp
            Horizontal Ramps
                - Every ramp that is not a Vertical Ramp
                - You cannot kickflip into the direction you were coming from
        Checkpoints
            Types
                - Green: mandatory or goal
                - Orange: optional
                - yellow: lap checkpoint
                - red: lap goal
            Order
                Sometimes checkpoints can only be collected in a certain order. In the game they're placed in a straightforward way. In custom levels you may have to figure out the order by yourself. A checkpoint is greyed out if you can't collect it yet
            Why do checkpoints rewind time?
                So beginners can achieve decent runs. But if they want to compete on the leaderboard they'll have to play without them, as they impose a one second penalty on you.
        Goal
            The phsyics run at 60 ticks per second, so to calculate your exact time of collision with the goal, the game checks how deep you went into the goal on the current tick.
    Ticks
        The physics run at 60 ticks per second. When playing on a higher framerate, the game inter- and extrapolates the physics so you have a smooth experience.

Optional Content
    Medal Times
        Check the individual levels here: https://sblb.thefanclub.cc/
    Cassettes
        Guide: https://steamcommunity.com/sharedfiles/filedetails/?id=3813553890
    Bonus Level
        - Just more levels, that are slightly weirder
        - Unlock them by collecting VHS tapes
        - They also have VHS tapes
    Challenges
        - The 6th room contains different multi-level speedrun challenges
        - The timer works differently here: It doesn't rewind and it penalizes you only when rewinding within 1 second of touching a checkpoint . See Rules: https://www.speedrun.com/stuntboost
        - Daily can only be played once and you can't reset your timer
        - Medals collected here will not count to your total medal number
        - If you want to see your time differenes, use LiveSplit. It's pretty easy to setup, just press the LiveSplit button in the challenge room and it'll give you all the instructions.
    Achievements
        Guide (Spoiler!): https://www.youtube.com/watch?v=L-IrCTK13Sc

Community Content
    Leaderboard
        individual levels: https://sblb.thefanclub.cc/
        overall leaderboard, ranked by your average level placement: https://sblb.thefanclub.cc/overall
    Custom Maps
        To play: either check out our $discord or see https://sblb.thefanclub.cc/?room=custom
        - To create check out our $discord
    Modding
        - Not officially supported, but some players got something going in our $discord
    Guides
        https://steamcommunity.com/app/2999500/guides/
