import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.courses.module_sync_runtime import (
    default_output_root,
    load_selected_packs,
    publish_course_pack,
    sync_course_pack,
    validate_course_definition,
    validate_synced_course,
)


class Command(BaseCommand):
    help = "Run the module content sync for Module 4, Module 6, and Module 8."

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            choices=["draft", "sync", "validate", "publish", "run-all"],
            default="run-all",
            help="draft=pack validation, sync=upsert content/artifacts, validate=current DB/files, publish=set published, run-all=sync+validate+publish",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply database and file changes. Without this flag, the command reports planned actions only.",
        )
        parser.add_argument(
            "--output-root",
            default=str(default_output_root()),
            help="Repo root for generated lesson artifacts.",
        )
        parser.add_argument(
            "--course",
            action="append",
            dest="courses",
            help="Limit execution to a course slug. Repeat to run multiple modules.",
        )

    def handle(self, *args, **options):
        mode = options["mode"]
        apply = options["apply"]
        output_root = Path(options["output_root"]).resolve()
        selected_packs = load_selected_packs(options.get("courses"))

        if not selected_packs:
            raise CommandError("No mission packs matched the selected course filters.")

        report = {
            "mode": mode,
            "apply": apply,
            "output_root": str(output_root),
            "courses": [],
            "passed": True,
        }

        structure_errors: list[str] = []
        for pack in selected_packs:
            course_report = {
                "slug": pack["slug"],
                "title": pack["title"],
                "structure_errors": validate_course_definition(pack),
                "sync": None,
                "validation_errors": [],
                "publish": None,
            }
            structure_errors.extend(course_report["structure_errors"])

            if mode in {"sync", "run-all"}:
                course_report["sync"] = sync_course_pack(pack, output_root=output_root, apply=apply)

            if mode == "validate":
                course_report["validation_errors"] = validate_synced_course(pack, output_root)
            elif mode == "publish":
                course_report["validation_errors"] = validate_synced_course(pack, output_root)
                if not course_report["validation_errors"]:
                    course_report["publish"] = publish_course_pack(pack, apply=apply)
            elif mode == "run-all":
                if apply:
                    course_report["validation_errors"] = validate_synced_course(pack, output_root)
                    if not course_report["validation_errors"]:
                        course_report["publish"] = publish_course_pack(pack, apply=True)
                else:
                    course_report["publish"] = {"slug": pack["slug"], "published": False, "applied": False}

            report["courses"].append(course_report)

        if structure_errors:
            report["passed"] = False
            self.stdout.write(json.dumps(report, indent=2))
            raise CommandError("One or more mission packs are structurally invalid.")

        validation_failures = [
            error
            for course_report in report["courses"]
            for error in course_report.get("validation_errors", [])
        ]
        if validation_failures:
            report["passed"] = False

        self.stdout.write(json.dumps(report, indent=2))

        if validation_failures and mode in {"validate", "publish", "run-all"} and apply:
            raise CommandError("Validation failed for one or more modules.")