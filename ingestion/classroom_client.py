import os
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from common.config import CLIENT_FILE, TOKEN_FILE, DOWNLOAD_DIR
from common.models import AcademicContent


SCOPES = [
    f"https://www.googleapis.com/auth/{scope}"
    for scope in [
        "classroom.courses.readonly",
        "classroom.announcements.readonly",
        "classroom.courseworkmaterials.readonly",
        "classroom.coursework.students.readonly",
        "classroom.coursework.me.readonly",
        "drive.readonly",
    ]
]


def get_creds():
    creds = (
        Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if os.path.exists(TOKEN_FILE)
        else None
    )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(
                CLIENT_FILE,
                SCOPES,
            ).run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as file:
            file.write(creds.to_json())

    return creds


def _safe(s):
    return re.sub(r"[^A-Za-z0-9._-]", "_", s)


def _download(drive, file_id, name):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    meta = (
        drive.files()
        .get(fileId=file_id, fields="name,mimeType")
        .execute()
    )

    if meta["mimeType"].startswith("application/vnd.google-apps"):
        data = (
            drive.files()
            .export_media(
                fileId=file_id,
                mimeType="application/pdf",
            )
            .execute()
        )

        mime, ext = "application/pdf", ".pdf"

    else:
        data = (
            drive.files()
            .get_media(fileId=file_id)
            .execute()
        )

        mime = meta["mimeType"]
        ext = ""

    filename = _safe(
        f"{file_id}_{meta['name']}"
    )

    if not meta["name"].endswith(ext):
        filename += ext

    path = os.path.join(
        DOWNLOAD_DIR,
        filename,
    )

    with open(path, "wb") as file:
        file.write(data)

    return path, mime


def fetch_items() -> list[AcademicContent]:
    creds = get_creds()

    classroom = build(
        "classroom",
        "v1",
        credentials=creds,
    )

    drive = build(
        "drive",
        "v3",
        credentials=creds,
    )

    items = []

    courses = (
        classroom.courses()
        .list(
            courseStates=["ACTIVE"],
            pageSize=10,
        )
        .execute()
        .get("courses", [])
    )

    for course in courses:
        course_id = course["id"]

        posts = []

        posts += [
            ("ANNOUNCEMENT", announcement)
            for announcement in (
                classroom.courses()
                .announcements()
                .list(
                    courseId=course_id,
                    pageSize=30,
                )
                .execute()
                .get("announcements", [])
            )
        ]

        posts += [
            ("ASSIGNMENT", coursework)
            for coursework in (
                classroom.courses()
                .courseWork()
                .list(
                    courseId=course_id,
                    pageSize=30,
                )
                .execute()
                .get("courseWork", [])
            )
        ]

        posts += [
            ("MATERIAL", material)
            for material in (
                classroom.courses()
                .courseWorkMaterials()
                .list(
                    courseId=course_id,
                    pageSize=30,
                )
                .execute()
                .get("courseWorkMaterial", [])
            )
        ]

        for classroom_type, post in posts:
            title = (
                post.get("title")
                or post.get("text", "")[:60]
                or "Announcement"
            )

            text = (
                post.get("description")
                or post.get("text")
                or ""
            )

            metadata = {
                "course": course["name"],
                "classroom_type": classroom_type,
                "posted_at": post.get(
                    "updateTime",
                    "",
                ),
            }

            files = [
                material["driveFile"]["driveFile"]
                for material in post.get("materials", [])
                if "driveFile" in material
            ]

            if not files:
                items.append(
                    AcademicContent(
                        id=f"gc_{post['id']}",
                        source="google_classroom",
                        title=title,
                        content=text,
                        metadata=metadata,
                    )
                )

            for file in files:
                path, mime = _download(
                    drive,
                    file["id"],
                    file.get("title", "file"),
                )

                items.append(
                    AcademicContent(
                        id=f"gc_{post['id']}_{file['id']}",
                        source="google_classroom",
                        title=file.get("title", title),
                        content=text,
                        file_path=path,
                        mime_type=mime,
                        metadata=metadata,
                    )
                )

    return items