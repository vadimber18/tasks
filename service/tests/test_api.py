import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, count, fields",
    [
        ("/tasks", 4, {}),
        ("/tasks?limit=2", 2, {}),
        ("/tasks?name=fin", 1, {"name": "some finished io task"}),
        ("/tasks?status=1", 1, {"name": "some task", "status": 1}),
    ],
)
async def test_get_tasks(cli, db_data, url, count, fields):
    response = await cli.get(url)
    assert response.status_code == 200
    data = response.json()
    for each in data:
        for key, value in fields.items():
            assert each[key] == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, fields",
    [
        ("/tasks/1", {"name": "some task", "status": 1}),
        ("/tasks/2", {"task_id": 2, "processing_time": 13}),
    ],
)
async def test_get_task(cli, db_data, url, fields):
    response = await cli.get(url)
    assert response.status_code == 200
    data = response.json()
    for key, value in fields.items():
        assert data[key] == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, json, status_code, fields",
    [
        ("/tasks", {"name": "new task", "processing_time": "a"}, 422, {}),
    ],
)
async def test_create_task(
    cli,
    db_data,
    mocker,
    url,
    json,
    status_code,
    fields,
):
    mocker.patch("app.helpers.publish_message", return_value=None)
    response = await cli.get(url)
    response = await cli.post(url, json=json)
    assert response.status_code == status_code
    data = response.json()
    for key, value in fields.items():
        assert data[key] == value


@pytest.mark.asyncio
async def test_update_task(cli, db_data, mocker):
    response = await cli.patch("/tasks/1", json={"status": 4})
    assert response.status_code == 204
    response = await cli.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["status"] == 4
