import argparse
import json
import re
import requests
import logging

API = "https://api.soracom.io/v1"

def post_json(url, body_dict):
    return requests.post(
        url, headers={"content-type": "application/json"}, data=json.dumps(body_dict)
    )

def get_with_auth(url, token):
    return requests.get(
        url,
        headers={
            "x-soracom-api-key": token["apiKey"],
            "x-soracom-token": token["token"],
        },
    )

def delete_image(base_path, file_name, token):
    url = API + "/files/private" + base_path + file_name
    return requests.delete(
        url,
        headers={
            "x-soracom-api-key": token["apiKey"],
            "x-soracom-token": token["token"],
        },
    )
def get_and_save_images(file_names, base_path, save_path, limit_size_to_files, is_delete, token):
    download_count = 0
    download_size = 0
    for file_name in file_names:
        response = get_with_auth(API + "/files/private" + base_path + file_name, token)
        with open(save_path + file_name, "wb") as handle:
            logging.debug("Writing {}".format(file_name))
            handle.write(response.content)
        logging.debug(file_name)
        download_count += 1
        download_size += len(response.content)
        if is_delete:
            logging.debug("Deleting {}".format(file_name))
            delete_image(base_path, file_name, token)

        if limit_size_to_files < download_size:
            break
    
    logging.info("Download Count:" + str(download_count))
    logging.info("Download Size:" + str(download_size))

def list_file(path, search, limit_num_to_list, limit_num_to_list_per_req, last_evaluated_key, token):
    files = []
    temp_key = ""
    if last_evaluated_key:
        temp_key = last_evaluated_key

    while True:
        url = API + "/files/private" + path + "?limit=" + str(limit_num_to_list_per_req)
        if temp_key != "":
            url += "&last_evaluated_key=" + temp_key
        result = get_with_auth(url, token)
        if result.status_code == 404:
            break
        data = result.json()
        if len(data) == 0:
            break
        logging.debug(data)
        
        for entry in data:
            if search:
                if re.search(search, entry["filename"]):
                    files.append(entry["filename"])
            else:
                files.append(entry["filename"])
            if limit_num_to_list <= len(files):
                return files
        logging.debug(result.headers)
        if result.headers.get("X-Soracom-Next-Key"):
            logging.debug("continue")
            temp_key = result.headers.get("X-Soracom-Next-Key")
        else:
            logging.debug("list end")
            break

    return files

def auth(auth_key_id, auth_key):
    params = {"authKeyId": auth_key_id, "authKey": auth_key}
    return post_json(API + "/auth", params).json()

def main(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    
    logging.debug(args)
    token = auth(args.auth_key_id, args.auth_key)
    file_names = list_file(
        args.base_path, args.search, args.limit_num_to_list, args.limit_num_to_list_per_req, args.last_evaluated_key, token
    )
    logging.info("List Count: " + str(len(file_names)))
    get_and_save_images(file_names, args.base_path, args.save_path, args.limit_size_to_files, args.delete, token)
    
if __name__ == "__main__":
    default_limit_size_to_files=1024*1024*1024*2.5 #2.5GB

    parser = argparse.ArgumentParser()
    parser.add_argument("--auth_key_id", type=str, required=True)
    parser.add_argument("--auth_key", type=str, required=True)
    parser.add_argument("--base_path", type=str, required=True)

    parser.add_argument("--save_path", type=str, default="./")
    parser.add_argument("--search", type=str, default=None)
    parser.add_argument("--limit_num_to_list", type=int, default=100)
    parser.add_argument("--limit_num_to_list_per_req", type=int, default=100)
    parser.add_argument("--limit_size_to_files", type=int, default=default_limit_size_to_files)
    parser.add_argument("--last_evaluated_key", type=str, default=None)
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--debug", action="store_true")
    
    args = parser.parse_args()
    
    main(args)