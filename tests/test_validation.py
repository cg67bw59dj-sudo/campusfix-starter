from app import validate_ticket


def test_title_too_long():
    """课14：函数级单元测试，直接调用校验函数。"""
    error = validate_ticket("A" * 21, "A101")
    assert error == "标题不能超过20个字符"


def test_post_title_too_long(client):
    """课15：请求级测试，走真实的 POST 表单提交。

    与上面的单元测试互补：这条能同时验证字段名、路由调用、
    HTTP 状态码和响应内容，但定位问题时不如单元测试直接。
    """
    resp = client.post(
        "/tickets/new",
        data={
            "title": "A" * 21,
            "room": "A区101",
            "description": "测试",
        },
    )
    assert resp.status_code == 400
    assert "标题不能超过20个字符" in resp.data.decode()

