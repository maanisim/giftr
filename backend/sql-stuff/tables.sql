-- http://sqlfiddle.com/#!9/1cab1b1
CREATE TABLE `products` (
	`product_id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(3000) NOT NULL,
	`photo` VARCHAR(3000) NOT NULL,
	`age_low` INT(3) NOT NULL,
  `age_high` INT(3) NOT NULL,
	`price` VARCHAR(4) NOT NULL,
	`link` TEXT NOT NULL,
	`gender` VARCHAR(7) NOT NULL,
	`category` VARCHAR(80) NOT NULL,
	UNIQUE KEY `is_gift_id_unique` (`product_id`) USING BTREE,
	PRIMARY KEY (`product_id`)
) DEFAULT CHARSET=latin1;

CREATE TABLE `users` (
  `user_id` INT(10) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(40) NOT NULL,
  `password` VARCHAR(256) NOT NULL,
  `email` VARCHAR(256) NOT NULL,
  `name` VARCHAR(40) NOT NULL,
  `dob` DATE NOT NULL,
  `gender` VARCHAR(6) NOT NULL,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE `product_liked` (
  `product_liked_id` INT(10) NOT NULL AUTO_INCREMENT,
  `product_id` INT(10),   
  `user_id` INT(10),   
	 PRIMARY KEY (`product_liked_id`),
   FOREIGN KEY(product_id) REFERENCES products(product_id),
   FOREIGN KEY(user_id) REFERENCES users(user_id)
) DEFAULT CHARSET=latin1;



CREATE TABLE `friends_list` (
  `friends_id` INT(10) NOT NULL AUTO_INCREMENT,
  `user_id_1` INT(10),   
  `user_id_2` INT(10),   
   PRIMARY KEY (friends_id),
   FOREIGN KEY(user_id_1) REFERENCES users(user_id),
   FOREIGN KEY(user_id_2) REFERENCES users(user_id)
);

CREATE TABLE `wishlist` (
  `wishlist_id` INT(10) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(40) NOT NULL,
  `user_id` INT(10),
  `for_friend_id` INT(10),  
   /*`suggestion_tags` INT(10) NOT NULL,*/
   /* 1 = private, 0 = public */
  `privacy` INT NOT NULL,
   PRIMARY KEY (wishlist_id),
   FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE `wishlist_list` (
  `wishlist_list_id` INT(10) NOT NULL AUTO_INCREMENT,
  `user_id` INT(10),   
  `product_id` INT(10),   
   PRIMARY KEY (wishlist_list_id),
   FOREIGN KEY(user_id) REFERENCES users(user_id),
   FOREIGN KEY(product_id) REFERENCES products(product_id)
);

CREATE TABLE `products_categories` (
  `category_name` VARCHAR(40),
  `product_id` INT(10),
   PRIMARY KEY (category_name),
   FOREIGN KEY(product_id) REFERENCES products(product_id)
);


/* #ask rufus for how he wants it structured */
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

CREATE TABLE productRecValues (
	'product_id' INT(10) NOT NULL,
         'age_low' INT(3) NOT NULL,
         'age_high' INT(3) NOT NULL, 
         'price' INT(3) NOT NULL,
         'gender1' INT(3) NOT NULL,
         'gender2' INT(3) NOT NULL,
         'toiletries' INT(3) NOT NULL,
         'clothes' INT(3) NOT NULL,
         'homeware' INT(3) NOT NULL,
         'entertainment' INT(3) NOT NULL,
         'consumable' INT(3) NOT NULL,
         'sport' INT(3) NOT NULL,
         'other' INT(3) NOT NULL,
         PRIMARY KEY(product_id),
         FOREIGN KEY(product_id) REFERENCES products(product_id)
 );
 
 CREATE TABLE profileRecValues (
 	'user_id' INT(10) NOT NULL,
	'age_low' INT(3) NOT NULL,
        'age_high' INT(3) NOT NULL,
        'price' INT(3) NOT NULL,
        'gender1' INT(3) NOT NULL,
        'gender2' INT(3) NOT NULL,
        'toiletries' INT(3) NOT NULL,
        'clothes' INT(3) NOT NULL,
        'homeware' INT(3) NOT NULL,
        'entertainment' INT(3) NOT NULL,
        'consumable' INT(3) NOT NULL,
        'sport' INT(3) NOT NULL,
        'other' INT(3) NOT NULL,
        PRIMARY KEY(user_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
);
 
 
