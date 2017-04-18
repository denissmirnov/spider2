create table torrents
(
	id bigserial not null
		constraint torrents_pkey
			primary key,
	url text,
	text text,
	stamp timestamp with time zone default now(),
	details jsonb,
	torrent_url text,
	rating double precision,
	year integer,
	genre jsonb,
	torrent_name text
);
