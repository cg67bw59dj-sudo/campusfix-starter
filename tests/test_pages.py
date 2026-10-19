"""页面级测试：用 Flask 测试客户端模拟浏览器，直接调用路由，不走网络。"""


def test_index(client):
    """访问首页应返回 200，并包含应用标题。"""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CampusFix" in resp.data.decode()


def test_detail(client):
    """先创建一个工单，再访问它的详情页。

    测试用的临时库是空的（fixture 只建表不塞数据），
    所以必须先自己造一条工单，才能测详情页。
    """
    client.post(
        "/tickets/new",
        data={"title": "详情页测试", "room": "A区101", "description": "灯坏了"},
    )
    resp = client.get("/tickets/1")
    assert resp.status_code == 200
    text = resp.data.decode()
    assert "详情页测试" in text
    assert "A区101" in text


def test_create(client):
    """提交新工单后应重定向回首页，且列表中出现该工单。"""
    resp = client.post(
        "/tickets/new",
        data={"title": "测试工单", "room": "A区101", "description": "灯坏了"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "测试工单" in resp.data.decode()
