
INSERT INTO users (username, password, token, email, name, age, gender, photo)
VALUES ("root", "toor", "0", "root@root.root","root",21,"female","avatar.png"),
("dummy", "dummy", "0", "dummy@dummy.dummy","dummy",21,"male","avatar.png"),
("david", "david", "0", "david@david.david","david",21,"male","avatar.png"),
("gaga", "gaga", "0", "gaga@gaga.gaga","gaga",22,"female","avatar.png"),
 ("z", "z", "0", "z@z.z","z",19,"male","avatar.png");

INSERT INTO users (username, password, token, email, name, age, gender, photo)
VALUES ("z", "z", "0", "z@z.z","z",19,"male","avatar.png");

INSERT INTO friends_list (user_id_1,user_id_2) VALUES (1,2), (3,1);

INSERT INTO wishlist (name,user_id,privacy) VALUES
("Dummy's favourite things",2,1),
("David's favourite things",3,0);

INSERT INTO wishlist_list (user_id,product_id) VALUES
(1,1),
(2,2);

INSERT INTO products (
    name,
    photo,
    age_low,
    age_high,
    price,
    link,
    gender,
    category
)
VALUES
    (
        "FITFORT Alarm Clock Wake Up",
        "1.jpg",
        20,
        99,
        "$",
        "https://www.amazon.co.uk/FITFORT-Alarm-Clock-Wake-Light-Sunrise/dp/B07CQVM7WY/ref=sr_1_6",
        "unisex",
        "Alarm Clocks"
    ),
    (
        "Molecule No 01 Super Pud Mun",
        "1083.jpg",
        18,
        99,
        "$$$",
        "https://www.amazon.co.uk/Molecule-No-01-Super-Pud-Mun/dp/B07NYS8WP2/ref=sr_1_13",
        "female",
        "Perfumes"
    );
