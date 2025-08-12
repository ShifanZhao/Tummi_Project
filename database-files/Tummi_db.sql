drop database if exists Tummi_db;
create database Tummi_db;
use Tummi_db;




drop table if exists Users;
create table Users
(
   UserId    int,
   FirstName Varchar(20),
   LastName  Varchar(20),
   Username  Varchar(50),
   primary key (UserId)
);




# GREEN
drop table if exists Restaurant;
create table Restaurant
(
   RestId     int primary key,
   RestName   Varchar(20),
   Location   Varchar(20),
   Cuisine    Varchar(20),
   Rating     Decimal(2, 1),
   `Add`      Boolean,
   Flag       Boolean,
   UserId     int,
   NumSaves   int,
   NumVisits  int
);




drop table if exists RestaurantOwner;
create table RestaurantOwner
(
   OwnerId    int primary key,
   OwnerFName Varchar(20),
   OwnerLName Varchar(20),
   Verify     Boolean,
   Flagged    Boolean,
   RestId     int,
   foreign key (RestId) references Restaurant (RestId),
   foreign key (OwnerId) references Users (UserId)
       ON DELETE CASCADE
);




drop table if exists AdCampaign;
create table AdCampaign
(
   CampaignId int primary key,
   AdCost     int,
   StartDate  Date,
   Profit     int,
   Revenue    int,
   OwnerId    int,
   foreign key (OwnerId) references RestaurantOwner (OwnerId)
       ON DELETE CASCADE
);




drop table if exists MenuItem;
create table MenuItem
(
   RestId   int,
   DishId   int,
   DishName Varchar(20),
   Photo    Blob,
   Price    Decimal(5, 2),
   primary key (DishId),
   foreign key (RestId) references Restaurant (RestId)
       ON DELETE CASCADE
);






# ORANGE
drop table if exists AppAnalytics;
create table AppAnalytics
(
   AppAnalyticsId int,
   SessLength     Time,
   LastVisit      DateTime,
   SaveCount      int,
   UserId         int,
   AnalystId      int,
   primary key (AppAnalyticsId)
);




drop table if exists UserActivity;
create table UserActivity
(
   UserActivityId int,
   Pending        DateTime,
   primary key (UserActivityId)
);




drop table if exists InteralAnalyst;
create table InternalAnalyst
(
   AnalystId int,
   FirstName Varchar(20),
   LastName  Varchar(20),
   primary key (AnalystId)
);




drop table if exists InteralApp;
create table InternalApp
(
   AnalystId      int,
   AppAnalyticsId int,
   primary key (AnalystId, AppAnalyticsId),
   foreign key (AnalystId) references InternalAnalyst (AnalystId)
       ON DELETE CASCADE,
   foreign key (AppAnalyticsId) references AppAnalytics (AppAnalyticsId)
       ON DELETE CASCADE
);




drop table if exists Reviews;
create table Reviews
(
   AnalystId      int,
   UserActivityId int,
   ReviewDate     Date,
   primary key (AnalystId, UserActivityId),
   foreign key (AnalystId) references InternalAnalyst (AnalystId)
       ON DELETE CASCADE,
   foreign key (UserActivityId) references UserActivity (UserActivityId)
       ON DELETE CASCADE
);




# PINK
drop table if exists Influencer;
create table Influencer
(
   InfId          int,
   Location       Varchar(50),
   Username       Varchar(50),
   FirstName      Varchar(20),
   LastName       Varchar(20),
   Verified       Boolean,
   LastUse        DateTime,
   Flagged        Boolean,
   RestaurantList int,
   primary key (InfId),
   foreign key (InfId) references Users (UserId)
       ON DELETE CASCADE
);




drop table if exists InfPost;
create table InfPost
(
   PostId    int,
   Likes     int,
   Bookmark  int,
   Share     int,
   Sponsored Boolean,
   InfId     int,
   RestId    int,
   primary key (PostId),
   foreign key (InfId) references Influencer (InfId)
       ON DELETE CASCADE,
   foreign key (RestId) references Restaurant (RestId)
);






drop table if exists RestaurantLists;
create table RestaurantLists
(
   RestListID   int,
   RestListName varchar(20),
   InfId        int,
   primary key (RestListID),
   foreign key (InfId) references Influencer (InfId)
       ON DELETE CASCADE
);




# BLUE / GREY




drop table if exists CasualDiner;
create table CasualDiner
(
   CDId        int,
   Location    Varchar(20),
   Flagged     Boolean,
   SessLength  Time,
   LastVisited DateTime,
   SaveCount   int,
   primary key (CDId),
   foreign key (CdId) references Users (UserId)
       ON DELETE CASCADE
);




drop table if exists Following;
create table Following
(
   FollowerId int,
   FolloweeId int,
   primary key (FollowerId, FolloweeId),
   foreign key (FollowerId) references CasualDiner (CDId)
   ON DELETE CASCADE,
       foreign key (FolloweeId) references CasualDiner (CDId)
       ON DELETE CASCADE
);




drop table if exists BeenTo;
create table BeenTo
(
   CDId       int,
   Restaurant Varchar(20),
   primary key (CDId, Restaurant),
   foreign key (CDId) references CasualDiner (CDId)
       ON DELETE CASCADE
);




drop table if exists WantToTry;
create table WantToTry
(
   CDId       int,
   Restaurant Varchar(20),
   primary key (CDId, Restaurant),
   foreign key (CDId) references CasualDiner (CDId)
       ON DELETE CASCADE
);




drop table if exists CDPost;
create table CDPost
(
   PostId   int,
   Likes    int,
   Rating   Decimal(2, 1),
   CDId     int,
   RestId   int,
   Bookmark int,
   Share    int,
   primary key (PostId),
   foreign key (CDId) references CasualDiner (CDId));






drop table if exists `Photo(s)`;
create table `Photo(s)`
(
   PhotoId   int,
   Photo     Blob,
   CDPostId  int,
   InfPostId int,
   primary key (PhotoId),
   foreign key (CDPostId) references CDPost (PostId)
       ON DELETE CASCADE,
   foreign key (InfPostId) references Influencer (InfId)
       ON DELETE CASCADE
);




drop table if exists Comment;
create table Comment
(
   CommentId int,
   Comment   Text,
   CDPostId  int,
   InfPostId int,
   primary key (CommentId),
   foreign key (CDPostId) references CDPost (PostId)
       ON DELETE CASCADE,
   foreign key (InfPostId) references InfPost (PostId)
       ON DELETE CASCADE
);




drop table if exists Follow;
create table Follow
(
   CDId  int,
   InfId int,
   primary key (CDId, InfId),
   foreign key (CDId) references CasualDiner (CDId)
   ON DELETE CASCADE,
       foreign key (InfId) references Influencer (InfId)
       ON DELETE CASCADE
);




drop table if exists FromInf;
create table FromInf
(
   UserActivityId int,
   InfId          int,
   primary key (UserActivityId, InfId),
   foreign key (UserActivityId) references UserActivity (UserActivityId),
   foreign key (InfId) references Influencer (InfId)
);




drop table if exists FromRestOwner;
create table FromRestOwner
(
   UserActivityId int,
   OwnerId        int,
   primary key (UserActivityId, OwnerId),
   foreign key (UserActivityId) references UserActivity (UserActivityId),
   foreign key (OwnerId) references RestaurantOwner (OwnerId)
);




drop table if exists FromRest;
create table FromRest
(
   UserActivityId int,
   RestId         int,
   primary key (UserActivityId, RestId),
   foreign key (UserActivityId) references UserActivity (UserActivityId),
   foreign key (RestId) references Restaurant (RestId)
);




drop table if exists FromCD;
create table FromCD
(
   UserActivityId int,
   CDId           int,
   primary key (UserActivityId, CDId),
   foreign key (UserActivityId) references UserActivity (UserActivityId),
   foreign key (CDId) references CasualDiner (CDId)
);




drop table if exists ListedRest;
create table ListedRest
(
   RestListId int,
   RestId     int,
   primary key (RestListId, RestId),
   foreign key (RestListId) references RestaurantLists (RestListId),
   foreign key (RestId) references Restaurant (RestId)
);




drop table if exists Sponsorships;
create table Sponsorships
(
   InflId  int,
   RestId  int,
   Pricing int,
   primary key (InflId, RestId),
   foreign key (InflId) references Influencer (InfId)
       ON DELETE CASCADE,
   foreign key (RestId) references Restaurant (RestId)
       ON DELETE CASCADE
);

INSERT INTO Users
VALUES (1, 'Spencer', 'Grant', 'SpencerTheGuy'),
      (2, 'Tiffany', 'Nguyen', 'FoodManiac'),
      (3, 'Shifan', 'Zhao', 'ShifanZhao'),
      (4, 'Evelyn', 'Fabel', 'TheBestAnalyst'),
      (5, 'Billy', 'Bob', 'BobbyEater'),
      (6, 'Rest', 'Hoffman', 'BigChef'),
      (7, 'John', 'Doe', '2ndAnalyst'),
      (8, 'Lil', 'God', 'lilgod');


INSERT INTO Restaurant
VALUES (1, 'Table Mercato', 'North End', 'Italian',
       8.7, TRUE, FALSE, 3, 100, 5000),
      (2, 'El Jefe''s', 'North End', 'Mexican', 7.2,
       TRUE, FALSE, 6, 50, 182);


INSERT INTO RestaurantOwner
VALUES (3, 'Shifan', 'Zhao', TRUE, FALSE, 1),
      (6, 'Rest', 'Hoffman', TRUE, FALSE, 2);


INSERT INTO AdCampaign
VALUES (1, 1234, '2025-10-26', 123, 1357, 3),
      (2, 200, '2024-10-15', 500, 700, 6);


INSERT INTO MenuItem
VALUES (1, 1, 'Vodka Parm Sandwich', 'https://example.com/images/pic1.jpg', 20.99),
      (2, 2, 'Burrito', 'https://example.com/images/pic2.jpg', 8.99);


INSERT INTO AppAnalytics
VALUES (1, 500, NOW(), 4, 1, 4),
      (2, 400, NOW(), 3, 5, 4);


INSERT INTO UserActivity
VALUES (1, NOW()),
      (2, '2024-10-5 10:12:50.000');


INSERT INTO InternalAnalyst
VALUES (4, 'Evelyn', 'Fabel'),
      (7, 'John', 'Doe');


INSERT INTO InternalApp
VALUES (4, 1),
      (7, 2);


INSERT INTO Reviews
VALUES (4, 1, '2024-10-5'),
      (7, 2, '2025-1-2');


INSERT INTO Influencer
VALUES (2, 'LA', 'FoodManiac', 'Tiffany', 'Nguyen', TRUE,
       '2025-8-5 7:51:00.000', FALSE, 1),
      (8, 'New York City', 'lilgod', 'Lil', 'God', TRUE,
       '2025-6-10 8:51:00.000', FALSE, 2);


INSERT INTO RestaurantLists
VALUES (1, 'Mexican Spots', 2),
      (2, 'Scrumptious Italian', 8);


INSERT INTO InfPost
VALUES (1, 50, 3, 2, FALSE, 8, 1),
      (2, 100, 5, 4, FALSE, 2, 2);


INSERT INTO CasualDiner
VALUES (1, 'Roxbury', FALSE, 120, NOW(), 3),
      (5, 'Roxbury', FALSE, 500, NOW(), 5);


INSERT INTO Following
VALUES (1, 5),
      (5, 1);


INSERT INTO BeenTo
VALUES (1, 'Table Mercato'),
      (5, 'El Jefe''s');


INSERT INTO WantToTry
VALUES (1, 'El Jefe''s'),
      (5, 'Table Mercato');


INSERT INTO CDPost
VALUES (1, 500, 6.7, 1, 1, 5, 10),
      (2, 90, 8.9, 5, 2, 14, 20);


INSERT INTO `Photo(s)`
VALUES (1, 'https://example.com/images/pic1.jpg', 1, NULL),
      (2, 'https://example.com/images/pic2.jpg', 2, NULL);


INSERT INTO Comment
VALUES (1, 'That looks soooo gooood', 1, NULL),
      (2, 'Tasty', NULL, 1);


INSERT INTO Follow
VALUES (1, 2),
      (5, 8);


INSERT INTO FromInf
VALUES (1, 2),
      (2, 8);


INSERT INTO FromRestOwner
VALUES (1, 3),
      (2, 6);


INSERT INTO FromRest
VALUES (1, 1),
      (2, 2);


INSERT INTO FromCD
VALUES (1, 1),
      (2, 5);


INSERT INTO ListedRest
VALUES (1, 1),
      (1, 2);


INSERT INTO Sponsorships
VALUES (2, 1, 500),
      (8, 2, 750);


# User sample database
insert into User (UserId, FirstName, LastName, Username) values (9, 'Rourke', 'Cypler', 'rcypler8');
insert into User (UserId, FirstName, LastName, Username) values (10, 'Lula', 'Klausewitz', 'lklausewitz9');
insert into User (UserId, FirstName, LastName, Username) values (11, 'Brenn', 'De Freyne', 'bdefreynea');
insert into User (UserId, FirstName, LastName, Username) values (12, 'Joli', 'Fergie', 'jfergieb');
insert into User (UserId, FirstName, LastName, Username) values (13, 'Tamas', 'Dominelli', 'tdominellic');
insert into User (UserId, FirstName, LastName, Username) values (14, 'Barron', 'Breukelman', 'bbreukelmand');
insert into User (UserId, FirstName, LastName, Username) values (15, 'Sibilla', 'Leyton', 'sleytone');
insert into User (UserId, FirstName, LastName, Username) values (16, 'Dianemarie', 'Zettler', 'dzettlerf');
insert into User (UserId, FirstName, LastName, Username) values (17, 'Rufus', 'Tod', 'rtodg');
insert into User (UserId, FirstName, LastName, Username) values (18, 'Ernestine', 'Stoney', 'estoneyh');
insert into User (UserId, FirstName, LastName, Username) values (19, 'Hanson', 'Dibble', 'hdibblei');
insert into User (UserId, FirstName, LastName, Username) values (20, 'Bone', 'Grenkov', 'bgrenkovj');
insert into User (UserId, FirstName, LastName, Username) values (21, 'Rafa', 'Hirsch', 'rhirschk');
insert into User (UserId, FirstName, LastName, Username) values (22, 'Rubina', 'Farnon', 'rfarnonl');
insert into User (UserId, FirstName, LastName, Username) values (23, 'Pepita', 'Rodgman', 'prodgmanm');
insert into User (UserId, FirstName, LastName, Username) values (24, 'Gretchen', 'Giacomo', 'ggiacomon');
insert into User (UserId, FirstName, LastName, Username) values (25, 'Haslett', 'Gaule', 'hgauleo');
insert into User (UserId, FirstName, LastName, Username) values (26, 'Marielle', 'Hoffner', 'mhoffnerp');
insert into User (UserId, FirstName, LastName, Username) values (27, 'Fannie', 'Jozwik', 'fjozwikq');
insert into User (UserId, FirstName, LastName, Username) values (28, 'Ches', 'Devenish', 'cdevenishr');
insert into User (UserId, FirstName, LastName, Username) values (29, 'Tore', 'Wimlet', 'twimlets');
insert into User (UserId, FirstName, LastName, Username) values (30, 'Dodie', 'Rainsbury', 'drainsburyt');
insert into User (UserId, FirstName, LastName, Username) values (31, 'Diann', 'Gavaran', 'dgavaranu');
insert into User (UserId, FirstName, LastName, Username) values (32, 'Urson', 'Nutbean', 'unutbeanv');
insert into User (UserId, FirstName, LastName, Username) values (33, 'Delcina', 'Ferguson', 'dfergusonw');
insert into User (UserId, FirstName, LastName, Username) values (34, 'Shaina', 'Don', 'sdonx');
insert into User (UserId, FirstName, LastName, Username) values (35, 'Gray', 'Kinnerk', 'gkinnerky');
insert into User (UserId, FirstName, LastName, Username) values (36, 'Woody', 'Blackden', 'wblackdenz');
insert into User (UserId, FirstName, LastName, Username) values (37, 'Gayel', 'McGinnell', 'gmcginnell10');
insert into User (UserId, FirstName, LastName, Username) values (38, 'Emlen', 'Dahlman', 'edahlman11');
insert into User (UserId, FirstName, LastName, Username) values (39, 'Roselle', 'McElhargy', 'rmcelhargy12');
insert into User (UserId, FirstName, LastName, Username) values (40, 'Vikky', 'Kendal', 'vkendal13');