CREATE TABLE turkers(
  person_id TEXT PRIMARY KEY, -- internal name, = login user
  turker_id TEXT UNIQUE DEFAULT NULL, -- id on amazon platform
  password TEXT, -- not encrypted
  datetime_connected INTEGER DEFAULT NULL -- when was this internal user connected to a turker? unix timestamp
);

CREATE TABLE abstracts(
  person_id TEXT, -- ->turkers.person_id
  pmid TEXT, -- abstract pmid
  time_taken INTEGER DEFAULT NULL -- how long did it take the turker to annotate this abstract? In seconds. If null: abstract not finished yet.
);
