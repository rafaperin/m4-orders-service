create table if not exists orders (
	order_id uuid primary key,
	customer_id uuid not null,
    creation_date timestamp default now(),
    order_total decimal(7,2)
);

create table if not exists order_items (
	id serial primary key,
	order_id uuid references orders(order_id) on delete cascade,
	product_id uuid not null,
	product_quantity integer not null
);

alter table order_items
add constraint constraint_order_id
foreign key (order_id)
references orders (order_id);
