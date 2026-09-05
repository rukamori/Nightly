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
    lines = []

    for repo in repos:
        url = f'https://api.github.com/repos/{repo["owner"]}/{repo["name"]}/commits'

        if 'branch' in repo:
            params['sha'] = repo['branch']

        response = requests.get(url, params=params)

        if response.status_code == 200:
            commits = response.json()

            if commits:
                lines.append(f"### {repo['label']} Updates:\n")

                for commit in commits:
                    commit_message = commit['commit']['message'].split('\n')[0]
                    commit_sha = commit['sha'][:7]
                    commit_url = commit['html_url']

                    lines.append(f"- {commit_message} - [`{commit_sha}`]({commit_url})\n")

                lines.append("\n")

    if lines:
        file.write("## What's Changed\n\n")
        file.writelines(lines)

    print("✅ File created: commits.txt")
