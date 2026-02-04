from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_authorship():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """ SELECT * 
                    FROM authorship"""
        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_roles():
        conn = DBConnect.get_connection()
        roles = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT role
                FROM authorship
                """

        cursor.execute(query)
        for row in cursor:
            roles.append(row['role'])
        conn.close()
        cursor.close()
        return roles

    @staticmethod
    def get_artist_for_role(role):
        conn = DBConnect.get_connection()
        artists = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT a.artist_id, a.name
                FROM artists a, authorship au, objects o
                WHERE a.artist_id = au.artist_id
                AND o.object_id = au.object_id
                AND au.role = %s
                AND o.curator_approved = 1    
                """

        cursor.execute(query, (role,))
        for row in cursor:
            artist = Artist(**row)
            artists.append(artist)
        conn.close()
        cursor.close()
        return artists


    @staticmethod
    def get_edges(role, id_map):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        edges = []
        query = """
                SELECT t1.artist_id as n1, t2.artist_id as n2, t1.ip-t2.ip as peso
                FROM    (SELECT a.artist_id, COUNT(*) AS ip
                        FROM authorship a, objects o 
                        WHERE a.object_id = o.object_id
                            AND curator_approved = 1
                            AND a.role = %s
                            GROUP BY a.artist_id) t1,
                        (SELECT a.artist_id, COUNT(*) AS ip
                        FROM authorship a, objects o 
                        WHERE a.object_id = o.object_id
                            AND curator_approved = 1
                            AND a.role = %s
                            GROUP BY a.artist_id) t2
                WHERE t1.artist_id <> t2.artist_id
                AND t1.ip < t2.ip
                GROUP BY t1.artist_id, t2.artist_id                    
                """

        cursor.execute(query, (role, role,))

        for row in cursor:
            edges.append((id_map[row["n1"]], id_map[row["n2"]], row["peso"]))

        conn.close()
        cursor.close()
        return edges





