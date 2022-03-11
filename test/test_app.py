from app import app


class TestAPI:

    def setup(self):
        # 'Выполняется в начале теста каждого теста'
        app.testing = True
        self.client = app.test_client()

    def test_api_posts(self):
        response = self.client.get('/api/posts')
        assert response.status_code == 200
        temp = []
        assert type(response.json) == type(temp), 'Вернулся  не список'
        assert len(response.json) > 0, 'Пустой список'
        assert ('poster_name' in response.json[0]) == True, 'Нет ключа "poster_name"'
        assert ('poster_avatar' in response.json[0]) == True, 'Нет ключа "poster_avatar"'
        assert ('pic' in response.json[0]) == True, 'Нет ключа "pic"'
        assert ('content' in response.json[0]) == True, 'Нет ключа "content"'
        assert ('views_count' in response.json[0]) == True, 'Нет ключа "views_count"'
        assert ('likes_count' in response.json[0]) == True, 'Нет ключа "likes_count"'
        assert ('pk' in response.json[0]) == True, 'Нет ключа "pk"'

    def test_api_post_id(self):
        response = self.client.get('/api/posts/1')
        assert response.status_code == 200
        temp = dict()
        assert type(response.json) == type(temp), 'Вернулся  не словарь'
        assert ('poster_name' in response.json) == True, 'Нет ключа "poster_name"'
        assert ('poster_avatar' in response.json) == True, 'Нет ключа "poster_avatar"'
        assert ('pic' in response.json) == True, 'Нет ключа "pic"'
        assert ('content' in response.json) == True, 'Нет ключа "content"'
        assert ('views_count' in response.json) == True, 'Нет ключа "views_count"'
        assert ('likes_count' in response.json) == True, 'Нет ключа "likes_count"'
        assert ('pk' in response.json) == True, 'Нет ключа "pk"'

    def teardown(self):
        # выполняется после каждого теста
        pass
