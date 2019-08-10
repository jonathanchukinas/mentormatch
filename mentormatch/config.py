"""Set storage location for mentormatch files."""

from pathlib import Path


def mentormatch_db_connection():

    # --- Directory for mentormatch files -------------------------------------
    # TODO eventually move this over to ~/
    #   mentormatch_path = Path.home() / ".mentormatch"
    mentormatch_path = (
        Path(__file__).parent.parent.parent / "dummy_home" / ".mentormatch"
    )
    mentormatch_path.mkdir(parents=True, exist_ok=True)

    # --- DB Path -------------------------------------------------------------
    db_path = mentormatch_path / "db.json"

    return db_path
