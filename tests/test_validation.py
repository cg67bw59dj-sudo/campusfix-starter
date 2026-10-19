from app import validate_ticket
import pytest


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


@pytest.mark.parametrize("title, expected", [
    ("测试工单", 200),      # 有效类代表值（4 字符）
    ("A" * 19, 200),        # 边界内
    ("A" * 20, 200),        # 恰好上限
    ("A" * 21, 400),        # 越界
    ("A" * 100, 400),       # 无效类代表值
])
def test_title_boundary(client, title, expected):
    """等价类 + 边界值分析：用 5 个用例覆盖标题长度的全部情况。

    成功创建会返回 302 重定向，这里用 follow_redirects=True 跟随到首页，
    因此有效输入得到 200，无效输入得到 400。
    """
    resp = client.post(
        "/tickets/new",
        data={"title": title, "room": "A区101", "description": "测试"},
        follow_redirects=True,
    )
    assert resp.status_code == expected

