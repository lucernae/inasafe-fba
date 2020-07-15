CREATE OR REPLACE FUNCTION kartoza_building_admin_boundary_mapper() RETURNS trigger
    LANGUAGE plpgsql
AS $$
BEGIN
    SELECT
        d.dc_code
    INTO new.district_id
    FROM district d
    WHERE st_within(new.geometry, d.geom);
    RETURN NEW;
END
$$;
