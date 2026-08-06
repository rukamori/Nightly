import requests
from datetime import datetime, timedelta

time = datetime.now() - timedelta(days=1)
time_format = time.isoformat() + 'Z'

repos = [
    {'owner': 'rukamori', 'name': 'ArchiveTune', 'branch': 'dev', 'label': 'App'},
    {'owner': 'rukamori', 'name': 'core', 'branch': 'main', 'label': 'Core'},
    {'owner': 'rukamori', 'name': 'lyrics', 'branch': 'main', 'label': 'Lyrics'},
    {'owner': 'rukamori', 'name': 'IconPack', 'branch': 'main', 'label': 'Icon Pack'},
    {'owner': 'rukamori', 'name': 'moriextractor', 'branch': 'main', 'label': 'Extractor'},
    {'owner': 'rukamori', 'name': 'morideobfuscator', 'branch': 'main', 'label': 'Deobfuscator'},
]

params = {
    'since': time_format,
}

with open('commits.txt', 'w', encoding='utf-8') as file:
    file.write("## What's Changed\n\n")

    for repo in repos:
        has_updates = False
        url = f'https://api.github.com/repos/{repo["owner"]}/{repo["name"]}/commits'

        if 'branch' in repo:
            params['sha'] = repo['branch']

        response = requests.get(url, params=params)

        if response.status_code == 200:
            commits = response.json()

            if commits:
                file.write(f"### {repo['label']} Updates:\n")
                has_updates = True

                for commit in commits:
                    commit_message = commit['commit']['message'].split('\n')[0]
                    commit_sha = commit['sha'][:7]
                    commit_url = commit['html_url']

                    file.write(f"- {commit_message} - [`{commit_sha}`]({commit_url})\n")

                file.write("\n")

        if not has_updates:
            file.write(f"### {repo['label']} Updates:\n- Nothing changed...\n\n")

    print("✅ File created: commits.txt")
