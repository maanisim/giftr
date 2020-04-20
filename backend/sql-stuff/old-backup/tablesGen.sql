/* Tables generated in certain app may need some modifications */
CREATE TABLE [users] (
[id] INT AUTOINCREMENT NOT NULL UNIQUE,
[username] VARCHAR (40) NOT NULL,
[password] VARCHAR (40) NOT NULL,
[email] VARCHAR (256) NOT NULL,
[name] INT (40),
[age] INT (3),
[gender] INT (10),
[photo] BLOB,
[friends] INT,
PRIMARY KEY ([id],[username]));

CREATE TABLE [wishlist] (
[id] INT (100) PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
[username] INT NOT NULL,
[name] VARCHAR (40),
[suggestion tags] XML NOT NULL,
[gifts] XML NOT NULL,
[privacy] INT NOT NULL,
FOREIGN KEY([username])REFERENCES[users](username));

CREATE TABLE [tag] (
[age] INT (3),
[gender] VARCHAR (10),
[price] VARCHAR (50),
[type] XML,
[id] INT (100) PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE);

CREATE TABLE [gift] (
[id] INT (100) PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
[name] VARCHAR (3000) NOT NULL,
[photo] VARCHAR (3000) NOT NULL,
[age] VARCHAR (15),
[price] INT (50) NOT NULL,
[link] TEXT NOT NULL,
[gender] INT (10),
[category] VARCHAR (30));

CREATE TABLE [gift profiles] (
[id] INT (100) PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
[name] VARCHAR (40),
[suggestion tags] XML,
[gifts] XML NOT NULL,
[username] INT NOT NULL,
FOREIGN KEY([id])REFERENCES[gift](id),
FOREIGN KEY([suggestion tags])REFERENCES[tag](id),
FOREIGN KEY([username])REFERENCES[users](username));
