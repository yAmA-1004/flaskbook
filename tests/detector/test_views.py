from apps.detector.models import UserImage
from pathlib import Path

from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage


def test_index(client):
    rv = client.get("/")
    assert "ログイン" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


def signup(client, username, email, password):
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)


def test_index_signup(client):
    rv = signup(client, "admin", "flaskbook@example.com", "password")
    assert "admin" in rv.data.decode()

    rv = client.get("/")
    assert "ログアウト" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


def test_upload_no_auth(client):
    rv = client.get("/upload", follow_redirects=True)
    assert "アップロード" not in rv.data.decode()
    assert "メールアドレス" in rv.data.decode()
    assert "パスワード" in rv.data.decode()


def test_upload_signup_get(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = client.get("/upload")
    assert "アップロード" in rv.data.decode()


def upload_image(client, image_path):
    image = Path(get_root_path("tests"), image_path)

    test_file = (
        FileStorage(stream=open(image, "rb"), filename=Path(image_path).name, content_type="multipart/form-data", ),)

    data = dict(
        image=test_file,
    )
    return client.post("/upload", data=data, follow_redirects=True)


def test_upload_signup_post_validate(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")
    assert "サポートされていない画像形式です。" in rv.data.decode()


def test_upload_signup_post(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()


def test_detect_no_user_image(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    rv = client.post("/detect/nonexistent", follow_redirects=True)
    assert "物体検知対象の画像が存在しません。" in rv.data.decode()


def test_detect(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    rv = client.post(f"/detect/{user_image.id}", follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()


def test_detect_search(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    client.post(f"/detect/{user_image.id}", follow_redirects=True)

    rv = client.get("/images/search?search=dog")
    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()

    rv = client.get("/images/search?search=test")
    assert user_image.image_path not in rv.data.decode()
    assert "dog" not in rv.data.decode()


def test_delete(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    UserImage.query.first()

    user_image = UserImage.query.first()
    image_path = user_image.image_path
    rv = client.post(f"/images/delete/{user_image.id}", follow_redirects=True)
    assert image_path not in rv.data.decode()


def test_custom_error(client):
    rv = client.get("/notfound")
    assert "404 Not Found" in rv.data.decode()

