# Constraints needed in target Neo4j Database

```
CREATE CONSTRAINT unique_profile_id IF NOT EXISTS FOR (a:Profile) REQUIRE (a.id) IS UNIQUE


CREATE CONSTRAINT unique_meeting_uuid IF NOT EXISTS FOR (a:Meeting) REQUIRE (a.uuid) IS UNIQUE
```
