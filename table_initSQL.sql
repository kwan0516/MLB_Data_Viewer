-- init user table
CREATE TABLE ko_users (
uid INT AUTO_INCREMENT NOT NULL,
`name` VARCHAR(20),
`password` VARCHAR(100),
`role` VARCHAR(20),
`favoriteTeam` VARCHAR(40),
PRIMARY KEY (uid)
) ENGINE=MyISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- init team table
CREATE TABLE ko_team (
teamKey INT AUTO_INCREMENT NOT NULL,
teamid INT,
Name VARCHAR(30),
abbr VARCHAR(5),
Division VARCHAR(30),
Win INT,
Lose INT,
Standing INT,
PRIMARY KEY (teamKey)
) ENGINE=MyISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- init game table
CREATE TABLE ko_game (
    gameKey INT AUTO_INCREMENT,
    gameid INT,
    date Date,
    homeKey INT,
    homeTeam VARCHAR(50),
    homeid INT,
    homeWins INT,
    homeLosses INT,
    awayKey INT,
    awayTeam VARCHAR(50),
    awayid INT,
    awayWins INT,
    awayLosses INT,
    homeScore INT,
    awayScore INT,

    PRIMARY KEY (gameKey)
) ENGINE=MyISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- init linescore table
CREATE TABLE ko_linescore (
    gameid INT,
    titel VARCHAR(3)
    away INT,
    home INT
) ENGINE=MyISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- init batterbox table
CREATE TABLE ko_pitcherbox (
    gameid INT,
    hw VARCHAR(20),
    teamid INT,
    abbreviation VARCHAR(5),
    pitcherName VARCHAR(30),
    pitcherid INT,
    IP DECIMAL(3,1),
    H INT,
    R INT,
    ER  INT,
    BB  INT,
    K  INT,
    HR  INT,
    ERA DECIMAL(5,2),
    note VARCHAR(30)
) ENGINE=MyISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- init batterbox 
CREATE TABLE ko_batterbox (
    gameid INT,
    hw VARCHAR(20),
    teamid INT,
    abbreviation VARCHAR(5),
    batterName VARCHAR(30),
    batterid INT,
    position VARCHAR(10),
    battingOrder VARCHAR(10),
    AB INT,
    H INT,
    R INT,
    RBI INT,
    BB INT,
    K INT,
    AVG DECIMAL(5,3),
    OPS DECIMAL(5,3)
) ENGINE=MyISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- init gamelog table
CREATE TABLE ko_gamelog (
    gameid INT,
    atBatIndex INT,
    `type` VARCHAR(20),
    awayScore INT,
    homeScore INT,
    batterid INT,
    batterName VARCHAR(50),
    pitcherid INT,
    pitcherName VARCHAR(50),
    inning INT,
    halfInning VARCHAR(10),
    runnerIndex INT,
    ball INT,
    strike INT, 
    `out` INT,
    RBI INT,
    `event` VARCHAR(500),
    situation VARCHAR(5),
    situation_after VARCHAR(5)
) ENGINE=MyISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- init players table
CREATE TABLE ko_players (
    playerKey INT AUTO_INCREMENT,
    f_name VARCHAR(20),
    l_name VARCHAR(20), 
    playerID INT,
	team VARCHAR(50),
    number INT,
    height VARCHAR(10),
    weight VARCHAR(10),
    birthday DATE,
    MLB_debut_date DATE,
    position VARCHAR(30),
    BT VARCHAR(10),
    PA INT NOT NULL,
    AB INT NOT NULL,
    H INT NOT NULL,
    BB INT NOT NULL,
    RBI INT NOT NULL,
    `AVG` DECIMAL(4,3) NOT NULL,
    SLG DECIMAL(4,3) NOT NULL,
    OBP DECIMAL(4,3) NOT NULL,
    OPS DECIMAL(4,3) NOT NULL,
    PRIMARY KEY (playerKey)
)