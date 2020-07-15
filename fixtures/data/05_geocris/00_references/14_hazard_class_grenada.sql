INSERT INTO public.hazard_class (id, min_m, max_m, label) VALUES (5, 0, 0.7, '1:50 year extent') ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_class (id, min_m, max_m, label) VALUES (6, 0.7, 1.5, '1:20 year extent') ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_class (id, min_m, max_m, label) VALUES (7, 1.5, 3, '1:10 year extent') ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_class (id, min_m, max_m, label) VALUES (8, 3, 999999, '1:5 year extent') ON CONFLICT DO NOTHING ;
