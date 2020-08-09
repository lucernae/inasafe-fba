
--- District is equal to admin level 6
insert into district (id, geom, dc_code, name)
(select id, st_multi(geometry), id, name from osm_admin where admin_level = 6) on conflict DO NOTHING ;

insert into sub_district (id, geom, sub_dc_code, name)
(select id, st_multi(geometry), id, name from osm_admin where admin_level = 9) on conflict DO NOTHING ;

insert into village (id, geom, village_code, name)
(select id, st_multi(geometry), id, name from osm_admin where admin_level = 10) on conflict DO NOTHING ;
