from pkb_processor.use_cases.bundle_use_case import run_bundle
from pkb_processor.use_cases.ingest_use_case import run_ingest
from pkb_processor.use_cases.summarize_use_case import run_summarize


def main() -> None:
    import sys

    step = sys.argv[1] if len(sys.argv) > 1 else "help"
    if step == "ingest":
        run_ingest()
    elif step == "summarize":
        run_summarize()
    elif step == "bundle":
        run_bundle()
    else:
        print("usage: python -m pkb_processor.cli [ingest|summarize|bundle]")


if __name__ == "__main__":
    main()
