import config
import asyncpg


class DBManager:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Connect to the database"""
        self.pool = await asyncpg.create_pool(dsn=config.DB_DNS)

    async def disconnect(self):
        """Disconnect from the database"""
        if self.pool is not None:
            await self.pool.close()

    async def fetch(self, query: str, *args):
        """Fetch a list of objects from the database"""
        async with self.pool.acquire() as connection:
            results = await connection.fetch(query, *args)
            return [dict(result) for result in results]

    async def fetch_one(self, query: str, *args):
        """Fetch a single object from the database"""
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
            if result is None:
                return None  # Agar natija None bo'lsa, None qaytarish
            return dict(result)

    async def fetch_all(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query, *args):
        """Execute a SQL command"""
        async with self.pool.acquire() as connection:
            await connection.execute(query, *args)

    async def create_tables(self):
        queries = [
            """
            CREATE TABLE directors (
                id SERIAL PRIMARY KEY,          -- Unikal identifikator
                name VARCHAR NOT NULL,          -- Direktor ismi
                score INTEGER DEFAULT 0,        -- Ball (standart qiymati 0)
                school_number VARCHAR           -- Maktab raqami
        );

            CREATE TABLE users (
                id SERIAL PRIMARY KEY,          
                vote_director INTEGER,
                created_at TIMESTAMP DEFAULT NOW(),
                CONSTRAINT fk_vote_director FOREIGN KEY (vote_director) REFERENCES directors (id)
        );
            """
        ]

        for query in queries:
            await self.execute(query)

    async def get_directors(self):
        query = "SELECT * FROM directors ORDER BY id ASC"
        return await self.fetch(query)

    async def get_director_by_id(self, id):
        query = "SELECT * FROM directors WHERE id = $1"
        return await self.fetch_one(query, (int(id)))

    async def update_director_score(self, id, new_score):
        query = "UPDATE directors SET score = $1 WHERE id = $2"
        await self.execute(query, new_score, int(id))

    async def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = $1"
        user = await self.fetch_one(query, user_id)
        if not user:
            return None
        return user

    async def update_user_vote(self, user_id, director_id):
        director_id = int(director_id)

        query = "UPDATE users SET vote_director = $1 WHERE id = $2"
        await self.execute(query, director_id, user_id)

    async def create_user(self, user_id: int):
        query = """
        INSERT INTO users (id, vote_director, created_at)
        VALUES ($1, NULL, CURRENT_TIMESTAMP);
        """
        await self.execute(query, user_id)

    async def get_all_directors(self):
        query = "SELECT name, school_number, score FROM directors ORDER BY score DESC"
        return await self.fetch_all(query)

db = DBManager()






# INSERT INTO directors (id, name, score, school_number)
# VALUES
# (1, 'Hulkar Amanbayeva', 0, '1-maktab'),
# (2, 'Jumagul Bo`ronova', 0, '2-maktab'),
# (3, 'Nodirbek Toshboyev', 0, '3-maktab'),
# (4, 'Marg`uba Zoirova', 0, '4-maktab'),
# (5, 'Husan G`aynazarov', 0, '5-maktab'),
# (6, 'Zuhra Po`latova', 0, '7-maktab'),
# (7, 'Barno Turg`unboyeva', 0, '8-maktab'),
# (8, 'Hafiza Umarova', 0, '9-maktab'),
# (9, 'Nigora Asqarova', 0, '10-maktab'),
# (10, 'Rano Baxramova', 0, '11-maktab'),
# (11, 'Mamurjon Qobilov', 0, '12-maktab'),
# (12, 'Gulbahor Altmishova', 0, '13-maktab'),
# (13, 'Matluba Toshmatova', 0, '14-maktab'),
# (14, 'Saparali Turakulov', 0, '15-maktab'),
# (15, 'Lenura Baydullayeva', 0, '16-maktab'),
# (16, 'Malika Miraxmedova', 0, '17-maktab'),
# (17, 'Eldor Sheranov', 0, '18-maktab'),
# (18, 'Sevar Qodirova', 0, '19-maktab'),
# (19, 'Inoyat Ergasheva', 0, '20-IDUM'),
# (20, 'Ro`zmat Loikov', 0, '21-maktab'),
# (21, 'Hamid Nishonov', 0, '22-maktab'),
# (22, 'Nafisa Tursunboyeva', 0, '23-maktab'),
# (23, 'Andryan Dadayev', 0, '24-maktab');
