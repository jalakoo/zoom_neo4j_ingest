# Constraints needed in target Neo4j Database

```
CREATE CONSTRAINT unique_profile_id IF NOT EXISTS FOR (a:Profile) REQUIRE (a.id) IS UNIQUE

```
