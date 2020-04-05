
-- http://sqlfiddle.com/#!9/78fc97
CREATE TABLE `products` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(3000) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
	`photo` VARCHAR(3000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
	`age_low` INT(3) NOT NULL,
  	`age_high` INT(3) NOT NULL,
	`price` VARCHAR(4) NOT NULL,
	`link` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
	`gender` VARCHAR(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
	`category` VARCHAR(80) NOT NULL,
	UNIQUE KEY `is_gift_id_unique` (`id`) USING BTREE,
	PRIMARY KEY (`id`)
);

CREATE TABLE `users` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `password` VARCHAR(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `email` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `name` INT(40),
  `age` INT(3),
  `gender` INT(6),
  /*'photo` BLOB,
  `friends` INT,*/
  PRIMARY KEY (`id`,`username`)
);

CREATE TABLE `wishlist` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `username` INT NOT NULL,
  `name` VARCHAR(40),
  /*`suggestion_tags` INT(10) NOT NULL,*/
  `wishlist_gift_id` INT(10) NOT NULL,
  `privacy` INT NOT NULL,
  PRIMARY KEY (id)
  /*FOREIGN KEY(username) REFERENCES users(username)*/
);

CREATE TABLE `tag` (
  `age` INT(3),
  `gender` VARCHAR(6),
  `price` VARCHAR(4),
  /*`type` XML,*/
  `id` INT(100) PRIMARY KEY AUTO_INCREMENT NOT NULL
);

CREATE TABLE `gift_profiles` (
  `id` INT(100) AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(40),
  /*
  `suggestion tags` XML,
  `gifts` XML NOT NULL,
  */
  `username` INT NOT NULL,
  PRIMARY KEY (id)
  /*
  FOREIGN KEY(`id`)REFERENCES`gift`(id),
  FOREIGN KEY(`suggestion tags`)REFERENCES`tag`(id),
  FOREIGN KEY(`username`)REFERENCES`users`(username)
  */
);