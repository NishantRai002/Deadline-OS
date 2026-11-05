# DeadlineOS

DeadlineOS is a secure campus notice and deadline board. It brings academic updates from scattered channels into one place, filters them for each student's program, semester, section, and courses, and lets students track what they need to do.

## MVP

- Student and staff sign-in with server-controlled roles
- Staff publish notices and deadlines for a selected audience
- Students see only matching items and track them as pending, in progress, or completed
- Authorized file attachments and in-app upcoming deadline reminders
- A small staff analytics view if the core workflow is complete

The project conversation also describes Azure SQL Database, Azure Blob Storage, Azure App Service, and a live URL as course deliverables. The local development setup should be easy to run first; deploy to the required Azure services after confirming the official project guide, access, and credits. Do not claim a cloud integration until it has been deployed and demonstrated.

## Two-person work split

Agree on the database and route contract before parallel implementation. Use the two owners below in GitHub issues and pull requests.

| Owner | Owns | Suggested paths | First milestone |
| --- | --- | --- | --- |
| Teammate A: backend, data, cloud | Flask routes and services, authentication/authorization, SQL schema and queries, validation, attachment storage, Azure deployment and security | `app/`, `database/`, `docs/api.md`, `docs/data-model.md`, deployment config | Agree contracts; implement login, audience filtering, publishing and status updates |
| Teammate B: frontend, UX, documentation | Page templates, responsive styling and browser interactions, accessible flows, screenshots/demo, report and user documentation | `app/templates/`, `app/static/`, `docs/ui-flows.md`, `docs/report/` | Agree contracts; create the login, student dashboard and staff publishing experience |

Both teammates should contribute commits, review the other's pull requests, and take part in integration, security review, demo and report. Avoid assigning all documentation or testing to one person. Keep changes in the agreed paths where practical; coordinate shared files such as app startup and requirements before editing.

## Work plan

1. **Confirm requirements:** check the official course guide for the required non-relational/file-storage service, analytics deliverable, report format, and deployment expectations. Keep the product scope to the MVP above.
2. **Lock contracts:** agree item fields, route payloads, roles, profile fields, upload limits and storage approach in `docs/` before feature branches diverge.
3. **Build independently:** create small issues and branches such as `backend/auth` and `frontend/dashboard`; open focused pull requests into `main` and request the partner's review.
4. **Integrate and demonstrate:** connect screens to real routes, use sample data only, verify access control and file access, and capture evidence for the report.
5. **Deploy and submit:** use Azure SQL, Azure Blob Storage and Azure App Service as required by the guide; record the live URL, schema/query files, analytics output and report. Keep cloud credentials out of the repository.

## GitHub setup for both teammates

1. One teammate creates a **private** GitHub repository named `DeadlineOS`, adds the other as a collaborator, and pushes this project as the initial `main` branch.
2. Both clone the same repository and configure their own Git identity. Never share GitHub passwords or personal access tokens.
3. For each task, create a branch from an up-to-date `main`, commit only that task, push the branch, and open a pull request. The other teammate reviews it before merge.
4. Use issues for the work items and owners listed in `docs/team-work-plan.md`. Both people should make meaningful commits under their own accounts; do not squash or re-author the partner's work just to make histories look balanced.
5. Add only source, docs, and safe sample data. Keep `.env`, local databases, uploads, credentials, and real student data out of GitHub.

## Run locally

Requires Python 3.11+.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

Set a long random `SECRET_KEY` in `.env` before using sessions beyond local development. The local database is for development only; cloud deployment must use the database required by the course guide.

## Repository map

```text
app/                 Flask application, routes, templates and static files
database/            Local schema and migration/query artifacts
docs/                API, data model, UI flows and team plan
```

## Similarity and approval note

The supplied conversation notes substantial overlap with a public project called Chronosync. Preserve the original DeadlineOS submission receipt/timestamp and public listing screenshot. The conversation summary did not confirm DeadlineOS's current registration status or approval; verify that status and the official first-come rule with the project lead. Do not present the idea as approved until confirmed. Keep DeadlineOS's own implementation and scope distinct, and do not copy Chronosync's wording or materials.
