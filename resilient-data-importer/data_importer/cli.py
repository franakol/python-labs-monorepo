"""Command-line interface for the Data Importer."""

import argparse
import logging
import sys
from pathlib import Path

from data_importer import __version__
from data_importer.exceptions import ImporterError
from data_importer.services.import_service import ImportService


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the CLI.

    Args:
        verbose: If True, set level to DEBUG, otherwise INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="data-importer",
        description="Import user data from CSV files into a JSON database.",
        epilog="Example: data-importer --input users.csv --output database.json",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Path to the input CSV file",
        metavar="FILE",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Path to the output JSON file",
        metavar="FILE",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (debug logging)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate input without importing",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any validation error or duplicate",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    logger.info(f"Data Importer v{__version__}")
    logger.info(f"Input: {args.input}")
    logger.info(f"Output: {args.output}")

    try:
        # Create service with appropriate settings
        service = ImportService(
            input_path=args.input,
            output_path=args.output,
            skip_duplicates=not args.strict,
            skip_invalid=not args.strict,
        )

        # Run import or validation
        if args.dry_run:
            logger.info("Running in dry-run mode (validation only)")
            result = service.validate_only()
            action = "validated"
        else:
            result = service.run_import()
            action = "imported"

        # Report results
        print("\n" + "=" * 50)
        print(f"  Import Summary")
        print("=" * 50)
        print(f"  Total rows processed: {result.total_rows}")
        print(f"  Successfully {action}: {result.imported}")
        print(f"  Skipped: {result.skipped}")
        print(f"  Errors: {len(result.errors)}")
        print("=" * 50)

        if result.errors:
            print("\nErrors encountered:")
            for error in result.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(result.errors) > 10:
                print(f"  ... and {len(result.errors) - 10} more errors")

        if result.success:
            logger.info("Import completed successfully!")
            return 0
        else:
            logger.warning("Import completed with issues")
            return 1

    except ImporterError as e:
        logger.error(f"Import failed: {e}")
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        logger.info("Import cancelled by user")
        print("\n⚠️  Import cancelled", file=sys.stderr)
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
