CREATE TABLE `tUser` (
  `userID` int PRIMARY KEY AUTO_INCREMENT,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `familyID` int, 
  `password` varchar(255) NOT NULL,
  `image` varchar(255),
  `addressID` int,
  `last_message_read_time` timestamp,
  FULLTEXT KEY (firstName, lastName, email),
  FULLTEXT KEY (firstName, lastName),
  FULLTEXT KEY (email)
);

CREATE TABLE `tAddress` (
  `addressID` int PRIMARY KEY AUTO_INCREMENT,
  `address` varchar(255),
  `city` varchar(255),
  `state` varchar(255),
  `zip` int
);

CREATE TABLE `tDog` (
  `dogID` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `gender` varchar(255),  
  `breedID` int,
  `fixed` varchar(255),
  `age` int NOT NULL,
  `Size` varchar(255) NOT NULL,
  `weight` int,
  `bio` varchar(255),
  `image` varchar(255),
  `favToyID` int,
  `favParkID` int,
  `familyID` int,
  FULLTEXT KEY (name)
);

CREATE TABLE `tBreed` (
  `breedID` int PRIMARY KEY AUTO_INCREMENT,
  `breed` varchar(255) NOT NULL
);

CREATE TABLE `tFamily` (
  `familyID` int PRIMARY KEY AUTO_INCREMENT,
  `familyName` varchar(255),
  `headofHouseID` int,
  FULLTEXT KEY (familyName)
);

CREATE TABLE `tAdmin` (
  `adminID` int PRIMARY KEY AUTO_INCREMENT,
  `dogID` int,
  `userID` int
);

CREATE TABLE `tFavoriteToy` (
  `favToyID` int PRIMARY KEY AUTO_INCREMENT,
  `ToyName` varchar(255) NOT NULL,
  `image` varchar(255)
);

CREATE TABLE `tFavoritePark` (
  `favParkID` int PRIMARY KEY AUTO_INCREMENT,
  `parkName` varchar(255) NOT NULL,
  `AddressID` int,
  `image` varchar(255)
);

CREATE TABLE `tFollowers` (
  `followID` int PRIMARY KEY AUTO_INCREMENT,
  `dogID` int,
  `userID` int
);

CREATE TABLE `tPosts` (
  `postID` int PRIMARY KEY AUTO_INCREMENT,
  `dogID` int,
  `userID` int,
  `groupID` int,
  `Post` varchar(255) NOT NULL,
  `ts` timestamp NOT NULL DEFAULT NOW(),
  `image` varchar(255)
);

CREATE TABLE `tPostPictures` (
  `postPicturesID` int,
  `image` varchar(255),
  `postID` int
);

CREATE TABLE `tComments` (
  `commentID` int PRIMARY KEY AUTO_INCREMENT,
  `postID` int,
  `userID` int,
  `Comment` varchar(255) NOT NULL,
  `ts` timestamp NOT NULL DEFAULT NOW(),
  `image` varchar(255)
);

CREATE TABLE `tReacts` (
  `reactID` int PRIMARY KEY AUTO_INCREMENT,
  `userID` int,
  `postID` int, 
  `ts` timestamp NOT NULL DEFAULT NOW()
);

CREATE TABLE `tAvailability` (
  `availabilityID` int PRIMARY KEY AUTO_INCREMENT,
  `dogID` int,
  `userID` int,
  `Begin_ts` timestamp NULL DEFAULT NULL,
  `End_ts` timestamp NULL DEFAULT NULL
);

CREATE TABLE `tPlayDateTime` (
  `playdateTimeID` int PRIMARY KEY AUTO_INCREMENT,
  `playDateID` int,
  `Begin_ts` timestamp NULL DEFAULT NULL,
  `End_ts` timestamp NULL DEFAULT NULL,
  `AddressID` int
);

CREATE TABLE `tPlayDate` (
  `playDateID` int PRIMARY KEY AUTO_INCREMENT,
  `dogID` int,
  `userID` int
);

CREATE TABLE `tFriend` (
  `friendID` int PRIMARY KEY AUTO_INCREMENT,
  `user` int,
  `friend` int
);

CREATE TABLE `tMessage` (
  `messageID` int PRIMARY KEY AUTO_INCREMENT,
  `friendID` int NOT NULL,
  `sender` int,
  `recipient` int,
  `time_Sent` timestamp NOT NULL DEFAULT NOW(),
  `message` varchar(255)
);

CREATE TABLE `tPictureMessage` (
  `pictureMessageID` int,
  `image` varchar(255),
  `messageID` int
);

CREATE TABLE `tInterests` (
  `interestsID` int PRIMARY KEY AUTO_INCREMENT,
  `Interests` varchar(255) NOT NULL,
  `Disinterests` varchar(255) NOT NULL
);

CREATE TABLE `tDogInterests` (
  `DogInterestsID` int PRIMARY KEY AUTO_INCREMENT,
  `interestsID` int,
  `dogID` int
);

CREATE TABLE `tGroupParticipants` (
  `GroupParticipantsID` int PRIMARY KEY AUTO_INCREMENT,
  `userID` int,
  `groupID` int
);

CREATE TABLE `tGroup` (
  `groupID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `image` varchar(255)
);

CREATE TABLE `tHeadofHouse` (
  `headofHouseID` int PRIMARY KEY AUTO_INCREMENT,
  `userID` int
);
ALTER TABLE `tUser` ADD FOREIGN KEY (`addressID`) REFERENCES `tAddress` (`addressID`);

ALTER TABLE `tUser` ADD FOREIGN KEY (`FamilyID`) REFERENCES `tFamily` (`familyID`);

ALTER TABLE `tDog` ADD FOREIGN KEY (`breedID`) REFERENCES `tBreed` (`breedID`);

ALTER TABLE `tDog` ADD FOREIGN KEY (`favParkID`) REFERENCES `tFavoritePark` (`favParkID`);

ALTER TABLE `tDog` ADD FOREIGN KEY (`favToyID`) REFERENCES `tFavoriteToy` (`favToyID`);

ALTER TABLE `tDog` ADD FOREIGN KEY (`FamilyID`) REFERENCES `tFamily` (`familyID`);

ALTER TABLE `tFamily` ADD FOREIGN KEY (`headofHouseID`) REFERENCES `tHeadofHouse` (`headofHouseID`);

ALTER TABLE `tFavoritePark` ADD FOREIGN KEY (`AddressID`) REFERENCES `tAddress` (`addressID`);

ALTER TABLE `tAdmin` ADD FOREIGN KEY (`dogID`) REFERENCES `tDog` (`dogID`);

ALTER TABLE `tAdmin` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tFollowers` ADD FOREIGN KEY (`dogID`) REFERENCES `tDog` (`dogID`);

ALTER TABLE `tFollowers` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tPosts` ADD FOREIGN KEY (`dogID`) REFERENCES `tDog` (`dogID`);

ALTER TABLE `tPosts` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tPosts` ADD FOREIGN KEY (`groupID`) REFERENCES `tGroup` (`groupID`);

ALTER TABLE `tPostPictures` ADD FOREIGN KEY (`postID`) REFERENCES `tPosts` (`postID`);

ALTER TABLE `tComments` ADD FOREIGN KEY (`postID`) REFERENCES `tPosts` (`postID`);

ALTER TABLE `tComments` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tReacts` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tReacts` ADD FOREIGN KEY (`postID`) REFERENCES `tPosts` (`postID`);

ALTER TABLE `tAvailability` ADD FOREIGN KEY (`dogID`) REFERENCES `tDog` (`dogID`);

ALTER TABLE `tAvailability` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tPlayDateTime` ADD FOREIGN KEY (`playDateID`) REFERENCES `tPlayDate` (`playDateID`);

ALTER TABLE `tPlayDateTime` ADD FOREIGN KEY (`AddressID`) REFERENCES `tAddress` (`addressID`);

ALTER TABLE `tPlayDate` ADD FOREIGN KEY (`dogID`) REFERENCES `tDog` (`dogID`);

ALTER TABLE `tPlayDate` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tFriend` ADD FOREIGN KEY (`user`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tFriend` ADD FOREIGN KEY (`friend`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tMessage` ADD FOREIGN KEY (`friendID`) REFERENCES `tFriend` (`friendID`) ON DELETE CASCADE;

ALTER TABLE `tMessage` ADD FOREIGN KEY (`sender`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tMessage` ADD FOREIGN KEY (`recipient`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tPictureMessage` ADD FOREIGN KEY (`messageID`) REFERENCES `tMessage` (`messageID`);

ALTER TABLE `tDogInterests` ADD FOREIGN KEY (`interestsID`) REFERENCES `tInterests` (`interestsID`);

ALTER TABLE `tDogInterests` ADD FOREIGN KEY (`dogID`) REFERENCES `tDog` (`dogID`);

ALTER TABLE `tGroupParticipants` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);

ALTER TABLE `tGroupParticipants` ADD FOREIGN KEY (`groupID`) REFERENCES `tGroup` (`groupID`);

ALTER TABLE `tHeadofHouse` ADD FOREIGN KEY (`userID`) REFERENCES `tUser` (`userID`);
