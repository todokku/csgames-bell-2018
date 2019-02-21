import sys, hashlib
import datetime

from flask import Blueprint, jsonify, request, render_template

bell_blueprint = Blueprint("bell", __name__, template_folder="./templates")


# def asset_matches_id(asset, profile_ids):
#     for profile_id in asset["profileIds"]:
#         if profile_id in profile_ids:
#             return True
#     return False


@bell_blueprint.route("/app/ping")
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong"
    })


@bell_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bell_blueprint.route("/bell/authentication", methods=["POST", "PUT"])
def bell_authentication():
    response = {}
    request_json = request.get_json()
    if request.method == "POST":
        username = request_json["username"]
        password = request_json["password"].encode("utf-8")
        users = get_auth_data()
        user_object = get_user(username)
        
        if user_object is None:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
        hashed_password = hashlib.sha256(password).hexdigest()
        if hashed_password != user_object["hashedPassword"]:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
    elif request.method == "PUT":
        hashed_credentials = request_json["hashedCredentials"].split(":")
        username = hashed_credentials[0]
        hashed_password = hashed_credentials[1]
        user_object = get_user(username)
        if user_object is None:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
        update_user_password(username, hashed_password)

    response["accountId"] = user_object["id"]
    response["profiles"] = []
    for profile in user_object["profiles"]:
        response["profiles"].append(profile["name"])
    response["hashedCredentials"] = username + ":" + hashed_password
    return jsonify(response)


# @bell_blueprint.route("/bell/assets")
# def bell_assets():
#     response = []
#     profile_names = profiles = request.args.getlist("profiles")
#     profile_data = get_profile_data()
#     profile_ids = []
#     for name in profile_names:
#         profile_ids.append(profile_data[name])
#     prog_data = get_prog_data()
#     assets = prog_data["assets"]
#     providers = prog_data["providers"]

#     for asset in assets:
#         start = dateutil.parser.parse(asset["licensingWindow"]["start"])
#         end = dateutil.parser.parse(asset["licensingWindow"]["end"])
#         current = datetime.datetime.utcnow().replace(
#             tzinfo=datetime.timezone.utc
#         )
#         match = asset_matches_id(asset, profile_ids)
#         if start > current or end < current or not match:
#             continue
#         provider_name, refresh_rate_in_seconds = get_provider_info(
#             providers,
#             asset["providerId"]
#         )
#         asset_dict = {
#             "title": asset["title"],
#             "providerId": provider_name,
#             "refreshRateInSeconds": refresh_rate_in_seconds,
#             "media": {
#                 "mediaId": asset["mediaId"],
#                 "durationInSeconds": asset["durationInSeconds"]
#             }
#         }
#         response.append(asset_dict)
#     return jsonify(response)
