import requests
from requests import exceptions

def import_gists_to_database(db, username, commit=True):

    # Get the data for <username>
    url = 'https://api.github.com/users/{user}/gists'.format(user=username)

    response = requests.get(url)
    if response.status_code == 404:
        raise exceptions.HTTPError

    gist_data = response.json()

    # Insert into db
    insert_cmd = """INSERT INTO gists(
                        github_id,
                        html_url,
                        git_pull_url,
                        git_push_url,
                        commits_url,
                        forks_url,
                        public,
                        created_at,
                        updated_at,
                        comments,
                        comments_url)
                    VALUES(
                        :id,
                        :html_url,
                        :git_pull_url,
                        :git_push_url,
                        :commits_url,
                        :forks_url,
                        :public,
                        :created_at,
                        :updated_at,
                        :comments,
                        :comments_url)"""
    [db.execute(insert_cmd, cur_gist) for cur_gist in gist_data]
    if (commit):
        db.commit()


