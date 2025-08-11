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
