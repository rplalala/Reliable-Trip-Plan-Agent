"""Shared offline identity command options for batch, V0 and controlled entry points."""

from .identity import resolve_identities, resolve_legacy_identities
from .identity_llm import prepare_identity_judgment


def add_identity_options(parser):
    parser.add_argument(
        "--prepare", action="store_true", help="Print a frozen model packet; send nothing"
    )
    parser.add_argument("--model", help="Explicit model name for packet preparation")
    parser.add_argument("--model-result", help="Saved source-bound model-result JSON")
    parser.add_argument(
        "--legacy", action="store_true", help="Explicit historical human/audit replay"
    )
    parser.add_argument("--reviews", help="Historical human review JSON; requires --legacy")


def identity_command(intake, evidence, args, read, *, audit=None, legacy=None):
    """Choose one explicit policy and reject contradictory command options."""
    if args.legacy:
        if args.prepare or args.model or args.model_result:
            raise ValueError("Legacy replay cannot use uniform model options")
        if legacy is not None:
            return legacy(read(args.reviews)).to_dict()
        return resolve_legacy_identities(intake, evidence, read(args.reviews), audit).to_dict()
    if args.reviews or audit is not None:
        raise ValueError("Human/audit inputs require --legacy")
    if args.prepare:
        if args.model_result:
            raise ValueError("Packet preparation cannot import a model result")
        return prepare_identity_judgment(intake, evidence, model=args.model).to_dict()
    if args.model:
        raise ValueError("--model requires --prepare; saved result binds its model")
    return resolve_identities(intake, evidence, model_result=read(args.model_result)).to_dict()
