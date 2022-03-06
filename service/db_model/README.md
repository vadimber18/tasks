# db-model

## Описание
Модели для сервиса `tasks-api`. Поддерживаются автогенерируемые миграции.

## Миграции

`cd db_model/alembic`

`alembic revision -m "init"` - будет создана новая пустая миграция, внести необходимые изменения в `upgrade` и `downgrade`

`alembic revision --autogenerate -m "init"` - автогенерация миграций

`alembic upgrade head` - накатить миграции

`alembic downgrade -1` - откатить последнюю миграцию


подробнее: https://alembic.sqlalchemy.org/en/latest/tutorial.html
