from environs import env
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def create_api_key(project_id: str, suffix: str) -> Key:
    """
    Creates and restrict an API key in google cloud project.
    """

    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    print(
        f'Successfully created an API key: {response.name}\n'
        f'uid: {response.uid}\n'
        f'display_name: {response.display_name}\n'
        f'key_string: {response.key_string}\n'
        f'create_time: {response.create_time}\n'
        f'update_time: {response.update_time}\n'
    )
    return response


def main():
    env.read_env()
    PROJECT_ID = env.str('PROJECT_ID')
    SUFFIX = env.str('KEY_FILE_NAME')

    create_api_key(PROJECT_ID, SUFFIX)


if __name__ == '__main__':
    main()
