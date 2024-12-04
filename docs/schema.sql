CREATE TABLE `users` (
    `id` int PRIMARY KEY auto_increment,
    `username` varchar(128),
    `email` varchar(255),
    `password` varchar(128),
    `role` enum ('Admin', 'Staff', 'User'),
    UNIQUE (`username`),
    UNIQUE (`email`)
);

CREATE TABLE `notification` (
    `id` int PRIMARY KEY auto_increment,
    `uid` int,
    `title` varchar(255),
    `description` varchar(255)
);

CREATE TABLE `meta_item_categories` (
    `id` int PRIMARY KEY auto_increment,
    `category_name` varchar(255)
);

CREATE TABLE `meta_item_subcategories` (
    `id` int PRIMARY KEY auto_increment,
    `category_id` int,
    `subcategory_name` varchar(255)
);

CREATE TABLE `meta_item_attributes` (
    `id` int PRIMARY KEY auto_increment,
    `attribute_name` varchar(255),
    `subcategory_id` int
);

CREATE TABLE `items` (
    `id` int PRIMARY KEY auto_increment,
    `name` varchar(255),
    `category_id` int,
    `subcategory_id` int
);

CREATE TABLE `item_attributes` (
    `item_id` int,
    `attribute_id` int,
    `attribute_value` varchar(255)
);

CREATE TABLE `auctions` (
    `id` int PRIMARY KEY auto_increment,
    `item_id` int,
    `seller_id` int,
    `initial_price` real,
    `min_increment` real,
    `min_price` real,
    `opening_time` timestamp,
    `closing_time` timestamp,
    `status` enum ('Open', 'Sold', 'Expired')
);

CREATE TABLE `bids` (
    `id` int PRIMARY KEY auto_increment,
    `auction_id` int,
    `users_id` int,
    `bid_value` real,
    `bid_active` bool DEFAULT true
);

CREATE TABLE `user_questions` (
    `id` int PRIMARY KEY auto_increment,
    `auction_id` int,
    `asker_id` int,
    `replier_id` int,
    `question_text` varchar(255),
    `is_open` bool
);

CREATE TABLE `user_answers` (
    `id` int PRIMARY KEY auto_increment,
    `question_id` int,
    `replier_id` int,
    `reply_text` varchar(255)
);

CREATE TABLE `alerts` (
    `id` int PRIMARY KEY auto_increment,
    `item_id` int,
    `user_id` int
);

ALTER TABLE `notification` ADD FOREIGN KEY (`uid`) REFERENCES `users` (`id`);

ALTER TABLE `meta_item_subcategories` ADD FOREIGN KEY (`category_id`) REFERENCES `meta_item_categories` (`id`);

ALTER TABLE `meta_item_attributes` ADD FOREIGN KEY (`subcategory_id`) REFERENCES `meta_item_subcategories` (`id`);

ALTER TABLE `items` ADD FOREIGN KEY (`category_id`) REFERENCES `meta_item_categories` (`id`);

ALTER TABLE `items` ADD FOREIGN KEY (`subcategory_id`) REFERENCES `meta_item_subcategories` (`id`);

ALTER TABLE `item_attributes` ADD FOREIGN KEY (`item_id`) REFERENCES `items` (`id`);

ALTER TABLE `item_attributes` ADD FOREIGN KEY (`attribute_id`) REFERENCES `meta_item_attributes` (`id`);

ALTER TABLE `auctions` ADD FOREIGN KEY (`item_id`) REFERENCES `items` (`id`);

ALTER TABLE `auctions` ADD FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`);

ALTER TABLE `bids` ADD FOREIGN KEY (`auction_id`) REFERENCES `auctions` (`id`);

ALTER TABLE `bids` ADD FOREIGN KEY (`users_id`) REFERENCES `users` (`id`);

ALTER TABLE `user_questions` ADD FOREIGN KEY (`auction_id`) REFERENCES `auctions` (`id`);

ALTER TABLE `user_questions` ADD FOREIGN KEY (`asker_id`) REFERENCES `users` (`id`);

ALTER TABLE `user_answers` ADD FOREIGN KEY (`question_id`) REFERENCES `user_questions` (`id`);

ALTER TABLE `user_answers` ADD FOREIGN KEY (`replier_id`) REFERENCES `users` (`id`);

ALTER TABLE `alerts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `alerts` ADD FOREIGN KEY (`item_id`) REFERENCES `items` (`id`);
