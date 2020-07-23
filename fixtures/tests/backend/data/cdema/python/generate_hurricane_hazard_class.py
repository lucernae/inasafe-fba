#!/usr/bin/env python


if __name__ == '__main__':
    hazard_class_offset = 5
    # radii class: [34, 50, 64]
    radii_class = [34, 50, 64]
    # intensity class: fro 35 increment in 5 knots until 160
    intensity_class = range(35, 165, 5)
    # verbose as intended to become more readable/understandable
    with open('temp.sql', '+w') as f:

        for i, intensity in enumerate(intensity_class):
            for r, radii in enumerate(radii_class):
                hazard_class = hazard_class_offset + i * 3 + r
                label = 'INTENSITY : {} - RADII : {}'.format(intensity, radii)
                sql_statement = """INSERT INTO public.hazard_class (id, label, hazard_type) VALUES ({hazard_class}, '{label}', 2) ON CONFLICT DO NOTHING ;\n""".format(hazard_class=hazard_class, label=label)
                f.write(sql_statement)
