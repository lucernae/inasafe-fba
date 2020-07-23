ALTER TABLE hazard_class ADD COLUMN IF NOT EXISTS hazard_type INTEGER;
ALTER TABLE hazard_class DROP CONSTRAINT IF EXISTS  hazard_type_pkey;
ALTER TABLE hazard_class ADD CONSTRAINT hazard_type_pkey
    FOREIGN KEY (hazard_type) REFERENCES hazard_type (id);
