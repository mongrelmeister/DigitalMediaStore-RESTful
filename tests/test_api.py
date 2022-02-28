# """API tests"""
# # pylint: disable=invalid-name

DUMMY_ID = 0

BASE_URL = "/api"
ARTISTS_URL = "/artists/"
ALBUMS_URL = "/albums/"


class TestApi:
    """TEST API"""

    artist_1_id = artist_1_etag = artist_1 = None
    album_1_id = album_1_etag = album_1 = None
    album_2_id = album_2_etag = album_2 = None

    def test_artists_url(self, test_client):
        """GET ARTISTS"""
        ret = test_client.get(BASE_URL + ARTISTS_URL)
        assert ret.status_code == 200
        assert ret.json == []

    def test_artists_post(self, test_client):
        """ADD ARTISTS"""
        TestApi.artist_1 = {"name": "AC / DC"}

        ret = test_client.post(BASE_URL + ARTISTS_URL, json=TestApi.artist_1)
        assert ret.status_code == 201

        ret_val = ret.json
        TestApi.artist_1_id = ret_val.pop("id")
        TestApi.artist_1_etag = ret.headers["ETag"]
        assert ret_val == TestApi.artist_1

    def test_artists_get_list(self, test_client):
        """GET ARTISTS LIST"""
        ret = test_client.get(BASE_URL + ARTISTS_URL)
        assert ret.status_code == 200

        ret_val = ret.json
        assert len(ret_val) == 1
        assert ret_val[0]["id"] == TestApi.artist_1_id

    def test_artists_get_by_id(self, test_client):
        """GET ARTISTS BY ID"""
        ret = test_client.get(BASE_URL + ARTISTS_URL + str(TestApi.artist_1_id))
        assert ret.status_code == 200
        assert ret.headers["ETag"] == TestApi.artist_1_etag

        ret_val = ret.json
        ret_val.pop("id")
        assert ret_val == TestApi.artist_1

    def test_artists_put(self, test_client):
        """PUT ARTISTS"""
        TestApi.artist_1.update({"name": "AC/DC"})

        ret = test_client.put(
            BASE_URL + ARTISTS_URL + str(TestApi.artist_1_id),
            json=TestApi.artist_1,
            headers={"If-Match": TestApi.artist_1_etag},
        )
        assert ret.status_code == 200

        ret_val = ret.json
        ret_val.pop("id")
        TestApi.artist_1_etag = ret.headers["ETag"]
        assert ret_val == TestApi.artist_1

    def test_artists_put404(self, test_client):
        """PUT ARTISTS WITH WRONG ID"""
        ret = test_client.put(
            BASE_URL + ARTISTS_URL + str(DUMMY_ID),
            json=TestApi.artist_1,
            headers={"If-Match": TestApi.artist_1_etag},
        )
        assert ret.status_code == 404

    def test_albums_url(self, test_client):
        """GET ALBUMS"""
        ret = test_client.get(BASE_URL + ALBUMS_URL)
        assert ret.status_code == 200
        assert ret.json == []

    def test_albums_post(self, test_client):
        """ADD ALBUMS"""
        TestApi.album_1 = {"title": "For Those About To Rock We Salute You", "artist_id": TestApi.artist_1_id}
        TestApi.album_2 = {"title": "Let There Be Rock", "artist_id": None}

        ret = test_client.post(BASE_URL + ALBUMS_URL, json=TestApi.album_1)
        assert ret.status_code == 201

        ret_val = ret.json
        ret_val["artist"].pop("id")
        TestApi.album_1_id = ret_val.pop("id")
        TestApi.album_1_etag = ret.headers["ETag"]
        TestApi.album_1.pop("artist_id")
        TestApi.album_1.update({"artist": TestApi.artist_1})
        assert ret_val == TestApi.album_1

        ret = test_client.post(BASE_URL + ALBUMS_URL, json=TestApi.album_2)
        assert ret.status_code == 422

        TestApi.album_2.update({"artist_id": TestApi.artist_1_id})
        ret = test_client.post(BASE_URL + ALBUMS_URL, json=TestApi.album_2)
        assert ret.status_code == 201

        ret_val = ret.json
        ret_val["artist"].pop("id")
        TestApi.album_2_id = ret_val.pop("id")
        TestApi.album_2_etag = ret.headers["ETag"]
        TestApi.album_2.pop("artist_id")
        TestApi.album_2.update({"artist": TestApi.artist_1})
        assert ret_val == TestApi.album_2

    def test_albums_get_list(self, test_client):
        """GET ALBUMS LIST"""
        ret = test_client.get(BASE_URL + ALBUMS_URL)
        assert ret.status_code == 200

        ret_val = ret.json
        assert len(ret_val) == 2
        assert ret_val[0]["id"] == TestApi.album_1_id
        assert ret_val[1]["id"] == TestApi.album_2_id

    def test_albums_get_by_id(self, test_client):
        """GET ALBUMS BY ID"""
        ret = test_client.get(BASE_URL + ALBUMS_URL + str(TestApi.album_1_id))
        assert ret.status_code == 200
        assert ret.headers["ETag"] == TestApi.album_1_etag

        ret_val = ret.json
        ret_val.pop("id")
        ret_val["artist"].pop("id")
        assert ret_val == TestApi.album_1

        ret = test_client.get(BASE_URL + ALBUMS_URL + str(TestApi.album_2_id))
        assert ret.status_code == 200
        assert ret.headers["ETag"] == TestApi.album_2_etag

        ret_val = ret.json
        ret_val.pop("id")
        ret_val["artist"].pop("id")
        assert ret_val == TestApi.album_2

    def test_albums_put(self, test_client):
        """PUT ALBUMS"""
        TestApi.album_2.update({"title": "Hágase el Rock", "artist_id": TestApi.artist_1_id})
        TestApi.album_2.pop("artist")

        ret = test_client.put(
            BASE_URL + ALBUMS_URL + str(TestApi.album_2_id),
            json=TestApi.album_2,
            headers={"If-Match": TestApi.album_2_etag},
        )
        assert ret.status_code == 200

        ret_val = ret.json
        ret_val.pop("id")
        ret_val["artist"].pop("id")
        TestApi.album_2_etag = ret.headers["ETag"]
        TestApi.album_2.pop("artist_id")
        TestApi.album_2["artist"] = TestApi.artist_1
        assert ret_val == TestApi.album_2

    def test_albums_put404(self, test_client):
        """PUT ALBUMS WITH WRONG ID"""
        TestApi.album_1.update({"artist_id": TestApi.artist_1_id})
        TestApi.album_1.pop("artist")

        ret = test_client.put(
            BASE_URL + ALBUMS_URL + str(DUMMY_ID),
            json=TestApi.album_1,
            headers={"If-Match": TestApi.album_1_etag},
        )
        assert ret.status_code == 404

    def test_albums_put400(self, test_client):
        """PUT ALBUMS WITH UNKNOWN ARTIST ID"""
        TestApi.album_2.update({"artist_id": DUMMY_ID})
        # TestApi.album_2.pop("artist")

        ret = test_client.put(
            BASE_URL + ALBUMS_URL + str(TestApi.album_2_id),
            json=TestApi.album_2,
            headers={"If-Match": TestApi.album_2_etag},
        )
        assert ret.status_code == 400

    def test_albums_delete(self, test_client):
        """DELETE ALBUMS"""
        ret = test_client.delete(
            BASE_URL + ALBUMS_URL + str(TestApi.album_2_id),
            headers={"If-Match": TestApi.album_2_etag},
        )
        assert ret.status_code == 204

    def test_artists_delete(self, test_client):
        """DELETE ARTISTS ==> DELETE ALBUMS WITH CASCADE"""
        # DELETE
        ret = test_client.delete(
            BASE_URL + ARTISTS_URL + str(TestApi.artist_1_id),
            headers={"If-Match": TestApi.artist_1_etag},
        )
        assert ret.status_code == 204

        # GET list
        ret = test_client.get(BASE_URL + ARTISTS_URL)
        assert ret.status_code == 200
        assert ret.json == []

        # GET by id artists -> 404
        ret = test_client.get(BASE_URL + ARTISTS_URL + str(TestApi.artist_1_id))
        assert ret.status_code == 404

        # GET by id albums -> 404
        ret = test_client.get(BASE_URL + ALBUMS_URL + str(TestApi.album_1_id))
        assert ret.status_code == 404
