ALTER TABLE hazard_class ADD COLUMN hazard_type INTEGER;
ALTER TABLE hazard_class ADD CONSTRAINT hazard_type_pkey
    FOREIGN KEY (hazard_type) REFERENCES hazard_type (id);