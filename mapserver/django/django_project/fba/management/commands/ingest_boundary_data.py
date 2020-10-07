import random
import hashlib
import psycopg2 as driv

from postgis.psycopg import register

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from fba.models.all import District


class Command(BaseCommand):
    """ Command to process first hazard event queue. """
    base_url = 'https://geocris2.cdema.org/'
    limit = 10

    def is_table_exists(self, conn, table_name, schema_name):
        query = 'SELECT EXISTS (' \
                    'SELECT FROM information_schema.tables ' \
                    'WHERE  table_schema = \'{schema_name}\' ' \
                    'AND table_name   = \'{table_name}\' ' \
                ')'.format(
            schema_name=schema_name,
            table_name=table_name
        )
        cur = conn.cursor()
        cur.execute(query)
        is_exist = cur.fetchone()
        return is_exist[0]

    def get_table_header(self, conn, table_name):
        cur = conn.cursor()
        sql = "SELECT * FROM {table_name} WHERE 1=0".format(
            table_name=table_name
        )
        cur.execute(sql)
        table_header = [d[0] for d in cur.description]
        cur.close()
        return table_header

    def get_admin_data(self, conn, table_name):
        cur = conn.cursor()
        sql = "SELECT * FROM {table_name}".format(
            table_name=table_name
        )
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def create_connection(self):
        try:
            conn = driv.connect(database='gis',
                                user='docker',
                                password='docker',
                                host='192.168.1.197',
                                port='45432')
            register(conn)
            return conn
        except driv.OperationalError as e:
            print(e)
        return None

    def get_all_schemas(self, conn):
        cur = conn.cursor()
        query = (
            'SELECT schema_name FROM information_schema.schemata '
            'WHERE length(schema_name) = 3'
        )
        cur.execute(query)
        schemas_list = cur.fetchall()
        schema_names = []
        for schema_name in schemas_list:
            schema_names.append(schema_name[0])
        cur.close()
        return schema_names

    def handle(self, *args, **options):
        conn = self.create_connection()
        schema_names = self.get_all_schemas(conn)
        table_to_check = [
            'bnd_adm2_pop_polygon',
            'bnd_adm1_pop_polygon',
            'bnd_adm1_polygon',
        ]
        for schema_name in schema_names:
            table_name = ''
            table_to_check_index = 0
            is_exist = False
            while not is_exist and table_to_check_index < len(table_to_check):
                table_name = '{schema}.{schema}_{table_name}'.format(
                    schema=schema_name,
                    table_name=table_to_check[table_to_check_index]
                )
                is_exist = self.is_table_exists(
                    conn,
                    '{schema}_{table_name}'.format(
                        table_name=table_to_check[table_to_check_index],
                        schema=schema_name
                    ),
                    schema_name
                )
                table_to_check_index += 1

            # Table exists, get name, pop and geometry
            if is_exist:
                rows = self.get_admin_data(conn, table_name)
                header = self.get_table_header(conn, table_name)
                for row in rows:
                    geometry = None
                    if 'name' in header:
                        name = row[header.index('name')]
                    else:
                        if 'district' in header:
                            name = row[header.index('district')]
                        else:
                            name = '{schema}_{id}'.format(
                                schema=schema_name,
                                id=row[0]
                            )

                    if 'pop' in header:
                        pop = row[header.index('pop')]
                    else:
                        pop = random.randint(100, 10000)
                    if 'geom' in header:
                        geometry = row[header.index('geom')]
                    if geometry:
                        geojson = geometry.geojson
                        geom = GEOSGeometry(str(geojson))

                        all_district = District.objects.all().order_by('-id')
                        district_id = all_district[0].id + 1
                        dc_code_name = '{id}:{schema}:{name}'.format(
                            id=district_id,
                            schema=schema_name,
                            name=name
                        )
                        dc_code = int(hashlib.sha1(dc_code_name.encode('utf-8')).hexdigest(), 16) % (10 ** 7)
                        try:
                            district, created = District.objects.get_or_create(
                                id=district_id,
                                geom=geom,
                                name=name,
                                dc_code=dc_code
                            )
                            print('District {cc} - {n} = {c}'.format(
                                cc=schema_name,
                                n=name,
                                c=created
                            ))
                        except Exception as e:
                            print(str(e))
