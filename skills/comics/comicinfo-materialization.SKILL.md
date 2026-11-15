# ComicInfo Materialization Skill

Use this skill after identity resolution and before CBZ mutation.

1. Extract and parse embedded `ComicInfo.xml`, if present.
2. Otherwise seed ComicInfo from the nearest `series.json`.
3. Fill and cross-check fields from the CBL cache, GCD, Metron API, then ComicVine API.
4. Resolve the ComicVine issue ID before generating the external filename.
5. Sanitize the series name and normalize the issue number to three digits.
6. Generate `CV-[series]-#000-(year)-CVID.xml` beside the CBZ.
7. Use exclusive creation and stop on filename collision.
8. Validate the proposal independently of the CBZ.
9. Only an explicit apply phase may upsert the XML into the CBZ.

Do not overwrite archives, edit canonical caches, or fabricate missing IDs.
