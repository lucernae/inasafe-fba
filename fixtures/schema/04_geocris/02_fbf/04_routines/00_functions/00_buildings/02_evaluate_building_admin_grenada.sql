CREATE OR REPLACE FUNCTION public.kartoza_evaluate_building_admin() RETURNS VARCHAR
    LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE osm_buildings
    SET
        district_id = d.dc_code
    FROM
         district d
    WHERE st_within(geometry, d.geom);
 RETURN 'OK';
END
$$;
