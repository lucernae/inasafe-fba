CREATE OR REPLACE FUNCTION public.kartoza_evaluate_road_admin() RETURNS VARCHAR
    LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE osm_roads
    SET
        district_id = d.dc_code
    FROM
         district d
    WHERE st_within(geometry, d.geom);
 RETURN 'OK';
END
$$;
