#共享fixture

import uuid

import pytest

from common.http_client import delete, post


@pytest.fixture
def temp_todo():
    # ↓ 前置：准备一条数据（标题唯一，避免并发用例互相干扰）
    title = f"临时数据-{uuid.uuid4().hex[:8]}"
    r = post("/todos", json={"title": title})
    todo = r.json()
    yield todo          # ← 把数据交给用例
    # ↓ 后置：用例跑完，清理掉
    delete(f"/todos/{todo['id']}")


@pytest.fixture
def create_todo():
    created_ids = []

    def _create(title):
        r = post("/todos", json={"title": title})
        created_ids.append(r.json()["id"])
        return r

    yield _create
    for todo_id in created_ids:        # 用例结束后统一清理
        delete(f"/todos/{todo_id}")
