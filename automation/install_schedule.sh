#!/usr/bin/env bash
# install_schedule.sh — install or remove the com.corpus.daily LaunchAgent
#
# Usage:
#   ./automation/install_schedule.sh            # install (idempotent)
#   ./automation/install_schedule.sh uninstall  # remove the agent
#
# The repo ships ONLY this script and the .plist.template.  The rendered plist
# is written to ~/Library/LaunchAgents/ and is NOT committed to the repo.
#
# CATCH-UP SEMANTICS (R3):
#   launchd's StartCalendarInterval fires the job once at the configured time
#   each day.  If the Mac is asleep at that moment, launchd replays the job
#   exactly ONCE on the next wake — not once per missed interval.  This means
#   you always get one catch-up run after sleep/shutdown with no risk of a
#   flood of back-to-back executions.

set -euo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Resolve the repo root from the location of this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TEMPLATE="${SCRIPT_DIR}/com.corpus.daily.plist.template"
LAUNCH_AGENTS_DIR="${HOME}/Library/LaunchAgents"
PLIST_DEST="${LAUNCH_AGENTS_DIR}/com.corpus.daily.plist"
LABEL="com.corpus.daily"

# Resolve the absolute path to python3 — launchd has NO shell PATH so we
# must embed the full path in the rendered plist.
PYTHON="$(command -v python3)"
if [[ -z "${PYTHON}" ]]; then
    echo "ERROR: python3 not found on PATH.  Install Python 3 and retry." >&2
    exit 1
fi

UID_VAL="$(id -u)"

# ---------------------------------------------------------------------------
# Subcommand: uninstall
# ---------------------------------------------------------------------------

if [[ "${1:-}" == "uninstall" ]]; then
    echo "Uninstalling ${LABEL} …"

    # bootout is a no-op when the job is not loaded; suppress the error.
    launchctl bootout "gui/${UID_VAL}" "${PLIST_DEST}" 2>/dev/null || true

    if [[ -f "${PLIST_DEST}" ]]; then
        rm -f "${PLIST_DEST}"
        echo "Removed ${PLIST_DEST}"
    else
        echo "(plist was not present — nothing to remove)"
    fi

    echo "Done.  The agent is disabled and will not run again."
    exit 0
fi

# ---------------------------------------------------------------------------
# Subcommand: install (default)
# ---------------------------------------------------------------------------

echo "Installing ${LABEL} …"
echo "  Repo root : ${REPO_ROOT}"
echo "  Python    : ${PYTHON}"
echo "  Plist     : ${PLIST_DEST}"

# Verify the template exists before doing anything.
if [[ ! -f "${TEMPLATE}" ]]; then
    echo "ERROR: template not found at ${TEMPLATE}" >&2
    exit 1
fi

# Create the LaunchAgents directory if it doesn't already exist.
mkdir -p "${LAUNCH_AGENTS_DIR}"

# Render the template by substituting __REPO_ROOT__ and __PYTHON__.
# We use a temporary file so a partial write never clobbers the installed copy.
TMP_PLIST="$(mktemp /tmp/com.corpus.daily.XXXXXX.plist)"
trap 'rm -f "${TMP_PLIST}"' EXIT

sed \
    -e "s|__REPO_ROOT__|${REPO_ROOT}|g" \
    -e "s|__PYTHON__|${PYTHON}|g" \
    "${TEMPLATE}" > "${TMP_PLIST}"

# Validate XML well-formedness before installing (requires plutil, always
# present on macOS).
if command -v plutil &>/dev/null; then
    plutil -lint "${TMP_PLIST}"
fi

# Atomically replace the destination.
cp "${TMP_PLIST}" "${PLIST_DEST}"

# ---------------------------------------------------------------------------
# Load idempotently:
#   1. bootout — unload if already loaded (ignore failure when not loaded).
#   2. bootstrap — load the new/updated plist.
#   3. enable  — mark the service enabled so it survives logout/reboot.
# ---------------------------------------------------------------------------

launchctl bootout "gui/${UID_VAL}" "${PLIST_DEST}" 2>/dev/null || true
launchctl bootstrap "gui/${UID_VAL}" "${PLIST_DEST}"
launchctl enable "gui/${UID_VAL}/${LABEL}"

# ---------------------------------------------------------------------------
# Next-step guidance
# ---------------------------------------------------------------------------

cat <<EOF

Installation complete.

VERIFY the agent is registered:
  launchctl print gui/${UID_VAL}/${LABEL}

FORCE a manual run now (useful to test the full pipeline):
  launchctl kickstart -k gui/${UID_VAL}/${LABEL}

WATCH the log during or after a run:
  tail -f ${REPO_ROOT}/raw/.scheduled_run.log

DISABLE without removing (the plist stays in place):
  launchctl disable gui/${UID_VAL}/${LABEL}
  launchctl bootout gui/${UID_VAL} ${PLIST_DEST}

RE-ENABLE after disabling:
  launchctl enable gui/${UID_VAL}/${LABEL}
  launchctl bootstrap gui/${UID_VAL} ${PLIST_DEST}

UNINSTALL entirely (removes the plist from ~/Library/LaunchAgents/):
  ${SCRIPT_DIR}/install_schedule.sh uninstall

CATCH-UP NOTE:
  The job fires daily at 08:00.  If the Mac is asleep at that time, launchd
  replays the job exactly ONCE on the next wake.  Missed intervals do NOT
  accumulate, so you always get at most one catch-up run after sleep/shutdown.

EOF
