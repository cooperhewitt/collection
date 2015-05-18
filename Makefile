prune:
	git gc --aggressive --prune

build:	prune csv glossary pubdate prune

csv:
	bin/generate-csv-exhibitions.py
	bin/generate-csv-objects.py
	bin/generate-csv-people.py
	bin/generate-csv-periods.py
	bin/generate-csv-roles.py
	bin/generate-csv-types.py

glossary:
	bin/generate-glossary.py --objects departments --glossary meta/departments-glossary.json
	bin/publish-glossary.py --glossary meta/departments-glossary.json --markdown meta/departments-glossary.md

	bin/generate-glossary.py --objects exhibitions --glossary meta/exhibitions-glossary.json
	bin/publish-glossary.py --glossary meta/exhibitions-glossary.json --markdown meta/exhibitions-glossary.md

	bin/generate-glossary.py --objects objects --glossary meta/objects-glossary.json
	bin/publish-glossary.py --glossary meta/objects-glossary.json --markdown meta/objects-glossary.md

	bin/generate-glossary.py --objects people --glossary meta/people-glossary.json
	bin/publish-glossary.py --glossary meta/people-glossary.json --markdown meta/people-glossary.md

	bin/generate-glossary.py --objects periods --glossary meta/periods-glossary.json
	bin/publish-glossary.py --glossary meta/periods-glossary.json --markdown meta/periods-glossary.md

	bin/generate-glossary.py --objects roles --glossary meta/roles-glossary.json
	bin/publish-glossary.py --glossary meta/roles-glossary.json --markdown meta/roles-glossary.md

	bin/generate-glossary.py --objects types --glossary meta/types-glossary.json
	bin/publish-glossary.py --glossary meta/types-glossary.json --markdown meta/types-glossary.md

pubdate:
	echo `date` > PUBDATE.md
