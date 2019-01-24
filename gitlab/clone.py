# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import os
import gitlab
from git import Repo

access_token = "xxxxxxxxxxxx"
gitlab_url = "urlurl"
local_dir = "D:\\data\\"

def allprojects():
    """获取gitlab的所有projects"""
    return gl.projects.list(all=True)

def cloneprojects(projects):
    for project in projects:
        print(project.name, project.http_url_to_repo)
        git_url = "https://oauth2:" + access_token + "@" + project.http_url_to_repo[8:]
        try:
            Repo.clone_from(git_url, os.path.join(local_dir, project.name))
        except Exception:
            pass

if __name__ == '__main__':
    gl = gitlab.Gitlab(gitlab_url, private_token=access_token)
    projects = allprojects()
    cloneprojects(projects)
