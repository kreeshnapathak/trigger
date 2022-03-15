--create table t1 and t2
--used postgre for this operation


--function to be called after trigger
CREATE OR REPLACE FUNCTION notify_id_trigger() RETURNS trigger AS $$
BEGIN
PERFORM pg_notify('new_id',json_build_object('table', TG_TABLE_NAME, 'type', TG_OP, 'row', row_to_json(NEW))::text);
RETURN new;
END;
$$ LANGUAGE plpgsql;

--to end the trigger
drop TRIGGER buy_sell_signal_trigger  on pt_data.buy_sell_signal ;
drop TRIGGER buy_sell_signal_early_trigger  on pt_data.buy_sell_signal_early ;

--create trigger to check the data insert and call above function
create t1  after  insert or update on table1 for each row execute procedure notify_id_trigger();
create t2 after  insert or update on table2 for each row execute procedure notify_id_trigger();

--check the trigger after inserting data as

--inserting data
INSERT INTO table1 ("date",name,price) VALUES
	 ('2025-05-05','NICA',600);

INSERT INTO table2 ("date",name,price) VALUES
	 ('2025-05-05','NICA',600);
