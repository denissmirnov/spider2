create table torrents
(
	id bigserial not null
		constraint torrents_pkey
			primary key,
	url text,
	text text,
	stamp timestamp with time zone default now(),
	details jsonb,
	rating double precision,
	year integer,
	genre jsonb,
	torrent_name text,
	torrent_url jsonb
);
