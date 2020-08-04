update sub_district set dc_code = district.dc_code from district where st_within(sub_district.geom, district.geom);
update village set dc_code = sub_district.dc_code, sub_dc_code = sub_district.sub_dc_code from sub_district where st_within(village.geom, sub_district.geom);
