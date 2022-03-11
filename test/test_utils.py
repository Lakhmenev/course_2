import pytest
import utils
from app import app


def test_error_json_load_data_from_json():
    assert utils.load_data_from_json('./data/data_er.json') == None, 'Ошибка обработки JSON'


def test_error_file_not_found_load_data_from_json():
    assert utils.load_data_from_json('./data/data1.json') == None, 'Ошибка обработки несуществующего файла'


def test_get_posts_by_user():
    with pytest.raises(AttributeError):
        utils.get_posts_by_user(2)


def test_app():
    response = app.test_client().get('/')
    assert response.status_code == 200, 'Не загружжены данные постов'
