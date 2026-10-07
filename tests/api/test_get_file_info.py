from tests.api.upload import upload
from tests.builders.build_square_kml import build_square_kml


def test_info_matches_the_upload_response(client):
    uploaded = upload(client, "survey.kml", build_square_kml()).json()
    response = client.get(f"/api/files/{uploaded['id']}/")
    assert response.status_code == 200
    assert response.json() == uploaded


def test_unknown_id_returns_404(client):
    response = client.get(f"/api/files/{'0' * 32}/")
    assert response.status_code == 404
    assert response.json()["code"] == "file_not_found"


def test_malformed_id_returns_404(client):
    assert client.get("/api/files/..%2Fsecrets/").status_code == 404
    assert client.get("/api/files/not-an-id/measurements/").status_code == 404
