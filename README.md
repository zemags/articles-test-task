# Articles Test Task [![Test](https://github.com/zemags/articles-test-task/workflows/Test/badge.svg)](https://github.com/zemags/articles-test-task/actions)

FastAPI app with optimistic Postgres lock

#### Build app
```bash
docker-compose up -d --build
```
Open http://localhost:8000/docs and work with endpoints

#### Test endpoints
```bash
docker-compose exec web pytest
```

Test code detail: [Test Optimistic Lock](https://github.com/zemags/articles-test-task/blob/3be21ad3370f17b82c4cbe7b81a7e0de3bdc675f/tests/test_articles.py#L112)

One user take article for read, while the second user updated.
Than the frist try to update. But the version of article is different.
Result achieved by tests.

<img src="/pic/arch.png" alt="arch"/>
