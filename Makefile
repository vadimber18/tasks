run:
	docker-compose up --build
test:
	docker-compose -f docker-compose-test.yml up --build
lint:
	docker-compose -f docker-compose-lint.yml up --build
