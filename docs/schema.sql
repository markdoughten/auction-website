create database auction;

use auction;

create table users (
    id int auto_increment primary key,
    username varchar(128) not null,
    email varchar(255) not null,
    password varchar(128) not null,
    role enum ('Admin', 'Staff', 'User') not null,
    is_disabled tinyint (1) default 1 not null,
    constraint email unique (email),
    constraint username unique (username)
);

create table meta_item_categories (
    id int auto_increment primary key,
    category_name varchar(255) not null
);

create table meta_item_subcategories (
    id int auto_increment primary key,
    category_id int not null,
    subcategory_name varchar(255) not null,
    constraint meta_item_subcategories_fk1 foreign key (category_id) references meta_item_categories (id)
);

create table meta_item_attributes (
    id int auto_increment primary key,
    attribute_name varchar(255) not null,
    subcategory_id int not null,
    constraint meta_item_attributes_fk1 foreign key (subcategory_id) references meta_item_subcategories (id)
);

create table items (
    id int auto_increment primary key,
    name varchar(255) not null,
    category_id int not null,
    subcategory_id int not null,
    constraint items_fk1 foreign key (category_id) references meta_item_categories (id),
    constraint items_fk2 foreign key (subcategory_id) references meta_item_subcategories (id)
);

create table item_attributes (
    item_id int not null,
    attribute_id int not null,
    attribute_value varchar(255) null,
    constraint item_attributes_fk1 foreign key (item_id) references items (id) on delete cascade,
    constraint item_attributes_fk2 foreign key (attribute_id) references meta_item_attributes (id) on delete cascade
);

create table auctions (
    id int auto_increment primary key,
    item_id int not null,
    seller_id int not null,
    initial_price double not null,
    min_increment double not null,
    min_price double not null,
    opening_time timestamp not null,
    closing_time timestamp not null,
    status enum ('Open', 'Sold', 'Expired') default 'Open' not null,
    constraint auctions_fk1 foreign key (item_id) references items (id),
    constraint auctions_fk2 foreign key (seller_id) references users (id)
);

create table bids (
    id int auto_increment primary key,
    auction_id int not null,
    users_id int not null,
    bid_value double not null,
    bid_active tinyint (1) default 1 not null,
    constraint bids_fk1 foreign key (auction_id) references auctions (id),
    constraint bids_fk2 foreign key (users_id) references users (id)
);

create table user_questions (
    id int auto_increment primary key,
    auction_id int not null,
    asker_id int not null,
    question_text varchar(255) not null,
    is_open tinyint (1) default 1 not null,
    constraint user_questions_fk1 foreign key (auction_id) references auctions (id),
    constraint user_questions_fk2 foreign key (asker_id) references users (id)
);

create table user_answers (
    id int auto_increment primary key,
    question_id int not null,
    replier_id int not null,
    reply_text varchar(255) not null,
    constraint user_answers_fk1 foreign key (question_id) references user_questions (id),
    constraint user_answers_fk2 foreign key (replier_id) references users (id)
);

create table alerts (
    id int auto_increment primary key,
    item_id int not null,
    user_id int not null,
    constraint alerts_fk1 foreign key (user_id) references users (id),
    constraint alerts_fk2 foreign key (item_id) references items (id)
);

create table notifications (
    id int auto_increment primary key,
    user_id int not null,
    item_id int not null,
    constraint notifications_fk1 foreign key (user_id) references users (id) on delete cascade,
    constraint notifications_fk2 foreign key (item_id) references items (id) on delete cascade
);
