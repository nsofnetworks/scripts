import os
import boto3
from munch import Munch

REGISTRY_ID = os.environ["REGISTRY_ID"]
client = boto3.client('ecr')


def get_repositories_names():
    args = {
        'registryId': REGISTRY_ID,
    }
    repos = client.describe_repositories(**args)
    names = [repo['repositoryName'] for repo in repos['repositories']]
    return names


def get_repo_images_data(repo, filters=None):
    args = {
        'registryId': REGISTRY_ID,
        'repositoryName': repo,
        'maxResults': 2
    }
    if filters:
        args['filter'] = filters

    images = client.describe_images(**args)
    images_data = []
    for image in images['imageDetails']:
        image_digest = image['imageDigest']
        image_tags = image['imageTags']
        image_pushed_in = image['imagePushedAt']
        images_data.append(Munch(digest=image_digest, tags=image_tags,
                           pushed_in=image_pushed_in))
    return images_data


def get_untagged_repo_images(repo):
    filters = {
        'tagStatus': 'UNTAGGED'
    }
    response = get_repo_images_data(repo, filters)


def get_batch_image(repo, image_data):
    args = {
        'registryId': REGISTRY_ID,
        'repositoryName': repo,
        'imageIds': [
            {
                'imageDigest': image_data.digest,
            },
        ]
    }

    res = client.batch_get_image(**args)
    return res


repos = get_repositories_names()
# print(repos[0])
# get_untagged_repo_images(repos[0])
images_data = get_repo_images_data(repos[0])
# print(images_data)
print(get_batch_image(repos[0], images_data[0]))
